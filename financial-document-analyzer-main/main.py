# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import database # Import our new database module
from crewai import Crew, Process
from agents import financial_analyst, investment_advisor
from task import analyze_financial_document, investment_recommendation

# Initialize the application and the database
app = FastAPI(title="Financial Document Analyzer with Background Processing")
database.init_db()

def run_crew_analysis(query: str, file_path: str, job_id: str):
    """
    This is our "worker" function. It runs the CrewAI analysis
    and saves the result to the database.
    """
    print(f"--- Starting analysis for job_id: {job_id} ---")
    try:
        crew = Crew(
          agents=[financial_analyst, investment_advisor],
          tasks=[analyze_financial_document, investment_recommendation],
          process=Process.sequential,
          verbose=2
        )
        result = crew.kickoff(inputs={'query': query, 'file_path': file_path})
        
        # Save the result to the database
        database.update_job_result(job_id, str(result))
        print(f"--- Finished analysis for job_id: {job_id} ---")

    except Exception as e:
        print(f"--- Error during analysis for job_id: {job_id}: {e} ---")
        database.update_job_result(job_id, f"Error: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/analyze", status_code=202)
async def analyze_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Provide a detailed financial analysis and investment recommendation.")
):
    """
    This endpoint now starts a background job for analysis and immediately
    returns a job ID.
    """
    # Save the file temporarily with a unique name
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    # Create a job entry in the database
    job_id = database.create_job(file.filename)
    
    # Add the long-running analysis task to the background
    background_tasks.add_task(run_crew_analysis, query, file_path, job_id)
    
    return {"message": "Analysis has been started.", "job_id": job_id}

@app.get("/results/{job_id}")
async def get_results_endpoint(job_id: str):
    """
    This new endpoint allows the user to check the status and result
    of an analysis job using its job ID.
    """
    result = database.get_job_status(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
        
    status, analysis_result = result
    return {"job_id": job_id, "status": status, "result": analysis_result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)