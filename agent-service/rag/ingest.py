from pathlib import Path
import shutil

from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader
)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"
CHROMA_DIR = BASE_DIR / "chroma_db"


if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)

docs = []


csv_files = [
    KNOWLEDGE_DIR / "rooms.csv",
    KNOWLEDGE_DIR / "services.csv",
    KNOWLEDGE_DIR / "schedules.csv",
    KNOWLEDGE_DIR / "faq.csv",
]

for file in csv_files:

    if file.exists():

        loader = CSVLoader(
            file_path=str(file),
            encoding="utf-8"
        )

        docs.extend(loader.load())


for file in KNOWLEDGE_DIR.glob("*.txt"):

    loader = TextLoader(
        str(file),
        encoding="utf-8"
    )

    docs.extend(loader.load())


splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    separators=[
        "\n\n",
        "\n",
        ".",
        "،",
        " "
    ]
)

docs = splitter.split_documents(docs)


unique_docs = []
seen = set()

for doc in docs:

    content = doc.page_content.strip()

    if content not in seen:

        seen.add(content)
        unique_docs.append(doc)

docs = unique_docs


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)

print(f"Indexed {len(docs)} chunks")
print("Knowledge Base Created Successfully")