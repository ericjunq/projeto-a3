from database import Base
from sqlalchemy import Column, func, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(11),unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
        )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
        )
    status = Column(Boolean, default=True)
    
class Prefeitura(Base):
    __tablename__ = 'prefeitura'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(11), unique=True, nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    token_autenticador = Column(String, ForeignKey('tokens_autenticadores.token'))
    token_id = Column(Integer, ForeignKey('tokens_autenticadores.id'),nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
        )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
        )
    status = Column(Boolean, default=True)

    token_autenticador = relationship('TokenAutenticador', back_populates='prefeitura')

class TokenAutenticador(Base):
    __tablename__ = 'tokens_autenticadores'

    id = Column(Integer, autoincrement=True, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    usado = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    prefeitura = relationship('Prefeitura', back_populates='token_autenticador')
