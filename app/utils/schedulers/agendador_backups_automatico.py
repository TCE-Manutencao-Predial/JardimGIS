"""
Agendador de Backups Automáticos
Executa backups diários de todos os arquivos de dados às 20h
Sistema circular de 15 níveis
"""

import logging
import schedule
import time
import threading
from datetime import datetime
from pathlib import Path

# Importações dos gerenciadores
from ...config import (
    DATA_DIR,
    ARVORES_JSON_PATH,
)

from ..managers.GerenciadorBackupJSON import create_backup as create_json_backup


logger = logging.getLogger('jardimgis')


class AgendadorBackups:
    """
    Agendador de backups automáticos para arquivos de dados.
    Executa diariamente às 20h com sistema circular de 15 níveis.
    """
    
    def __init__(self):
        self.running = False
        self.thread = None
        
        # Lista de arquivos JSON para backup
        self.json_files = [
            ('Controle de Árvores', ARVORES_JSON_PATH),
        ]
        
        logger.info("🔄 AgendadorBackups inicializado")
    
    def fazer_backup_json(self, nome: str, caminho: str) -> bool:
        """Executa backup de um arquivo JSON específico."""
        try:
            if not Path(caminho).exists():
                logger.warning(f"⚠️ Arquivo {nome} não existe: {caminho}")
                return False
            
            sucesso = create_json_backup(caminho)
            if sucesso:
                logger.info(f"✅ Backup de {nome} criado com sucesso")
            else:
                logger.error(f"❌ Falha ao criar backup de {nome}")
            return sucesso
        except Exception as e:
            logger.error(f"❌ Erro ao fazer backup de {nome}: {e}")
            return False
    
    def executar_backups_completos(self):
        """Executa todos os backups programados."""
        logger.info("=" * 70)
        logger.info("🔄 INICIANDO BACKUPS AUTOMÁTICOS DIÁRIOS")
        logger.info(f"⏰ Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info("=" * 70)
        
        total = 0
        sucesso = 0
        falhas = 0
        
        # Backups de arquivos JSON
        logger.info("📄 Iniciando backups de arquivos JSON...")
        for nome, caminho in self.json_files:
            total += 1
            if self.fazer_backup_json(nome, caminho):
                sucesso += 1
            else:
                falhas += 1
        
        # Relatório final
        logger.info("=" * 70)
        logger.info(f"✅ BACKUPS CONCLUÍDOS: {sucesso}/{total} sucessos, {falhas}/{total} falhas")
        logger.info(f"⏰ Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        logger.info("=" * 70)
    
    def agendar_backups(self):
        """Configura o agendamento diário às 20h."""
        schedule.clear()
        schedule.every().day.at("20:00").do(self.executar_backups_completos)
        logger.info("📅 Backups agendados para executar diariamente às 20:00")
    
    def iniciar(self):
        """Inicia o agendador em uma thread separada."""
        if self.running:
            logger.warning("⚠️ Agendador já está em execução")
            return
        
        self.running = True
        self.agendar_backups()
        
        def executar():
            logger.info("🚀 Thread do agendador de backups iniciada")
            while self.running:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Verifica a cada minuto
                except Exception as e:
                    logger.error(f"❌ Erro no agendador de backups: {e}")
                    time.sleep(60)
            logger.info("🛑 Thread do agendador de backups finalizada")
        
        self.thread = threading.Thread(target=executar, daemon=True, name="BackupScheduler")
        self.thread.start()
        logger.info("✅ Agendador de backups iniciado com sucesso")
    
    def parar(self):
        """Para o agendador."""
        if not self.running:
            logger.warning("⚠️ Agendador não está em execução")
            return
        
        logger.info("⏸️ Parando agendador de backups...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        schedule.clear()
        logger.info("✅ Agendador de backups parado")
    
    def status(self) -> dict:
        """Retorna o status atual do agendador."""
        return {
            'running': self.running,
            'next_run': str(schedule.next_run()) if schedule.jobs else 'Não agendado',
            'files_count': len(self.json_files),
            'files': [nome for nome, _ in self.json_files]
        }
    
    def executar_backup_manual(self):
        """Executa backup manual imediatamente."""
        logger.info("🔧 Backup manual solicitado")
        self.executar_backups_completos()


# Instância singleton global
_agendador_instance = None


def get_agendador_backups() -> AgendadorBackups:
    """Retorna a instância singleton do agendador."""
    global _agendador_instance
    if _agendador_instance is None:
        _agendador_instance = AgendadorBackups()
    return _agendador_instance


def iniciar_agendador_backups():
    """Inicializa e inicia o agendador de backups."""
    agendador = get_agendador_backups()
    agendador.iniciar()
    return agendador


def parar_agendador_backups():
    """Para o agendador de backups."""
    global _agendador_instance
    if _agendador_instance:
        _agendador_instance.parar()


def status_agendador_backups() -> dict:
    """Retorna o status do agendador."""
    agendador = get_agendador_backups()
    return agendador.status()


def backup_manual():
    """Executa backup manual."""
    agendador = get_agendador_backups()
    agendador.executar_backup_manual()
