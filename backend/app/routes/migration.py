"""
API routes for migration analysis - Simplified.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from bson import ObjectId

from ..models.report import AnalysisResponse, MigrationReport
from ..models.user import UserInDB
from ..services.file_processor import FileProcessor
from ..services.llm_analyzer import LLMAnalyzer
from ..services.auth import get_current_user
from ..database.mongodb import reports_collection

router = APIRouter(prefix="/api/migration", tags=["migration"])

# Services
file_processor = FileProcessor()
llm_analyzer = LLMAnalyzer()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Analyze Python files for Python 3 compatibility using LangChain + Gemini.
    Upload a .py file or .zip archive.
    """
    # Validate
    is_valid, error = file_processor.validate_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    try:
        # Process files
        files = await file_processor.process_upload(file)
        if not files:
            raise HTTPException(status_code=400, detail="No Python files found")
        
        # Analyze with LangChain + Gemini
        result = await llm_analyzer.analyze(files)
        
        # Create and store report
        report = MigrationReport(
            is_valid_python3=result.is_valid_python3,
            files_analyzed=result.files_analyzed,
            issues=result.issues,
            summary=result.summary
        )
        
        report_dict = report.model_dump(by_alias=True, exclude={"id"})
        db_result = await reports_collection().insert_one(report_dict)
        report_id = str(db_result.inserted_id)
        
        status = "✅ Valid Python 3" if result.is_valid_python3 else f"⚠️ Found {len(result.issues)} issues"
        return AnalysisResponse(report_id=report_id, message=status)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")


@router.get("/report/{report_id}")
async def get_report(report_id: str, current_user: UserInDB = Depends(get_current_user)):
    """Get a report by ID."""
    try:
        obj_id = ObjectId(report_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid report ID")
    
    report = await reports_collection().find_one({"_id": obj_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    report["id"] = str(report.pop("_id"))
    return report


@router.get("/reports")
async def list_reports(limit: int = 10, current_user: UserInDB = Depends(get_current_user)):
    """List recent reports."""
    cursor = reports_collection().find().sort("created_at", -1).limit(limit)
    reports = []
    async for r in cursor:
        reports.append({
            "id": str(r["_id"]),
            "files_analyzed": r.get("files_analyzed", []),
            "is_valid_python3": r.get("is_valid_python3"),
            "issues_count": len(r.get("issues", [])),
            "created_at": r.get("created_at")
        })
    return {"reports": reports}


@router.delete("/report/{report_id}")
async def delete_report(report_id: str, current_user: UserInDB = Depends(get_current_user)):
    """Delete a report."""
    try:
        obj_id = ObjectId(report_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid report ID")
    
    result = await reports_collection().delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": "Deleted"}
