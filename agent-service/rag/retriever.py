from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vectordb = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
)

KEYWORDS = {
    "واتساب": ["واتساب"],
    "whatsapp": ["واتساب"],
    "الهاتف": ["الهاتف"],
    "رقم": ["الهاتف"],
    "التواصل": ["التواصل"],
    "العنوان": ["العنوان"],
    "عنوان": ["العنوان"],
    "موقع": ["العنوان"],
    "مواعيد": ["ساعات الاستقبال"],
    "دوام": ["ساعات الاستقبال"],
    "ساعات العمل": ["ساعات الاستقبال"],
    "الغرفة القياسية": ["service: الغرفة القياسية"],
    "الجناح الفاخر": ["service: الجناح الفاخر"],
    "الجناح الملكي": ["service: الجناح الملكي"],

    # الغرف والأجنحة
    "الغرف": ["غرفة"],
    "الأجنحة": ["جناح"],
    "غرفة": ["غرفة"],
    "جناح": ["جناح"],
    "من هي الغرف": ["غرفة"],
    "خيارات الإقامة": ["غرفة"],
}

ROOM_QUERIES = [
    "الغرف",
    "الأجنحة",
    "أنواع الغرف",
    "خيارات الإقامة",
    "من هي الغرف",
    "ما هي الأجنحة",
    "الغرفة القياسية",
    "الجناح الفاخر",
    "الجناح الملكي",
]


def retrieve_context(query: str) -> str:

    query_lower = query.lower()

    # ==========================
    # لو السؤال عن الغرف
    # رجع الملف كاملاً مباشرة
    # ==========================

    if any(word in query_lower for word in ROOM_QUERIES):

        rooms_file = BASE_DIR / "knowledge" / "rooms.txt"

        if rooms_file.exists():

            return rooms_file.read_text(
                encoding="utf-8"
            )

    # ==========================
    # البحث العادي
    # ==========================

    results = vectordb.similarity_search_with_score(
        query,
        k=20
    )

    ranked = []

    for doc, score in results:

        content = doc.page_content

        boost = 0

        for trigger, targets in KEYWORDS.items():

            if trigger.lower() in query_lower:

                for target in targets:

                    if target in content:
                        boost += 1000

        ranked.append(
            (
                boost - float(score),
                content
            )
        )

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    seen = set()
    final_docs = []

    for _, content in ranked:

        content = content.strip()

        if content in seen:
            continue

        seen.add(content)

        final_docs.append(content)

    return "\n\n".join(final_docs[:5])