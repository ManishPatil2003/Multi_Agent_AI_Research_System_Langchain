from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

#model setup 
llm = ChatOpenAI(model = "gpt-4o-mini",temperature=0)


#1st agent 
def build_search_agent():
    return create_agent(
        model = llm,
        tools= [web_search]
    )
    
    
#2nd agent 

def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )
    
#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()


#critic chain

critic_prompt = ChatPromptTemplate.from_messages([
      ("system",
     """
     You are a senior research reviewer.

     Use this scoring rubric:

     9-10:
     Exceptional report with strong evidence,
     analysis, citations and depth.

     7-8:
     Good report with minor weaknesses.

     5-6:
     Missing depth or evidence.

     3-4:
     Significant weaknesses.

     1-2:
     Poor quality.
     """),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()