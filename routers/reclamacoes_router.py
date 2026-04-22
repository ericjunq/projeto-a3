from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path
import shutil

from dependencies import get_db
from models import Usuario, Reclamacao
from schemas import ReclaamacaoResponse, StatusReclamacao
from security.security import get_current_user

reclamacoes_router = APIRouter(prefix='/reclamacoes', tags=['Reclamações'])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@reclamacoes_router.post('/criar', response_model=ReclaamacaoResponse)
async def criar_reclamacao(
    titulo: str = Form(...),
    descricao: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail='Arquivo inválido: Envie jpeg, png, webp ou gif.'
        )
    
    destino = UPLOAD_DIR / file.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        reclamacao = Reclamacao(
        titulo=titulo,
        descricao=descricao,
        status=StatusReclamacao.em_andamento,
        imagem_url=str(destino),
        usuario_id=usuario.id

        )

        db.add(reclamacao)
        db.commit()
        db.refresh(reclamacao)
    

    return reclamacao

@reclamacoes_router.get('/minhas', response_model=list[ReclaamacaoResponse])
async def listar_minhas_reclamacoes(
    status: Optional[StatusReclamacao] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    
    query = db.query(Reclamacao).filter(Reclamacao.usuario_id == usuario.id)
 
    if status:
        query = query.filter(Reclamacao.status == status)
 
    return query.order_by(Reclamacao.created_at.desc()).all()


@reclamacoes_router.get('minhas/{reclamacao_id}', response_model=ReclaamacaoResponse)
async def detalhar_reclamacao(
    reclamacao_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    reclamacao = db.query(Reclamacao).filter(
        Reclamacao.id == reclamacao_id,
        Reclamacao.usuario_id == usuario.id
    ).filter()

    if not reclamacao:
        raise HTTPException(status_code=404, detail='Reclamação não encontrada')
    
    return reclamacao
    