from dependencies import get_db
from models import Prefeitura, TokenAutenticador, RefreshToken
from schemas import PrefeituraSchema, UsuarioSchema, UsuarioResponse, PrefeituraResponse, UsuarioUpdate, PrefeituraUpdate
from fastapi import Depends, HTTPException, APIRouter
from security.security import get_current_prefeitura, get_current_user, criptografar_senha, verificar_senha, criar_access_token, criar_refresh_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone


router = APIRouter(prefix='/prefeitura', tags=['Prefeitura'])

@router.post('/cadastrar_prefeitura', response_model=PrefeituraResponse)
async def cadastrar_prefeitura(
    prefeituraschema: PrefeituraSchema,
    db: Session = Depends(get_db)
):
    email_existente = db.query(Prefeitura).filter(
        Prefeitura.email == prefeituraschema.email
    ).first()
    if email_existente:
        raise HTTPException(status_code=409, detail='Email já cadastrado')
    
    cnpj_existente = db.query(Prefeitura).filter(
        Prefeitura.cnpj == prefeituraschema.cnpj
    ).first()
    if cnpj_existente:
        raise HTTPException(status_code=409, detail='CNPJ já cadastrado')
    
    telefone_existente = db.query(Prefeitura).filter(
        Prefeitura.telefone == prefeituraschema.telefone
    ).first()
    if telefone_existente:
        raise HTTPException(status_code=409, detail='Telefone já cadastrado')
    
    token = db.query(TokenAutenticador).filter(
        TokenAutenticador.token == prefeituraschema.token_autenticador
    ).first()
    if token is None:
        raise HTTPException(status_code=404, detail='Token de autenticação inválido')
    
    if token.usado:
        raise HTTPException(status_code=400, detail='Token de autenticação já utilizado')
    
    if token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail='Token de autenticação expirado')

    prefeitura = Prefeitura(
        cidade=prefeituraschema.cidade,
        email=prefeituraschema.email,
        senha_hash=criptografar_senha(prefeituraschema.senha),
        telefone=prefeituraschema.telefone,
        cnpj=prefeituraschema.cnpj,
        token_valor=token.token,
        token_id=token.id
    )

    db.add(prefeitura)
    db.commit()
    db.refresh(prefeitura)

    token.usado = True
    token.prefeitura_id = prefeitura.id
    db.commit()

    return prefeitura

@router.post('/login_prefeitura')
async def login_prefeitura(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    prefeitura = db.query(Prefeitura).filter(
        Prefeitura.email == form_data.username
    ).first()

    if not prefeitura:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos')
    
    if not verificar_senha(form_data.password, prefeitura.senha_hash):
        raise HTTPException(status_code=401, detail='Email ou senha incorretos')
    
    access_token = criar_access_token(
        data={"sub": prefeitura.id, 'origin': 'prefeitura'}
    )
    
    refresh_token, expires, jti = criar_refresh_token(
        data={"sub": prefeitura.id, 'origin': 'prefeitura'}
    )

    refresh_token_obj = RefreshToken(
        jti=jti,
        token_hash=criptografar_senha(refresh_token),
        prefeitura_id=prefeitura.id,
        expires_at=expires
    )
    db.add(refresh_token_obj)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }