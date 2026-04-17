import re
from pydantic import AfterValidator
from typing import Annotated

def validar_telefone(telefone: str) -> bool:
    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    if re.match(padrao, telefone):
        return True
    return False

def validar_cpf(cpf: str) -> bool:
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    total = sum(int(cpf[i]) * (10 - i) for i in range(9))
    remainder = (total * 10) % 11
    if remainder == 10:
        remainder = 0
    if remainder != int(cpf[9]):
        return False
    total = sum(int(cpf[i]) * (11 - i) for i in range(10))
    remainder = (total * 10) % 11
    if remainder == 10:
        remainder = 0
    if remainder != int(cpf[10]):
        return False
    return True


# --- Checadores (levantam erro se inválido) ---

def checar_cpf(v: str) -> str:
    if not validar_cpf(v):
        raise ValueError('CPF inválido')
    return v

def checar_telefone(v: str) -> str:
    if not validar_telefone(v):
        raise ValueError('Telefone inválido')
    return v

# --- Tipos reutilizáveis ---

CPF = Annotated[str, AfterValidator(checar_cpf)]
Telefone = Annotated[str, AfterValidator(checar_telefone)]