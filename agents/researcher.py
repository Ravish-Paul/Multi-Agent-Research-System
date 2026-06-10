from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from rag import get_rag_context
from llm import llm_model

search = DuckDuckGoSearchRun()

research_prompt = PromptTemplate(
    input_variables=["topic", "context", "search_result"],
    template="""
You are an expert researcher.

If PDF Context is available,
prioritize PDF Context over web results.

Only use web results if the answer
cannot be found in the PDF.

Web Search Results:
{search_result}

PDF Context:
{context}

Question:
{topic}

Answer the question.
"""
)
def research_agent(topic, pdf_path=None):
    context = ""
    if pdf_path:
        context = get_rag_context(topic, pdf_path)
        
    search_result = search.invoke(topic)
    chain = research_prompt | llm_model
    response = chain.invoke({"topic": topic, "context": context, "search_result": search_result})
    print("====Search Result======")
    print(search_result)
    print("\n===== RAG CONTEXT =====\n")
    print(context[:2000])
    print("=======Model Research Response======")

    content = response.content

    if isinstance(content, list):
        content = content[0]["text"]

    print(content)

    return context, content
