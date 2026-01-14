"""
LLM Analyzer using LangChain + Gemini to check Python 3 compatibility.
"""
import json
from typing import List, Dict, Any, Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from ..config import settings
from ..models.report import AnalysisResult, Severity


# Pydantic model for structured LLM output
class CodeIssue(BaseModel):
    issue: str = Field(description="Description of the issue found")
    severity: str = Field(description="high, medium, or low")
    line_hint: str = Field(description="Code snippet or line reference")
    fix: str = Field(description="How to fix this issue")


class AnalysisOutput(BaseModel):
    is_valid_python3: bool = Field(description="True if code is valid Python 3")
    issues: List[CodeIssue] = Field(description="List of issues found")
    summary: str = Field(description="Brief summary of code quality")


# Use a strict parser so Gemini is forced into the schema
_OUTPUT_PARSER = PydanticOutputParser(pydantic_object=AnalysisOutput)

ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert Python developer with deep knowledge of Python 2 and Python 3 differences.

Analyze the provided Python code and identify any Python 2 syntax/functions/patterns that are incompatible with Python 3.

Return ONLY a JSON object (no markdown, no code fences), following the provided schema."""),
    ("human", """{format_instructions}

Here is the code:

{code}
"""),
]).partial(format_instructions=_OUTPUT_PARSER.get_format_instructions())


class LLMAnalyzer:
    """Analyzes Python code using LangChain + Gemini."""

    def __init__(self):
        self.llm = None
        self.chain = None
        self.enabled = False

        if not settings.GEMINI_API_KEY:
            print("No GEMINI_API_KEY found - LLM analyzer disabled")
            return

        try:
            # Use a valid Gemini model name
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0,
            )
            self.chain = ANALYSIS_PROMPT | self.llm | _OUTPUT_PARSER
            self.enabled = True
            print("LLM Analyzer initialized with Gemini API")
        except Exception as e:
            print(f"Failed to initialize LLM: {e}")
            self.enabled = False

    def _get_file_fields(self, f: Dict[str, Any]) -> Optional[tuple[str, str]]:
        """Tolerate different frontend payload shapes."""
        filename = f.get("filename") or f.get("name") or f.get("fileName")
        content = f.get("content") or f.get("text") or f.get("source")
        if not filename or content is None:
            return None
        return filename, content

    async def analyze(self, files: List[Dict[str, Any]]) -> AnalysisResult:
        """Analyze uploaded Python files for Python 2 vs Python 3 compatibility."""
        code_parts: List[str] = []

        for f in files[:10]:
            fields = self._get_file_fields(f)
            if not fields:
                continue
            filename, content = fields

            if len(content) > 5000:
                content = content[:5000] + "\n# ... (file truncated)"
            code_parts.append(f"# === File: {filename} ===\n{content}")

        combined_code = "\n\n".join(code_parts)

        if not self.enabled:
            raise ValueError("LLM analyzer is not configured. Please set GEMINI_API_KEY.")

        print(f"Sending {len(combined_code)} chars to LLM for analysis...")
        parsed: AnalysisOutput = await self.chain.ainvoke({"code": combined_code})
        return self._parse_result(parsed, files)

    def _parse_result(self, result: AnalysisOutput, files: List[Dict[str, Any]]) -> AnalysisResult:
        """Convert LLM response to AnalysisResult."""
        severity_map = {
            "high": Severity.HIGH,
            "medium": Severity.MEDIUM,
            "low": Severity.LOW,
        }

        issues = []
        for item in result.issues:
            sev_enum = severity_map.get(item.severity.lower(), Severity.MEDIUM)
            issues.append({
                "issue": item.issue,
                # Ensure JSON-friendly output for the frontend
                "severity": sev_enum.value if hasattr(sev_enum, "value") else str(sev_enum),
                "line_hint": item.line_hint,
                "fix": item.fix,
            })

        files_analyzed = []
        for f in files:
            fields = self._get_file_fields(f)
            if fields:
                files_analyzed.append(fields[0])

        return AnalysisResult(
            is_valid_python3=result.is_valid_python3,
            files_analyzed=files_analyzed,
            issues=issues,
            summary=result.summary,
        )
