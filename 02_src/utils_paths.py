
import os
import yaml
from typing import List

# --- Constantes e Carregamento de Configuração ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def _load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config_paths.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config['paths']

PATHS = _load_config()

# --- Funções Utilitárias ---
class PathKeyNotFoundError(KeyError):
    def __init__(self, key):
        super().__init__(f"PATH_KEY_NOT_FOUND: '{key}' não é uma chave válida em config_paths.yaml")

def P(key: str, *extra: str, create_dirs: bool = False) -> str:
    if key not in PATHS:
        raise PathKeyNotFoundError(key)
    base_path = PATHS[key]
    full_path = os.path.join(ROOT, base_path, *extra)
    
    # CORREÇÃO #1: Lógica de criação de diretórios ajustada.
    if create_dirs:
        if len(extra) == 0:
            # A chave representa um diretório base (ex: P("models"))
            os.makedirs(full_path, exist_ok=True)
        else:
            # O caminho final provavelmente é um arquivo (ex: P("reports", "report.pdf"))
            # então cria o diretório pai.
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
    return os.path.normpath(full_path)

def ensure_dirs(*keys: str) -> None:
    print(f"Garantindo a existência dos diretórios para as chaves: {list(keys)}")
    for key in keys:
        try:
            path_to_ensure = P(key, create_dirs=True)
            print(f"  - OK: {key} -> {path_to_ensure}")
        except PathKeyNotFoundError as e:
            print(f"  - AVISO: {e}")
