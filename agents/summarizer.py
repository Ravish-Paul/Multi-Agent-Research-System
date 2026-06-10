from langchain_core.prompts import PromptTemplate
from llm import llm_model

summary_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    you are an expert summarizer.

    summarize the folloing topic
    
    {topic}

    """
)

def summarize_agent(research):
    chain = summary_prompt | llm_model
    response = chain.invoke({"topic":research})
    print("====Summary====")
    print(response.content[0]["text"])
    return response.content[0]["text"]