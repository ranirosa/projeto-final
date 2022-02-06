# Projeto Final

## Requisitos para correr a aplicação
- Docker (https://docs.docker.com/get-docker/)
- Docker Compose (https://docs.docker.com/compose/install/)
- Python 3.9

Opcional:
- Pipenv (https://pipenv.pypa.io/en/latest/)

## Como instalar e correr a aplicação
1º Passo

Levantar a instância de postgres
```bash 
docker-compose up -d
```

2º Passo

Instalar os pacotes dependentes
```python
pip install requirements.txt
```
ou
```
pipenv install
pipenv shell
```

3º Passo

Correr as migrações da base de dados

```python
python manage.py migrate
```

4º Passo

Carregar dados aleatórios
```python
python manage.py loaddata data.json
```

5º Passo

Correr a aplicação
```python 
python manage.py runserver
```