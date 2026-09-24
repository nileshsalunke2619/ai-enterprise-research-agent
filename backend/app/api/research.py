from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.agent.graph import build_research_graph
from app.db.database import get_db
from app.db.models import ResearchReport
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=ResearchResponse,
)
async def create_research(
    request: ResearchRequest,
    db: Session = Depends(get_db),
):

    # --------------------------------------------------
    # 1. Build LangGraph
    # --------------------------------------------------

    graph = build_research_graph()

    # --------------------------------------------------
    # 2. Initial agent state
    # --------------------------------------------------

    initial_state = {
        "company_name": request.company_name,
        "errors": [],
    }

    # --------------------------------------------------
    # 3. Execute agent
    # --------------------------------------------------

    try:

        result = await graph.ainvoke(
            initial_state
        )

    except Exception as error:

        raise HTTPException(
            status_code=502,
            detail=f"Agent execution failed: {error}",
        )

    # --------------------------------------------------
    # 4. Get generated report
    # --------------------------------------------------

    report_content = result.get("report")

    if not report_content:

        raise HTTPException(
            status_code=502,
            detail="Agent completed without generating a report.",
        )

    # --------------------------------------------------
    # 5. Save report in PostgreSQL
    # --------------------------------------------------

    company_name = result.get(
        "company_name",
        request.company_name,
    )

    report = ResearchReport(
        company_name=company_name,
        report_content=report_content,
        user_id=1,  # temporary until JWT authentication
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    # --------------------------------------------------
    # 6. Return API response
    # --------------------------------------------------

    return report