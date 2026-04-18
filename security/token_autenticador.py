import secrets
import hashlib
from dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import TokenAutenticador

def gerar_token():
    token = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    return token, token_hash

def criar_token(db: Session):
    token_autenticador, token_autenticador_hash = gerar_token()
    token_obj = TokenAutenticador(token=token_autenticador_hash)

    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)

    return token_autenticador