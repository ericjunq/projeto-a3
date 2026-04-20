from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pathlib import Path
import shutil


router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@router.post("/upload")
async def upload_image(
    tipo: str = Form(...),
    descricao: str = Form(...),
    file: UploadFile = File(...),
):
 if file.content_type not in ALLOWED_TYPES:
  raise HTTPException(
   status_code=400,
   detail=f"Arquivo Inválido: {file.content_type}"
  )
 
 destinacao = UPLOAD_DIR / file.filename
 with destinacao.open("wb") as buffer:
  shutil.copyfileobj(file.file, buffer)

  return {
   "tipo": tipo,
   "descricao": descricao,
   "arquivo": str(destinacao),
   "content_type": file.conteent_type,
  }