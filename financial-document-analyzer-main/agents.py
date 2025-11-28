# agents.py

import os
from dotenv import load_dotenv
from crewai import Agent
from tools import read_data_tool
from langchain_community.llms import Ollama

load_dotenv()

# We've switched to the more capable Llama 3 model
llm = Ollama(model="llama3")

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents to provide investment insights and recommendations",
    verbose=True,
    memory=True,
    backstory=(
        "With a wealth of experience in financial markets, you are a seasoned analyst "
        "known for your keen eye for detail and insightful investment advice."
    ),
    tools=[read_data_tool],
    llm=llm,
    allow_delegation=True
)

investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide personalized investment advice based on financial analysis",
    verbose=True,
    memory=True,
    backstory=(
        "As a trusted investment advisor, you help clients achieve their financial goals "
        "by providing tailored investment strategies based on thorough analysis."
    ),
    tools=[],
    llm=llm,
    allow_delegation=False,
)