import json
import os


SESSION_FILE = "session.json"

def carregar_sessao():
    """Carrega os dados da sessão, retornando um dicionário vazio se houver erro."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                conteudo = f.read().strip()
                if not conteudo:  # Se o arquivo estiver vazio
                    return {}
                return json.loads(conteudo)
        except json.JSONDecodeError:
            return {}  # Retorna um dicionário vazio se o JSON estiver corrompido
    return {}

def salvar_sessao(dados):
    """Salva os dados da sessão em um arquivo JSON."""
    with open(SESSION_FILE, "w") as f:
        json.dump(dados, f)
