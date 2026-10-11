import os
import socket
import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)

def conn():
    return psycopg.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=int(os.getenv('DB_PORT', '5432')),
        dbname=os.getenv('DB_NAME', 'notas'),
        user=os.getenv('DB_USER', 'notas'),
        password=os.getenv('DB_PASSWORD', ''),
        connect_timeout=3,
    )


def db():
    c = conn()
    c.execute('CREATE TABLE IF NOT EXISTS notas (id SERIAL PRIMARY KEY, texto TEXT NOT NULL)')
    c.commit()
    return c


@app.get('/health/live')
def live():
    return {'status': 'vivo'}


@app.get('/health/ready')
def ready():
    try:
        with conn() as c:
            c.execute('SELECT 1')
        return {'status': 'pronto'}
    except Exception as e:
        return {'status': 'banco indisponivel', 'erro': str(e)}, 503


@app.get('/api/info')
def info():
    return {'pod': socket.gethostname(), 'versao': os.getenv('APP_VERSION', '1.0.0')}


@app.get('/api/notas')
def listar():
    with db() as c:
        rows = c.execute('SELECT id, texto FROM notas ORDER BY id DESC LIMIT 50').fetchall()
    return jsonify([{'id': r[0], 'texto': r[1]} for r in rows])


@app.post('/api/notas')
def criar():
    texto = (request.get_json(silent=True) or {}).get('texto', '').strip()
    if not texto:
        return {'erro': 'texto obrigatorio'}, 400
    with db() as c:
        c.execute('INSERT INTO notas (texto) VALUES (%s)', (texto,))
    return {'ok': True}, 201
