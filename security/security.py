from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from security.settings import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from dependencies import get_db
from sqlalchemy.orm import Session
from models import Usuario, Prefeitura

passoword_hash = PasswordHash.recommended()

user_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login_usuario')
prefeitura_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login_prefeitura')

def criptografar_senha(senha: str)-> str:
    return passoword_hash.hash(senha)

def verificar_senha(senha: str, senha_hash: str)-> bool:
    return passoword_hash.verify(senha, senha_hash)

def criar_access_token(data: dict)-> str:
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({'exp': expires})

    access_token = jwt.encode(
        to_encode,
        settings.secret_key,
        settings.algorithm
    )

    return access_token

def criar_refresh_token(data: dict)->str:
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expires_days)
    to_encode.update({'exp': expires})

    refresh_token = jwt.encode(
        to_encode,
        settings.secret_key,
        settings.algorithm
    )

    return refresh_token

def get_current_user(
        token: str = Depends(user_scheme), 
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key,
            [settings.algorithm]
        )
        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise HTTPException(status_code=400, detail='Usuario não encontrado')
    
    return usuario

def get_current_prefeitura(
        token: str = Depends(prefeitura_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            [settings.algorithm]
        )
        email = payload.get('sub')  # corrigido: era 'email'
        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    prefeitura = db.query(Prefeitura).filter(Prefeitura.email == email).first()
    if prefeitura is None:
        raise HTTPException(status_code=400, detail='Prefeitura não encontrada')

    return prefeitura