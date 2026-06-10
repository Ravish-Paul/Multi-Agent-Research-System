from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)
