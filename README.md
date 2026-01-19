
# Shipay User CRUD

Uma API REST simples para gerenciar usuários.

Este projeto é norteado pelos padrões da arquitetura hexagonal juntamente com princípios do DDD.

## 🚀 Recursos

- ✅ Criar usuários
- ✅ Listar usuários
- ✅ Atualizar usuários
- ✅ Deletar usuários
- ✅ Criar papéis(roles)
- ✅ Listar papéis(roles)

## 📋 Pré-requisitos

- python 3.13
- poetry

## 🛠️ Instalação
Este projeto utiliza [Poetry](https://python-poetry.org/) para gerenciamento de dependências.
```bash
# Instale as dependências
poetry install

# Ative o ambiente virtual (opcional, mas recomendado para desenvolvimento)
poetry shell
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
