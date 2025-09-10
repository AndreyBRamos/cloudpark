# App de Chamados (Django + DRF + JWT + Templates + Vue 3)

## Requisitos
- Python 3.10+
- Node **não** é obrigatório (Vue via CDN)
- SQLite (padrão do Django)

O video do sistema está no repositório como: cloudpark_chamados.mp4

## Setup rápido
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed
python manage.py runserver
