from security.token_autenticador import gerar_token
from database import LocalSession

def main():
    db = LocalSession()
    try: 
        token_puro = gerar_token(db)
        print("=" * 60)
        print("✅ Token gerado e salvo no banco!")
        print(f"\n🔑 TOKEN (envie ao cliente):\n   {token_puro}")
        print(f"\n🔗 Link:\n   # a decidir")
        print("=" * 60)
    finally:
        db.close()

if __name__ == "__main__":
    main()