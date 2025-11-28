# tools.py

from dotenv import load_dotenv
from crewai_tools import tool
from langchain_community.document_loaders import UnstructuredFileLoader

load_dotenv()

@tool("Financial Document Reader Tool")
def read_data_tool(path: str) -> str:
    """
    Reads and processes the full text content from a financial document PDF.
    Args:
        path (str): The file path to the PDF document.
    """
    print(f"--- Reading document from path: {path} ---")
    loader = UnstructuredFileLoader(file_path=path)
    docs = loader.load()
    full_report = "\n".join(doc.page_content for doc in docs)
    return full_report