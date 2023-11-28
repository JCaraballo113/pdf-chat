import os
import pinecone
from langchain.vectorstores import Pinecone
from app.chat.embeddings.openai import embeddings
from app.chat.models import ChatArgs

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME"),
)

vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings)


def build_retriever(chat_args: ChatArgs, k):
    """
    :param retriever_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :param k: The number of documents to retrieve

    :return: A retriever

    Example Usage:

        retriever = build_retriever(retriever_args)
    """
    search_kwargs = {
        "filter": {"pdf_id": chat_args.pdf_id},
        "k": k,
    }
    return vector_store.as_retriever(search_kwargs=search_kwargs)
