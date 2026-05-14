from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from dependencies import get_db
from models import RefreshToken
from security.security import criar_access_token, verificar_senha, criar_refresh_token, criptografar_senha
from security.settings import settings
from jose import jwt, JWTError
from datetime import datetime, timezone

router = APIRouter(prefix='/refresh_token', tags=['refresh_token'])


def _processar_refresh_token(
    refresh_token: str,
    origin: str,
    entity_id: str,
    jti: str,
    db: Session
) -> dict:
    filtro = (
        RefreshToken.usuario_id == entity_id
        if origin == 'usuario'
        else RefreshToken.prefeitura_id == entity_id
    )

    token_db = db.query(RefreshToken).filter(filtro).first()
    if token_db is None:
        raise HTTPException(status_code=400, detail='Entidade não encontrada')

    if token_db.revoked:
        db.query(RefreshToken).filter(filtro, RefreshToken.revoked.is_(False)).update(
            {'revoked': True}, synchronize_session=False
        )
        db.commit()
        raise HTTPException(status_code=401, detail='Sessão comprometida, faça login novamente')

    if not verificar_senha(refresh_token, token_db.token_hash):
        raise HTTPException(status_code=401, detail='Token inválido')

    if token_db.jti != jti:
        raise HTTPException(status_code=401, detail='Token inválido')

    agora = datetime.now(timezone.utc)
    if token_db.expires_at <= agora:
        raise HTTPException(status_code=401, detail='Token expirado, faça login novamente')

    token_db.revoked = True
    db.commit()

    novo_access_token = criar_access_token(data={"sub": entity_id, "origin": origin})
    novo_refresh_token, expires, novo_jti = criar_refresh_token(data={"sub": entity_id, "origin": origin})

    novo_token_obj = RefreshToken(
        jti=novo_jti,
        token_hash=criptografar_senha(novo_refresh_token),
        expires_at=expires,
        **({'usuario_id': entity_id} if origin == 'usuario' else {'prefeitura_id': entity_id})
    )
    db.add(novo_token_obj)
    db.commit()

    return {
        'access_token': novo_access_token,
        'refresh_token': novo_refresh_token,
        'token_type': 'bearer'
    }


@router.post('/')
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": False}
        )

        if payload.get('token_type') != 'refresh':
            raise HTTPException(status_code=400, detail='Token inválido')

        agora = datetime.now(timezone.utc)
        if payload.get('exp') is None or payload['exp'] <= agora.timestamp():
            raise HTTPException(status_code=401, detail='Token expirado, faça login novamente')

        origin = payload.get('origin')
        entity_id = payload.get('sub')
        jti = payload.get('jti')

        if origin not in ('usuario', 'prefeitura') or entity_id is None or jti is None:
            raise HTTPException(status_code=401, detail='Token inválido')

        return _processar_refresh_token(refresh_token, origin, entity_id, jti, db)

    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')