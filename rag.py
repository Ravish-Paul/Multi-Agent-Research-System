from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def get_rag_context(query, pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
    )

    embedding = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
    )

    chunks = splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(
        chunks,
        embedding
    )
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )
    return context
