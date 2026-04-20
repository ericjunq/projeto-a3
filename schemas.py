from pydantic import BaseModel, EmailStr
from security.validations import CPF, Telefone, CNPJ
from datetime import datetime
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str 
    sobrenome: str 
    email: EmailStr
    senha: str
    telefone: Telefone
    cpf: CPF

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    sobrenome: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[Telefone] = None

class PrefeituraSchema(BaseModel):
    cidade: str 
    email: EmailStr
    senha: str 
    telefone: Telefone
    cnpj: CNPJ
    token_autenticador: str

class PrefeituraResponse(BaseModel):
    id: int
    cidade: str
    telefone: Telefone
    cnpj: CNPJ
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PrefeituraUpdate(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[Telefone] = None
