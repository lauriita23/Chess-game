# Chess game

Este proyecto es una aplicación web de ajedrez desarrollada con Django. Permite a dos jugadores enfrentarse en línea en una interfaz sencilla e intuitiva.

## Características
- Registro e inicio de sesión de usuarios
- Partidas de ajedrez en tiempo real
- Movimiento legal de piezas
- Guardado del estado de la partida

## Tecnologías
- Django
- Python 
- HTML + CSS + JavaScript
- SQLite / PostgreSQL (según configuración)

## Instalación

1. Clona el repositorio:
```
git clone https://github.com/lauriita23/Chess-game.git
cd Chess-game
```

2. Crea un entorno virtual y actívalo:
```
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```
pip install -r requirements.txt
```

4. Aplica las migraciones y ejecuta el servidor:
```
python manage.py migrate
python manage.py runserver
```
