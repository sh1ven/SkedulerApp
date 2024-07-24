import gradio as gr
from huggingface_hub import InferenceClient
from typing import List, Tuple
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")

class MyApp:
    def __init__(self) -> None:
        self.documents = []
        self.embeddings = None
        self.index = None
        self.load_pdf("skeduler knowledge base.pdf")
        self.build_vector_db()

    def load_pdf(self, file_path: str) -> None:
        """Extracts text from a PDF file and stores it in the app's documents."""
        doc = fitz.open(file_path)
        self.documents = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            self.documents.append({"page": page_num + 1, "content": text})
        print("PDF processed successfully!")

    def build_vector_db(self) -> None:
        """Builds a vector database using the content of the PDF."""
        model = SentenceTransformer('all-MiniLM-L6-v2')
        # Generate embeddings for all document contents
        self.embeddings = model.encode([doc["content"] for doc in self.documents])
        # Create a FAISS index
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        # Add the embeddings to the index
        self.index.add(np.array(self.embeddings))
        print("Vector database built successfully!")

    def search_documents(self, query: str, k: int = 3) -> List[str]:
        """Searches for relevant documents using vector similarity."""
        model = SentenceTransformer('all-MiniLM-L6-v2')
        # Generate an embedding for the query
        query_embedding = model.encode([query])
        # Perform a search in the FAISS index
        D, I = self.index.search(np.array(query_embedding), k)
        # Retrieve the top-k documents
        results = [self.documents[i]["content"] for i in I[0]]
        return results if results else ["No relevant documents found."]


app = MyApp()

def respond(
    message: str,
    history: List[Tuple[str, str]],
    system_message: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
):
    system_message = "Booking appointments now easier than ever, skip the long queues and do it the way you want it to be. Booking an appointment or trying to find our nearest location, With the Skeduler you can do everything at one go"
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    # Retrieve relevant documents
    retrieved_docs = app.search_documents(message)
    context = "\n".join(retrieved_docs)
    messages.append({"role": "system", "content": "Relevant documents:\n" + context})

    response = ""
    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content
        response += token
    return response

demo = gr.Blocks()

with demo:
    gr.Markdown("🧘‍♀️ **Skeduler**")
    gr.Markdown(
        "‼️Disclaimer: This chatbot is based on a Skeduler Space that is publicly available. "
        "This not an official app for booking appointments in real time, and the use of this chatbot is at your own responsibility.‼️"
    )
    
    chatbot = gr.ChatInterface(
        respond,
        examples=[
            ["Can you help me book an appointment? "],
            ["Can you guide me through the app?"],
            ["How do I find the nearest location?"],
            ["How can I cancel an appointment? "],
            ["How can I get reminders for  my appointment?"],
            ["What are all the different services available?"],
            ["Available Payment Methods"],
            ["Payment history"],
            ["Security and Privacy"],
            ["Support"],
        ],
        title='Skeduler 👩‍⚕️'
    )

if __name__ == "__main__":
    demo.launch()
