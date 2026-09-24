from datetime import datetime

from pydantic import BaseModel


class ResearchRequest(BaseModel):
    company_name: str


class ResearchResponse(BaseModel):
    id: int
    company_name: str
    report_content: str
    user_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }