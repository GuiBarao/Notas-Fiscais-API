

<h1>API do sistema de notas fiscais</h1> 

![Python](https://img.shields.io/badge/Python-3.11.5-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-brightgreen?style=for-the-badge&logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-0.34.3-informational?style=for-the-badge&logo=uvicorn&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.41-darkred?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-1.16.2-9cf?style=for-the-badge&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0.42-blue?style=for-the-badge&logo=mysql&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-2.1.3-6f42c1?style=for-the-badge&logo=poetry&logoColor=white)
## Descrição do projeto
Este sistema fornece uma API para acessar dados de notas fiscais eletrônicas.

## Intruções para rodar localmente

- Instale localmente o python em uma versão igual ou superior a 3.11. Download disponível no <a href = https://www.python.org/downloads/ > link oficial </a>.

- Instale localmente o MySQL na versão 8.0.*. Download disponível no <a href = https://dev.mysql.com/downloads/installer/ > link oficial </a>.
  - Crie um banco de dados para armazenar os usuários do sistema. 
  
- Clone o projeto.

- Edite as insformações do arquivo .env_exemplo de acordo com seu ambiente.
  
- No diretório do projeto execute <strong> pip install poetry==2.1.3 </strong> para instalar o gerenciador de dependências deste sistema.
  - OBS: Poetry deve ser instalado globalmente (sem ambiente virtual).

- Execute <strong> poetry install </strong> para instalar as dependências.

- Execute <strong> alembic head upgrade </strong> para rodar as migrações de banco de dados.
  - Cria a tabela de banco de dados "usuarios" para gerenciar os usuários do sistema.
  - OBS: As migrações só irão funcionar se o arquivo .env estiver com a string de conexão com o banco de dados correta.

- Execute <strong> poetry run uvicorn src.myapp.main:app </strong> para rodar localmente a API.
  - Ela fica por padrão disponível no host local e na porta 8000. 


## Obervações adicionais

O sistema possui gerenciamento de usuários. Logo todos os endpoints exceto o de login são protegidos por token que deve ser informado no header das requisições protegidas.

O FastAPI gera automaticamente a documentação dos endpoints da API. Com o servidor rodando basta acessar <strong>/docs</strong> na API que ela renderiza a interface do Swagger.


