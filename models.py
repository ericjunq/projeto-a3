from database import Base
from sqlalchemy import Column, func, Integer, Boolean, String, DateTime

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(20), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(11), unique=True, nullable=False)
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