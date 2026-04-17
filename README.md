# BACKEND A3

## 📁 Estrutura Backend Profissional

```
backend/
│── app/
│   │── main.py                 🔹 Pessoa 1
│   │── database.py             🔹 Pessoa 1
│   │── config.py               🔹 Pessoa 1
│   │
│   ├── models/
│   │     ├── user.py           🔹 Pessoa 1
│   │     ├── complaint.py      🔸 Pessoa 2
│   │
│   ├── schemas/
│   │     ├── user.py           🔹 Pessoa 1
│   │     ├── complaint.py      🔸 Pessoa 2
│   │
│   ├── routes/
│   │     ├── auth.py           🔹 Pessoa 1
│   │     ├── users.py          🔹 Pessoa 1
│   │     ├── complaints.py     🔸 Pessoa 2
│   │     ├── upload.py         🔸 Pessoa 2
│   │
│   ├── services/
│   │     ├── auth_service.py   🔹 Pessoa 1
│   │
│   ├── uploads/                🔸 Pessoa 2
│   │     ├── imagens aqui
│
│── requirements.txt            🔹 Pessoa 1
│── .env                        🔹 Pessoa 1
│── README.md                   🔸 Pessoa 2
```

## 🚀 Rodar Projeto
```
uvicorn main:app --reload
```
## 🌐 Testar
```
http://127.0.0.1:8000/docs
```


## 🟠 GIT
### 👨‍💻 Para adicionar seus arquivos:
```
git add .
git commit -m "suas alteracoes"
git push origin main
```

### Pegar as alteraçõs feitas por outros:
```
git pull origin main
```
