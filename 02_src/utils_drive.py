"""
Utilitário para montagem do Google Drive que funciona tanto no Colab quanto localmente.

Este módulo detecta automaticamente se está rodando no Google Colab ou localmente
e fornece uma interface unificada para montar/acessar o Google Drive.
"""

import os
import sys
from pathlib import Path

# Detectar se está no ambiente Colab
def is_colab():
    """Retorna True se o código está rodando no Google Colab."""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def mount_drive(mount_point='/content/drive', force_remount=False):
    """
    Monta o Google Drive ou configura o ambiente para acesso local.
    
    Args:
        mount_point: Ponto de montagem do drive (usado no Colab)
        force_remount: Se True, força remontagem no Colab
        
    Returns:
        str: Caminho raiz do drive (onde os arquivos estão acessíveis)
    """
    if is_colab():
        # No Colab, usar a API nativa
        from google.colab import drive
        print("🔵 Ambiente detectado: Google Colab")
        print(f"📁 Montando Google Drive em: {mount_point}")
        drive.mount(mount_point, force_remount=force_remount)
        print("✅ Google Drive montado com sucesso!")
        return mount_point
    else:
        # Localmente, informar o usuário
        print("🟢 Ambiente detectado: Local (não é Colab)")
        print("ℹ️  Google Drive não será montado (funcionalidade exclusiva do Colab)")
        print("ℹ️  Para trabalhar localmente:")
        print("   1. Use o Google Drive for Desktop para sincronizar arquivos")
        print("   2. Ou adapte os caminhos para sua estrutura local de arquivos")
        
        # Retornar um caminho local padrão (pode ser customizado)
        local_drive_path = os.path.expanduser("~/Google Drive") if os.path.exists(os.path.expanduser("~/Google Drive")) else os.getcwd()
        print(f"📂 Usando caminho local: {local_drive_path}")
        return local_drive_path

def get_project_root(base_mount_point='/content/drive'):
    """
    Retorna o caminho raiz do projeto BOLSA_2026_GEMINI.
    
    Args:
        base_mount_point: Ponto de montagem base do drive
        
    Returns:
        str: Caminho completo para a raiz do projeto
    """
    if is_colab():
        # No Colab, o caminho padrão do projeto
        project_path = os.path.join(
            base_mount_point, 
            'Shareddrives/BOLSA_2026/a_bolsa2026_gemini'
        )
    else:
        # Localmente, usar o diretório atual do repositório
        # Assumindo que este arquivo está em 02_src/
        project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        print(f"📂 Caminho do projeto (local): {project_path}")
    
    return project_path

def setup_environment():
    """
    Configura o ambiente completo: monta drive e retorna caminho do projeto.
    
    Returns:
        tuple: (drive_mount_point, project_root_path)
    """
    print("=" * 60)
    print("🚀 CONFIGURAÇÃO DO AMBIENTE - BOLSA_2026_GEMINI")
    print("=" * 60)
    
    # Montar o drive (ou configurar local)
    drive_path = mount_drive()
    
    # Obter caminho do projeto
    project_root = get_project_root(drive_path)
    
    # Adicionar ao PYTHONPATH se necessário
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"✅ Projeto adicionado ao PYTHONPATH: {project_root}")
    
    print("=" * 60)
    print("✅ AMBIENTE CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    
    return drive_path, project_root
