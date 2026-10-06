import os
import re
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from google import genai


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

load_dotenv()

BASE_DIR = Path(__file__).parent

FAQ_FILE = BASE_DIR / "data" / "college_faq.txt"

DB_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "college_faq"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

GEMINI_MODEL = "gemini-3.8-flash"



# ---------------------------------------------------------
# STREAMLIT
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Based College FAQ Chatbot",
    page_icon="🎓"
)

st.title("🎓 AI Based College FAQ Chatbot")

st.write(
    "Ask questions about college facilities, departments, "
    "certificates, placements, library and more."
)


# ---------------------------------------------------------
# CHECK API KEY
# ---------------------------------------------------------

api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")


if not api_key:

    st.error("Google API key is missing.")

    st.info(
        "Create a .env file and add:\n\n"
        "GOOGLE_API_KEY=YOUR_API_KEY"
    )

    st.stop()


# ---------------------------------------------------------
# GEMINI
# ---------------------------------------------------------

try:

    gemini = genai.Client(
        api_key=api_key
    )

except Exception as error:

    st.error(
        f"Gemini initialization error: {error}"
    )

    st.stop()


# ---------------------------------------------------------
# LOAD EMBEDDING MODEL
# ---------------------------------------------------------

@st.cache_resource
def get_embedding_model():

    return SentenceTransformer(
        EMBEDDING_MODEL
    )


embedding_model = get_embedding_model()


# ---------------------------------------------------------
# READ FAQ FILE
# ---------------------------------------------------------

if not FAQ_FILE.exists():

    st.error(
        f"FAQ file not found:\n{FAQ_FILE}"
    )

    st.stop()


faq_text = FAQ_FILE.read_text(
    encoding="utf-8"
)


# ---------------------------------------------------------
# PARSE FAQ
# ---------------------------------------------------------

def parse_faq(text):

    pattern = r"Q:\s*(.*?)\s*A:\s*(.*?)(?=\s*Q:|\Z)"

    matches = re.findall(
        pattern,
        text,
        re.DOTALL | re.IGNORECASE
    )

    faq_list = []

    for question, answer in matches:

        question = " ".join(
            question.split()
        )

        answer = " ".join(
            answer.split()
        )

        if question and answer:

            faq_list.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

    return faq_list


faq_list = parse_faq(
    faq_text
)


if not faq_list:

    st.error(
        "No FAQ entries were found."
    )

    st.info(
        "Use this format:\n\n"
        "Q: Your question?\n"
        "A: Your answer."
    )

    st.stop()


# ---------------------------------------------------------
# CHROMA DATABASE
# ---------------------------------------------------------

@st.cache_resource
def get_collection(faq_data):

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Create database only if empty
    if collection.count() == 0:

        documents = []

        ids = []

        for number, item in enumerate(faq_data):

            document = (
                "Question: "
                + item["question"]
                + "\nAnswer: "
                + item["answer"]
            )

            documents.append(
                document
            )

            ids.append(
                f"faq_{number}"
            )

        embeddings = embedding_model.encode(
            documents
        ).tolist()

        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )

    return collection


collection = get_collection(
    faq_list
)


# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

def search_faq(question):

    question_embedding = embedding_model.encode(
        [question]
    ).tolist()

    result = collection.query(
        query_embeddings=question_embedding,
        n_results=min(
            3,
            collection.count()
        )
    )

    if not result["documents"]:

        return []

    return result["documents"][0]


# ---------------------------------------------------------
# GEMINI ANSWER
# ---------------------------------------------------------

def get_answer(
    question,
    documents
):

    if not documents:

        return (
            "I couldn't find this information "
            "in the college FAQ."
        )

    context = "\n\n".join(
        documents
    )

    prompt = f"""
You are a college FAQ chatbot.

Use the following FAQ information to answer
the student's question.

FAQ INFORMATION:
{context}

STUDENT QUESTION:
{question}

Rules:
- Answer only using the FAQ information.
- Do not invent information.
- Give a short and clear answer.
- If the information is not available, say:
  "I couldn't find this information in the college FAQ."

Answer:
"""

    for attempt in range(3):

        try:

            response = gemini.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as error:

            if "503" in str(error) and attempt < 2:

                time.sleep(3)

            else:

                raise error

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("📊 System Information")

st.sidebar.write(
    f"FAQ entries: {len(faq_list)}"
)

st.sidebar.write(
    f"Database entries: {collection.count()}"
)

st.sidebar.success(
    "✅ Chatbot ready"
)


# ---------------------------------------------------------
# CHAT
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


question = st.chat_input(
    "Ask your question..."
)


if question:

    # Show question
    with st.chat_message("user"):

        st.write(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Search
    with st.spinner(
        "🔎 Searching FAQ..."
    ):

        documents = search_faq(
            question
        )

    # Generate answer
    with st.spinner(
        "🤖 Generating answer..."
    ):

        try:

            answer = get_answer(
                question,
                documents
            )

        except Exception as error:

            answer = (
                "Sorry, an error occurred:\n\n"
                + str(error)
            )

    # Show answer
    with st.chat_message("assistant"):

        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )