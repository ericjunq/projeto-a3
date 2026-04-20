from dependencies import get_db
from models import Prefeitura, Usuario
from schemas import PrefeituraSchema, UsuarioSchema, UsuarioResponse, PrefeituraResponse, UsuarioUpdate, PrefeituraUpdate
from fastapi import Depends, HTTPException, APIRouter
from security.security import get_current_prefeitura, get_current_user, criptografar_senha, verificar_senha, criar_access_token, criar_refresh_token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# Usuarios
@auth_router.post('/cadastrar_usuario', response_model=UsuarioResponse)
async def cadastrar_usuasrio(
    usuarioschema: UsuarioSchema,
    db: Session = Depends(get_db)
):
    email_existente = db.query(Usuario).filter(
        Usuario.email == usuarioschema.email
        ).first()
    if email_existente:
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    
    telefone_existente = db.query(Usuario).filter(
        Usuario.telefone == usuarioschema.telefone
    ).first()

    if telefone_existente:
        raise HTTPException(status_code=400, detail='Telefone já existente')
    
    cpf_existente = db.query(Usuario).filter(
        Usuario.cpf == usuarioschema.cpf
    ).first()

    if cpf_existente:
        raise HTTPException(status_code=400, detail='CPF já cadastrado')
    
    senha_criptografada = criptografar_senha(usuarioschema.senha)

    usuario = Usuario(
        nome = usuarioschema.nome,
        sobrenome = usuarioschema.sobrenome,
        email = usuarioschema.email,
        senha_hash = senha_criptografada,
        telefone = usuarioschema.telefone,
        cpf = usuarioschema.cpf
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    return usuario

@auth_router.post('/login_usuario')
async def login_usuario(
    dados: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.username
    ).first()

    if usuario is None:
        raise HTTPException(status_code=404, detail='Email não encontrado')
    
    if not verificar_senha(dados.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    access_token = criar_access_token(
        data = {'sub': dados.username, 'type': 'access', 'origin': 'usuario'}
    )
    
    refresh_token = criar_refresh_token(
        data = {'sub': dados.username, 'type': 'refresh', 'origin': 'usuario'}
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@auth_router.patch('/editar_usuario', response_model=UsuarioResponse)
async def editar_usuario(
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario: Session = Depends(get_current_user)
):
    dados_update = dados.dict(exclude_unset=True)

    if 'email' in dados_update:
        email_existente = db.query(Usuario).filter(
            Usuario.email == dados_update['email']
        ).first()
        if email_existente:
            raise HTTPException(status_code=400, detail='Email já cadastrado')
    
    if 'telefone' in dados_update:
        telefone_existente = db.query(Usuario).filter(
            Usuario.telefone == dados_update['telefone']
        ).first()
        if telefone_existente:
            raise HTTPException(status_code=400, detail='Telefone já cadastrado')
    
    if 'senha' in dados_update:
        dados_update['senha_hash'] = criptografar_senha(dados_update.pop('senha'))

    for campo, valor in dados_update.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario