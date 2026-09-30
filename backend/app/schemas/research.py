from datetime import datetime

from pydantic import BaseModel, Field


# ============================================================
# REQUEST
# ============================================================

class ResearchRequest(BaseModel):
    company_name: str


# ============================================================
# STRUCTURED REPORT
# ============================================================

class RecentDevelopment(BaseModel):
    development: str
    date: str
    source: str
    business_relevance: str


class BusinessSignal(BaseModel):
    signal: str
    category: str
    evidence: str


class PainPoint(BaseModel):
    pain_point: str
    evidence: str
    reasoning: str


class Opportunity(BaseModel):
    opportunity: str
    evidence: str
    why_it_matters: str
    suggested_action: str


class Risk(BaseModel):
    risk: str
    evidence: str


class NextAction(BaseModel):
    action: str
    reason: str


class CompanyOverview(BaseModel):
    company: str
    ticker: str
    sector: str
    industry: str
    headquarters: str
    core_business: str


class StructuredResearchReport(BaseModel):

    executive_summary: list[str] = Field(
        default_factory=list
    )

    company_overview: CompanyOverview

    recent_developments: list[
        RecentDevelopment
    ] = Field(
        default_factory=list
    )

    business_signals: list[
        BusinessSignal
    ] = Field(
        default_factory=list
    )

    potential_pain_points: list[
        PainPoint
    ] = Field(
        default_factory=list
    )

    potential_opportunities: list[
        Opportunity
    ] = Field(
        default_factory=list
    )

    risks_and_unknowns: list[
        Risk
    ] = Field(
        default_factory=list
    )

    recommended_next_actions: list[
        NextAction
    ] = Field(
        default_factory=list
    )


# ============================================================
# DATABASE / API RESPONSE
# ============================================================

class SourceResponse(BaseModel):
    id: int
    url: str
    title: str | None
    report_id: int

    model_config = {
        "from_attributes": True
    }


class ResearchResponse(BaseModel):
    id: int
    company_name: str
    report_content: str
    user_id: int
    created_at: datetime
    sources: list[SourceResponse] = Field(
        default_factory=list
    )

    model_config = {
        "from_attributes": True
    }