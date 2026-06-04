from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated
from pipeline import run_research_pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Research Pipeline API",
    description="API for running AI-powered research pipeline",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────
# Pydantic Models
# ───────────────────────────────

class ResearchRequest(BaseModel):
    topic: Annotated[str, Field(..., min_length=3, max_length=300, description="Topic to research")]


class ResearchResponse(BaseModel):
    search_result: str = Field(..., description="Results from the search agent")
    scraped_content: str = Field(..., description="Scraped content from top URL")
    report: str = Field(..., description="Final written report by the writer")
    feedback: str = Field(..., description="Critic's feedback on the report")


# ───────────────────────────────
# Routes
# ───────────────────────────────

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Research Pipeline API is running"}


@app.post("/research", response_model=ResearchResponse)
def run_research(request: ResearchRequest):
    try:
        result = run_research_pipeline(request.topic)

        return ResearchResponse(
            search_result=result["search_result"],
            scraped_content=result["scraped_content"],
            report=result["report"],
            feedback=result["feedback"]
        )

    except KeyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline returned incomplete data. Missing key: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline failed: {str(e)}"
        )