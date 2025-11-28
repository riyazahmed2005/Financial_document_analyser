from crewai import Task
from agents import financial_analyst, investment_advisor

analyze_financial_document = Task(
  description=(
      "Analyze the financial document located at {file_path}. "
      "Provide a detailed analysis of the company's financial health, performance, and market position. "
      "Your analysis should be comprehensive and well-supported by data from the document."
  ),
  expected_output=(
      "A detailed financial analysis report, including key metrics, trends, and a summary "
      "of the company's financial standing. The report should be easy for investors to understand."
  ),
  agent=financial_analyst,
)

investment_recommendation = Task(
  description=(
      "Based on the previous financial analysis, provide clear investment recommendations. "
      "Consider the user's query: {query}. "
      "Evaluate the company's growth potential, risks, and market trends."
  ),
  expected_output=(
      "A set of clear investment recommendations (e.g., Buy, Hold, Sell) with detailed "
      "justifications. The recommendations should be practical and actionable."
  ),
  agent=investment_advisor,
  context=[analyze_financial_document] # This task depends on the first one
)