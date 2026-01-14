"""
File processing service - handles .py and .zip uploads.
"""
import zipfile
import tempfile
import os
from typing import List, Dict, Tuple
from fastapi import UploadFile


class FileProcessor:
    """Handles file uploads and extracts Python code."""
    
    async def process_upload(self, file: UploadFile) -> List[Dict[str, str]]:
        """Process uploaded file and return list of {filename, content}."""
        if file.filename.lower().endswith(".zip"):
            return await self._process_zip(file)
        return await self._process_py(file)
    
    async def _process_py(self, file: UploadFile) -> List[Dict[str, str]]:
        """Process single .py file."""
        content = await file.read()
        text = content.decode("utf-8", errors="replace")
        return [{"filename": file.filename, "content": text}]
    
    async def _process_zip(self, file: UploadFile) -> List[Dict[str, str]]:
        """Extract .py files from zip."""
        files = []
        content = await file.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            with zipfile.ZipFile(tmp_path, "r") as zf:
                for name in zf.namelist():
                    if not name.endswith(".py") or "__pycache__" in name:
                        continue
                    try:
                        data = zf.read(name).decode("utf-8", errors="replace")
                        files.append({"filename": name, "content": data})
                    except:
                        continue
        finally:
            os.unlink(tmp_path)
        
        return files
    
    def validate_file(self, file: UploadFile) -> Tuple[bool, str]:
        """Check if file is .py or .zip."""
        name = file.filename.lower()
        if name.endswith(".py") or name.endswith(".zip"):
            return True, ""
        return False, "Only .py and .zip files allowed"
