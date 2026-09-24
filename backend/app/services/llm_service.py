from typing import Any

from langchain_groq import ChatGroq

from app.config import settings


class LLMService:

    def __init__(self):

        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model="openai/gpt-oss-20b",
            temperature=0,
        )

    async def generate_research(
        self,
        company_data: dict[str, Any],
        evidence: list[dict[str, Any]],
    ) -> str:

        # ==================================================
        # 1. COMPANY INFORMATION
        # ==================================================

        company_name = company_data.get(
            "Name",
            "Unknown",
        )

        symbol = company_data.get(
            "Symbol",
            "Unknown",
        )

        sector = company_data.get(
            "Sector",
            "Unknown",
        )

        industry = company_data.get(
            "Industry",
            "Unknown",
        )

        description = company_data.get(
            "Description",
            "No description available.",
        )

        headquarters = company_data.get(
            "Address",
            "Unknown",
        )

        # ==================================================
        # 2. BUILD EVIDENCE TEXT
        # ==================================================

        evidence_text = ""

        for index, item in enumerate(
            evidence,
            start=1,
        ):

            evidence_text += f"""
==================================================
Evidence {index}
==================================================

Type:
{item.get("type", "unknown")}

Title:
{item.get("title", "Unknown")}

Source:
{item.get("source", "Unknown")}

Published:
{item.get("published_at", "Unknown")}

URL:
{item.get("url", "")}

Content:
{item.get("content", "")}

"""

        # ==================================================
        # 3. PROMPT
        # ==================================================

        prompt = f"""
You are an enterprise research analyst.

Your job is to create a concise, evidence-backed
research brief for a sales and research team.

The user wants research about:

{company_name}

IMPORTANT RULES:

1. Use ONLY the company information and research
   evidence provided below.

2. Do NOT invent facts.

3. Do NOT assume that an opportunity, risk, or business
   problem is certain.

4. Clearly distinguish facts from analysis.

5. If there is insufficient evidence for a claim,
   explicitly say:
   "Insufficient evidence."

6. Do not create fake sources.

7. Do not create fake URLs.

8. Only reference URLs that are present in the
   supplied evidence.

9. If two sources disagree, explicitly mention
   the conflict.

10. Do not treat speculation from an article as
    an established fact.

11. Keep the report useful for a sales/research team.

12. Do not make unsupported financial predictions.

13. For political or regulatory topics, describe
    documented information neutrally.

14. Do not infer motives that are not supported
    by the supplied evidence.

15. Use recent evidence where available.

--------------------------------------------------
COMPANY INFORMATION
--------------------------------------------------

Company:
{company_name}

Ticker:
{symbol}

Sector:
{sector}

Industry:
{industry}

Headquarters:
{headquarters}

Description:
{description}

--------------------------------------------------
RESEARCH EVIDENCE
--------------------------------------------------

{evidence_text}

--------------------------------------------------
OUTPUT FORMAT
--------------------------------------------------

Create the research brief using exactly these sections:

# Research Brief – {company_name}

## 1. Executive Summary

Provide a concise summary of the most important
evidence-backed findings.

## 2. Company Overview

Include:

- Company
- Ticker
- Sector
- Industry
- Headquarters
- Core business

Only use information available in the company data
or supplied evidence.

## 3. Recent Developments

For each important development include:

- Development
- Date
- Source
- Evidence
- Business relevance

Do not present an unverified claim as a confirmed fact.

## 4. Business Signals

Identify important signals such as:

- Growth signals
- Technology signals
- Market signals
- Supply-chain signals
- Regulatory signals
- Competitive signals

For every signal explain the evidence supporting it.

## 5. Potential Customer Pain Points

Identify potential business problems that could matter
to customers.

Clearly distinguish documented problems from analytical
possibilities.

Use the word "Potential" when the conclusion is based
on analysis rather than directly documented evidence.

## 6. Potential Opportunities

Identify potential opportunities for a sales/research team.

For each opportunity provide:

- Opportunity
- Evidence
- Why it may matter
- Suggested next step

Do NOT state that an opportunity is guaranteed.

## 7. Risks and Unknowns

Include:

- Known risks supported by evidence
- Conflicting information
- Missing information
- Important uncertainties

## 8. Recommended Next Actions

Provide practical research/sales actions based on
the available evidence.

Do not invent information that is not supported
by the evidence.

## 9. Sources

List the sources used.

For each source include:

- Title
- Source
- URL
- Published date

Only include URLs supplied in the evidence.

--------------------------------------------------
QUALITY REQUIREMENTS
--------------------------------------------------

The final report must be:

- Evidence-backed
- Concise
- Business-focused
- Clear
- Structured
- Neutral
- Explicit about uncertainty

Never fabricate evidence, sources, URLs, dates,
companies, products, competitors, financial figures,
or events.

Return ONLY the research brief.
"""

        # ==================================================
        # 4. CALL GROQ
        # ==================================================

        try:

            response = await self.llm.ainvoke(
                prompt
            )

        except Exception as error:

            raise ValueError(
                f"Groq LLM request failed: {error}"
            ) from error

        # ==================================================
        # 5. EXTRACT RESPONSE CONTENT
        # ==================================================

        content = response.content

        # --------------------------------------------------
        # LangChain can sometimes return structured content
        # as a list instead of a plain string.
        # --------------------------------------------------

        if isinstance(content, list):

            text_parts = []

            for item in content:

                if isinstance(item, str):

                    text_parts.append(item)

                elif isinstance(item, dict):

                    text = item.get(
                        "text",
                        "",
                    )

                    if text:

                        text_parts.append(
                            str(text)
                        )

            content = "\n".join(
                text_parts
            )

        # --------------------------------------------------
        # Convert to string
        # --------------------------------------------------

        if content is None:

            content = ""

        content = str(content).strip()

        # ==================================================
        # 6. VALIDATE RESPONSE
        # ==================================================

        if not content:

            metadata = getattr(
                response,
                "response_metadata",
                {},
            )

            additional_kwargs = getattr(
                response,
                "additional_kwargs",
                {},
            )

            raise ValueError(
                "Groq returned an empty response. "
                f"Metadata: {metadata}. "
                f"Additional kwargs: {additional_kwargs}"
            )

        # ==================================================
        # 7. RETURN FINAL REPORT
        # ==================================================

        return content
