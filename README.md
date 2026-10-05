🎓 AI Based College FAQ Chatbot
📌 Project Description

The AI Based College FAQ Chatbot is an intelligent chatbot designed to help college students quickly find answers to frequently asked questions.

The chatbot allows students to ask questions in natural language about college departments, library facilities, examinations, certificates, placements, hostel, transport, attendance and other college-related services.

The system uses Artificial Intelligence, Natural Language Processing, semantic search, vector embeddings, ChromaDB and Google Gemini to provide relevant and easy-to-understand answers.

🎯 Objectives

Provide quick answers to common college-related questions.

Reduce the workload of college administrative staff.

Allow students to interact using natural language.

Retrieve relevant information from the college FAQ knowledge base.

Generate clear and student-friendly answers using Generative AI.

Provide a simple web-based interface using Streamlit.

✨ Features

🎓 College FAQ chatbot

🤖 AI-generated responses

🔎 Semantic search

🧠 Sentence Transformer embeddings

🗄️ ChromaDB vector database

💬 Natural-language question answering

📚 College FAQ knowledge base

🌐 Streamlit web interface

🔐 API key stored securely using .env

⚡ Fast retrieval of relevant FAQ information

🛠️ Technologies Used
Technology	Purpose
Python 3.11.9	Programming language
Streamlit	Web application interface
Google Gemini	Generative AI
Sentence Transformers	Text embeddings
ChromaDB	Vector database
PyTorch	Machine learning framework
python-dotenv	Environment variable management
🧠 System Architecture
             Student
                │
                ▼
        ┌─────────────────┐
        │  Streamlit UI   │
        └────────┬────────┘
                 │
                 ▼
        Student Question
                 │
                 ▼
       ┌──────────────────┐
       │ Sentence         │
       │ Transformer      │
       │ Embedding Model  │
       └────────┬─────────┘
                │
                ▼
          ┌───────────┐
          │ ChromaDB  │
          │ Vector DB │
          └─────┬─────┘
                │
                ▼
       Relevant FAQ Data
                │
                ▼
       ┌─────────────────┐
       │ Google Gemini   │
       │ Generative AI   │
       └────────┬────────┘
                │
                ▼
          AI Response
                │
                ▼
             Student

🔄 How the System Works
1. Student asks a question

The student enters a question through the Streamlit chatbot.

Example:

How can I get a bonafide certificate?

2. Question embedding

The Sentence Transformer model converts the question into a numerical vector representation called an embedding.

3. Semantic search

ChromaDB searches the college FAQ database for information that is semantically similar to the student's question.

4. Relevant information retrieval

The most relevant FAQ entries are retrieved from the vector database.

5. AI response generation

The retrieved information is provided to Google Gemini.

Gemini generates a clear response based on the retrieved college information.

6. Response displayed

The final answer is displayed to the student through the Streamlit interface.

📂 Project Structure
AI-College-FAQ-Chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    └── college_faq.txt


The .env file contains the Gemini API key and is intentionally excluded from GitHub.

⚙️ Installation
Step 1: Clone the repository
git clone https://github.com/YOUR_USERNAME/AI-College-FAQ-Chatbot.git

Step 2: Enter the project directory
cd AI-College-FAQ-Chatbot

Step 3: Create a virtual environment
python -m venv .venv

Step 4: Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Step 5: Install dependencies
pip install -r requirements.txt

🔑 API Key Configuration

Create a .env file in the project directory:

GOOGLE_API_KEY=YOUR_GEMINI_API_KEY


Replace YOUR_GEMINI_API_KEY with your actual Gemini API key.

Never upload the .env file to GitHub.

▶️ Running the Application

After installing the dependencies and configuring the API key, run:

streamlit run app.py


The application will open in your browser.

💬 Sample Questions

Students can ask questions such as:

How can I get a bonafide certificate?

What are the library timings?

How can I register for placements?

Is attendance compulsory?

How can I get a transfer certificate?

Does the college provide hostel facilities?

How can I contact the CSE department?

📚 Knowledge Base

The chatbot uses:

data/college_faq.txt


as its college knowledge base.

The FAQ file can be updated with additional questions and answers according to the requirements of the college.

🔐 Security

The Gemini API key is stored in the .env file and excluded from version control using .gitignore.

The following files/folders should not be uploaded:

.env
.venv/
venv/
chroma_db/

🚀 Future Enhancements

Voice-based questions and answers

Multi-language support

PDF document upload

Admin dashboard

Automatic FAQ updates

College notice integration

Student authentication

Mobile application

Voice assistant

Support for multiple departments

Integration with college websites

🎓 Project Information

Project Title: AI Based College FAQ Chatbot

Class/Section: CSE-B

Domain: Artificial Intelligence / Natural Language Processing

Application Type: Web-based AI Chatbot

👨‍💻 Team

Add your team members here:

1. Name - Roll Number
2. Name - Roll Number
3. Name - Roll Number
4. Name - Roll Number

📄 License

This project is developed as an academic project for educational purposes.