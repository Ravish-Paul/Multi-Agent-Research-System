from langchain_core.prompts import PromptTemplate
from llm import llm_model

fact_check_prompt = PromptTemplate.from_template(
"""
You are an expert fact checker

Review the following research
Research:
{research}

Rheck:
- Unsupported claims
- Inconsistencies
- Possible inaccuracies
"""
)

def fact_checker_agent(research):
    chain = fact_check_prompt | llm_model
    response = chain.invoke({"research": research})
    print("=====Fact Checker=====")
    print(response.content)
    return response.content