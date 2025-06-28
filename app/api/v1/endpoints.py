# FastAPI API endpoints
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.internal.llm.chain import get_llm_client, get_analysis_prompt_template, build_stock_analysis_chain_with_retry

router = APIRouter()

class StockAnalysisRequest(BaseModel):
    stock_id: str

class StockAnalysisResponse(BaseModel):
    stock_id: str
    suggestion: str
    reason: str

@router.post("/stock/llm-report", response_model=StockAnalysisResponse)
async def get_stock_llm_report(request: StockAnalysisRequest):
    """
    Generate a stock analysis report using LLM based on technical indicators.
    Returns a clear, actionable trading suggestion and rationale.
    """
    llm_client = get_llm_client()
    prompt_template = get_analysis_prompt_template()
    chain = build_stock_analysis_chain_with_retry(llm_client, prompt_template)
    try:
        llm_result = await chain.ainvoke(request.stock_id)
        # Ensure the response is in the expected JSON format
        return StockAnalysisResponse(
            stock_id=llm_result.get("stock_id", request.stock_id),
            suggestion=llm_result.get("suggestion", ""),
            reason=llm_result.get("reason", "")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM analysis failed: {str(e)}")
