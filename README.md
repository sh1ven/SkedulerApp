---
title: SkedulerApp
emoji: 💬
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 4.36.1
app_file: app.py
pinned: false
---
# Skeduler Chatbot

This repository contains the code for the Skeduler Chatbot, a document-based chatbot that helps users with various queries related to booking appointments, finding locations, and more. The chatbot uses a combination of PDF document parsing, vector database search, and natural language processing to provide relevant information to users.

## Features

- **PDF Document Parsing**: Extracts text from a PDF file to build a knowledge base.
- **Vector Database**: Uses SentenceTransformers and FAISS to create a searchable vector database of the document content.
- **Natural Language Processing**: Utilizes the HuggingFace InferenceClient to generate responses based on user queries and the context provided by the PDF documents.
- **Gradio Interface**: Provides an easy-to-use web interface for interacting with the chatbot.



## Usage

1. Place your PDF document (`skeduler_knowledge_base.pdf`) in the project directory.

2. Run the chatbot:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to the URL provided by Gradio to interact with the chatbot.

## Code Overview

### `app.py`

This is the main file containing the chatbot implementation.

- **Imports**: Necessary libraries are imported.
- **MyApp Class**: Handles PDF loading, vector database creation, and document searching.
  - `__init__`: Initializes the app, loads the PDF, and builds the vector database.
  - `load_pdf`: Extracts text from the PDF and stores it in the documents attribute.
  - `build_vector_db`: Generates embeddings for the document contents and builds a FAISS index.
  - `search_documents`: Searches for relevant documents based on a query using vector similarity.
- **respond Function**: Handles the conversation flow, integrates document search results, and generates responses using the HuggingFace InferenceClient.
- **Gradio Interface**: Sets up the Gradio interface for user interaction.

### Example Queries

- "Can you help me book an appointment?"
- "Can you guide me through the app?"
- "How do I find the nearest location?"
- "How can I cancel an appointment?"
- "How can I get reminders for my appointment?"
- "What are all the different services available?"
- "Available Payment Methods"
- "Payment history"
- "Security and Privacy"
- "Support"

## Disclaimer

This chatbot is based on a Skeduler Space that is publicly available. It is not an official app for booking appointments in real-time, and the use of this chatbot is at your own responsibility.

## Contributing

Feel free to submit issues and pull requests if you have any suggestions or improvements.


---

