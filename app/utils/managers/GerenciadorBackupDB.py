import os
import sqlite3
import shutil
import logging
from pathlib import Path


class GerenciadorBackupDB:
    """Backup circular simples para arquivos SQLite.

    - Mantém até `max_backups` níveis (ex.: .bak1 ... .bak10)
    - Usa a API de backup do SQLite para snapshot consistente
    - Cria os backups no mesmo diretório do arquivo original
    """

    def __init__(self, max_backups: int = 10, logger_name: str = 'controle_acesso') -> None:
        self.max_backups = max_backups
        self.logger = logging.getLogger(logger_name)

    def _rotate_backups(self, db_path: Path) -> None:
        """Rotaciona os arquivos .bakN (remove o mais antigo e renomeia os demais)."""
        # Remove o mais antigo
        oldest = db_path.with_suffix(db_path.suffix + f".bak{self.max_backups}")
        try:
            if oldest.exists():
                oldest.unlink()
        except Exception as e:
            self.logger.warning(f"Não foi possível remover backup antigo: {oldest} - {e}")

        # Desloca bak(N-1) -> bakN ... bak1 -> bak2
        for i in range(self.max_backups - 1, 0, -1):
            src = db_path.with_suffix(db_path.suffix + f".bak{i}")
            dst = db_path.with_suffix(db_path.suffix + f".bak{i+1}")
            try:
                if src.exists():
                    # Se destino existir por algum motivo, remove primeiro
                    if dst.exists():
                        dst.unlink()
                    src.rename(dst)
            except Exception as e:
                self.logger.warning(f"Falha ao rotacionar {src} -> {dst}: {e}")

    def create_backup(self, db_path_str: str) -> str:
        """Cria backup .bak1 do banco indicado.

        Args:
            db_path_str: Caminho absoluto do arquivo SQLite a ser copiado

        Returns:
            Caminho do backup criado (string)

        Raises:
            FileNotFoundError: se o arquivo de origem não existir
            Exception: outros erros de E/S ou SQLite
        """
        db_path = Path(db_path_str)

        if not db_path.exists():
            raise FileNotFoundError(f"Arquivo de banco não encontrado: {db_path}")

        # Garante que o diretório existe
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Rotaciona backups existentes
        self._rotate_backups(db_path)

        # Cria o novo backup consistente usando a API do SQLite
        backup_path = db_path.with_suffix(db_path.suffix + ".bak1")
        try:
            with sqlite3.connect(str(db_path)) as src_conn:
                # Garante que todas as transações estejam concluídas antes do backup
                try:
                    src_conn.execute("PRAGMA wal_checkpoint(FULL)")
                except Exception:
                    # Ignora se não estiver em WAL
                    pass

                with sqlite3.connect(str(backup_path)) as dst_conn:
                    src_conn.backup(dst_conn)

            # Como fallback adicional, caso o backup via API falhe silenciosamente,
            # verificamos tamanho > 0; se 0, faz uma cópia de arquivo.
            if backup_path.exists() and backup_path.stat().st_size == 0:
                shutil.copy2(str(db_path), str(backup_path))

            self.logger.info(f"Backup do DB criado: {backup_path}")
            return str(backup_path)
        except Exception as e:
            # Em caso de falha, tenta remover artefato incompleto
            try:
                if backup_path.exists():
                    backup_path.unlink()
            except Exception:
                pass
            raise
