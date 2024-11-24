
# EpiAlert System - Back-End

## Descrição do Projeto

O EpiAlert System é uma aplicação desenvolvida para monitorar e emitir alertas de epidemias. Este repositório contém o back-end da aplicação, construído utilizando o framework Django. O sistema oferece suporte para autenticação de usuários, consumo de APIs externas de dados de saúde, e geração de endpoints para alimentar o front-end do projeto. O banco de dados utilizado é o SQLite, ideal para o desenvolvimento inicial do MVP.

## Instruções de como executar a aplicação

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/samelakaroline/epialert-django.git
   cd epialert-django
   ```

2. **Crie e ative um ambiente virtual Python:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências do projeto:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crie um superusuário para acessar o admin do Django:**

   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento:**

   ```bash
   python manage.py runserver
   ```

7. **Acesse o sistema:**

   Abra o navegador e acesse [http://127.0.0.1:8000](http://127.0.0.1:8000) para visualizar a aplicação.

## Tecnologias Utilizadas

- **Python 3.12**;
- **Django 4.x**;
- **SQLite**;
- **APIs externas de dados de saúde** (como [Disease.sh](https://disease.sh) e dados do Ministério da Saúde do Brasil).

## Funcionalidades

- Autenticação de usuários;
- Consumo e processamento de dados de APIs externas;
- Geração de endpoints para o front-end;
- Integração com o banco de dados SQLite.

## Estrutura do Projeto

```plaintext
epialert-django/
├── epialert/         # Diretório principal da aplicação
├── users/            # Módulo dos usuários
├── dashboards/       # Módulo para geração dos dashboards
├── alerts            # Módulo para criação dos alertas
├── db.sqlite3        # Banco de dados SQLite
├── manage.py         # Script principal do Django
└── requirements.txt  # Dependências do projeto
```

## Contribuição

Este projeto ainda está em fase inicial de desenvolvimento. Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.
