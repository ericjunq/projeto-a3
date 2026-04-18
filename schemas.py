from pydantic import BaseModel, EmailStr
from security.validations import CPF, Telefone
from datetime import datetime
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str 
    sobrenome: str 
    email: EmailStr
    senha: str
    telefone: Telefone
    cpf: CPF
    token_autenticador = Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[Telefone] = None