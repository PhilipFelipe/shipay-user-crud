
# Shipay User CRUD

Uma API REST simples para gerenciar usuários.

## 🚀 Recursos

- ✅ Criar usuários
- ✅ Listar usuários
- ✅ Atualizar usuários
- ✅ Deletar usuários
- ✅ Criar papéis(roles)
- ✅ Listar papéis(roles)

## 📋 Pré-requisitos

- python 3.13
- uv ou pip

## 🛠️ Instalação

```bash
# Utilizando o "uv"
uv python install 3.13 
# vincula a versão do python ao projeto
uv python pin 3.13 
# Cria e ativa a venv
uv venv
# Instala as dependências do projeto
uv sync

# Utilizando pip
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt  # ambiente local
```

## ▶️ Rodar servidor
Ao rodar o servidor, um database users.db é criado com sqlite3.
```bash
# alias do taskpy
task run
```

## 🧪 Rodar testes
Rodar os testes cria um database à parte chamado test.db
```bash
task test
```

## 🧹 Formatando o código
```bash
task format
```


## 📚 Documentação
http://127.0.0.1:8000/docs

http://127.0.0.1:8000/redoc
