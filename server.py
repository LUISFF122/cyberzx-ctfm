from flask import Flask, request, render_template_string, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import datetime

app = Flask(__name__)

def registrar_log(mensagem):
    """Grava o IP, a data/hora e a ação diretamente no arquivo de texto"""
    try:
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip and ',' in ip:
            ip = ip.split(',').strip()
        if not ip:
            ip = "127.0.0.1"
    except RuntimeError:
        ip = "SISTEMA"
    
    horario = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linha_log = f"{horario} - [IP: {ip}] - {mensagem}\n"
    
    with open("logs_ctf.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(linha_log)

# CONFIGURAÇÃO DO RATE LIMIT (Bloqueio por IP)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

# CREDENCIAIS DO DESAFIO CTF
FLAG_TOKEN = "CTF{CyberZx_Defesas_Ativas_2026}"
ADMIN_USER = "cyberzx_admin"
ADMIN_PASSWORD = "password123"

# HTML REVISADO: APENAS TELA DE LOGIN COM DESIGN EM ARIAL E NEON VERMELHO
LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SISTEMA DEFENSIVO - CYBERZX</title>
    <style>
        body { 
            background-color: #050505; 
            color: #ff0000; 
            font-family: Arial, sans-serif; 
            padding: 20px; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0;
        }
        .container { 
            border: 2px solid #ff0000; 
            padding: 40px; 
            background-color: #0a0a0a; 
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.4);
            text-align: center;
            max-width: 400px;
            width: 100%;
            border-radius: 8px;
        }
        /* Título customizado em Arial Vermelho com brilho intenso */
        .titulo-cyber {
            font-family: Arial, sans-serif;
            font-size: 42px;
            font-weight: 900;
            color: #ff0000;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin: 0 0 10px 0;
            text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 40px #ff0000;
            animation: pulsar 1.5s infinite alternate;
        }
        @keyframes pulsar {
            from { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000; }
            to { text-shadow: 0 0 20px #ff0000, 0 0 35px #ff0000, 0 0 50px #ff0000; }
        }
        h2 { margin-bottom: 35px; font-size: 13px; letter-spacing: 2px; color: #666; text-transform: uppercase; }
        .input-group { margin-bottom: 25px; text-align: left; }
        label { display: block; margin-bottom: 8px; font-size: 11px; color: #ff0000; font-weight: bold; letter-spacing: 1px; }
        input { 
            background: #000; 
            color: #ff0000; 
            border: 1px solid #ff0000; 
            padding: 12px; 
            width: 100%; 
            box-sizing: border-box;
            font-family: Arial, sans-serif;
            border-radius: 4px;
        }
        input:focus { outline: none; box-shadow: 0 0 12px rgba(255, 0, 0, 0.6); }
        button { 
            background: #ff0000; 
            color: #000; 
            padding: 14px; 
            border: none; 
            width: 100%; 
            cursor: pointer; 
            font-weight: bold; 
            font-family: Arial, sans-serif;
            text-transform: uppercase;
            margin-top: 10px;
            transition: all 0.3s;
            border-radius: 4px;
            font-size: 14px;
            letter-spacing: 1px;
        }
        button:hover { background: #000; color: #ff0000; border: 1px solid #ff0000; box-shadow: 0 0 15px rgba(255,0,0,0.6); }
        .footer-text { margin-top: 30px; font-size: 11px; color: #333; }
        .footer-text a { color: #ff0000; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="titulo-cyber">CyberZx</h1>
        <h2>Portal Restrito - Nível 5</h2>
        
        <form method="POST" action="/login">
            <div class="input-group">
                <label>OPERADOR CREDENCIADO:</label>
                <input type="text" name="username" placeholder="username" autocomplete="off" required>
            </div>
            <div class="input-group">
                <label>CHAVE DE AUTENTICAÇÃO DIRETA:</label>
                <input type="password" name="password" placeholder="••••••••" required>
            </div>
            <button type="submit">Liberar Acesso</button>
        </form>
        <div class="footer-text">
            IP rastreado ativamente. Termos em <a href="/rules">regras_uso.txt</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    registrar_log("Acessou a página inicial de login.")
    return render_template_string(LOGIN_PAGE)

@app.route('/rules')
def rules():
    registrar_log("Acessou a página de regras de uso (/rules).")
    return """
    <body style="background:#000; color:#aaa; font-family:Arial, sans-serif; padding:30px;">
        <h3 style="color:#ff0000;">[ DIRETRIZES DE SEGURANÇA INTERNA ]</h3>
        <p>1. Tentativas consecutivas de brute force resultarão em banimento temporário automático via IP corporativo.</p>
        <p>2. Senhas padrão de fábrica foram alteradas de 'password123' em todos os setores corporativos.</p>
        <br><br>
        <a href="/" style="color:#ff0000;"><-- Voltar ao Terminal</a>
    </body>
    """

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute", error_message="Muitas tentativas! IP bloqueado temporariamente por 30-60 segundos.")
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    registrar_log(f"Tentativa de login enviada para o usuário: '{username}'")

    if username == ADMIN_USER and password == ADMIN_PASSWORD:
        registrar_log("SUCESSO: Autenticação bem-sucedida! Flag capturada.")
        return render_template_string(f"""
            <div style="background-color: #000; color: #ff0000; padding: 50px; text-align: center; font-family: Arial, sans-serif; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h1 style="color: #ff0000; font-size: 28px; text-shadow: 0 0 15px #ff0000;">🎉 INTRUSÃO EXECUTADA COM SUCESSO!</h1>
                <p style="color: #666;">Você burlou as políticas de firewall corporativo.</p>
                <br>
                <p style="color:#fff;">Copie o token abaixo e envie no direct do CyberZx:</p>
                <div style="color: #ff00ff; border: 2px dashed #ff00ff; padding: 20px; font-size: 22px; background: #0a0a0a; display: inline-block; font-weight: bold; box-shadow: 0 0 15px rgba(255,0,255,0.3);">
                    {FLAG_TOKEN}
                </div>
            </div>
        """)
    else:
        registrar_log("FALHA: Credenciais incorretas fornecidas.")
        return """
        <body style="background:#000; color:#ff0000; font-family:Arial, sans-serif; text-align:center; padding-top:100px;">
            <h2 style="font-size:30px; text-shadow: 0 0 10px #ff0000;">⚠️ ACESSO NEGADO ⚠️</h2>
            <p style="color:#888;">Credenciais inválidas inseridas no banco de dados.</p>
            <br><br>
            <a href="/" style="color:#ff0000; text-decoration:none; border: 2px solid #ff0000; padding:12px 25px; border-radius:4px; font-weight:bold;">Tentar Novamente</a>
        </body>
        """, 401

@app.errorhandler(429)
def ratelimit_handler(e):
    registrar_log("ALERTA: Rate limit atingido! Requisição bloqueada por excesso de tráfego.")
    return jsonify(error="Rate limit excedido", message=str(e.description)), 429

if __name__ == '__main__':
    with open("logs_ctf.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - [SISTEMA] - Servidor sem avatares online.\n")
    app.run(host='0.0.0.0', port=5000)
