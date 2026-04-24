from pydantic import BaseModel, EmailStr
from security.validations import CPF, Telefone, CNPJ
from datetime import datetime
from typing import Optional
from enum import Enum
from enums import TipoRequestEnum, StatusReclamacao

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


# Reclamações Eric

class ReclamacaoResponse(BaseModel):
    id: int
    tipo: TipoRequestEnum
    titulo: str
    bairro: str
    rua: str
    numero: int
    descricao: str
    status: StatusReclamacao
    imagem_url: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_atributes = True