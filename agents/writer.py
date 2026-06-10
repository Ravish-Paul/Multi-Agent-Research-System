from langchain_core.prompts import PromptTemplate
from llm import llm_model

report_writer = PromptTemplate.from_template("""
You are a professional technical report writer.

Create a well-structured report using the information below.

Include:

# Title

# Introduction

# Key Findings

# Analysis

# Conclusion

Information:

{summary}
""")

def writer_agent(summary):
    chain = report_writer | llm_model
    response = chain.invoke({"summary": summary})
    print("====writer====")
    print(response.content[0]["text"])
    return response.content[0]["text"]