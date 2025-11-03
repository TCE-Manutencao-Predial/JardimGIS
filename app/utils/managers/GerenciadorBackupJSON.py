# utils/GerenciadorBackupJSON.py
"""
Módulo para gerenciar backups circulares dos arquivos JSON do sistema.
Implementa um sistema de backup de até 15 níveis em uma subpasta 'bak'.
"""

import os
import shutil
import logging
from typing import Optional
from ...config import DATA_DIR

jardimgis_logger = logging.getLogger('jardimgis')


class GerenciadorBackupJSON:
    """
    Gerenciador de backups circulares para arquivos JSON.
    
    Características:
    - Backups são armazenados em uma subpasta 'bak' dentro do diretório de dados
    - Sistema circular de até 15 níveis (bak1 até bak15)
    - O backup mais recente é sempre .bak1
    - Quando um novo backup é criado, os existentes são "empurrados" para frente
    - O backup mais antigo (.bak15) é removido quando um novo é criado
    """
    
    def __init__(self, max_backups: int = 15):
        """
        Inicializa o gerenciador de backup.
        
        Args:
            max_backups: Número máximo de backups a manter (padrão: 15)
        """
        self.max_backups = max_backups
        self.backup_dir = os.path.join(DATA_DIR, 'bak')
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self) -> None:
        """Garante que o diretório de backup existe."""
        if not os.path.exists(self.backup_dir):
            try:
                os.makedirs(self.backup_dir, exist_ok=True)
                jardimgis_logger.info(f"Diretório de backup criado: {self.backup_dir}")
            except Exception as e:
                jardimgis_logger.error(f"Erro ao criar diretório de backup: {e}")
                raise
    
    def _get_backup_path(self, original_file_path: str, backup_number: int) -> str:
        """
        Gera o caminho completo para um arquivo de backup.
        
        Args:
            original_file_path: Caminho do arquivo original
            backup_number: Número do backup (1 = mais recente)
            
        Returns:
            Caminho completo para o arquivo de backup
        """
        filename = os.path.basename(original_file_path)
        backup_filename = f"{filename}.bak{backup_number}"
        return os.path.join(self.backup_dir, backup_filename)
    
    def create_backup(self, file_path: str) -> bool:
        """
        Cria um backup circular do arquivo especificado.
        
        Args:
            file_path: Caminho completo do arquivo a ser copiado
            
        Returns:
            True se o backup foi criado com sucesso, False caso contrário
        """
        if not os.path.exists(file_path):
            jardimgis_logger.warning(f"Arquivo não existe para backup: {file_path}")
            return False
        
        try:
            # Garante que o diretório de backup existe
            self._ensure_backup_dir()
            
            # Remove o backup mais antigo se existir (bak15)
            oldest_backup = self._get_backup_path(file_path, self.max_backups)
            if os.path.exists(oldest_backup):
                os.remove(oldest_backup)
                jardimgis_logger.debug(f"Backup mais antigo removido: {oldest_backup}")
            
            # Move todos os backups existentes uma posição para frente
            # Começa do mais antigo (bak14) e vai até o mais recente (bak1)
            for i in reversed(range(1, self.max_backups)):
                current_backup = self._get_backup_path(file_path, i)
                next_backup = self._get_backup_path(file_path, i + 1)
                
                if os.path.exists(current_backup):
                    # Se o destino já existir, remove (não deveria acontecer, mas por segurança)
                    if os.path.exists(next_backup):
                        os.remove(next_backup)
                    
                    # Move o backup atual para a próxima posição
                    os.rename(current_backup, next_backup)
                    jardimgis_logger.debug(f"Backup movido: {os.path.basename(current_backup)} -> {os.path.basename(next_backup)}")
            
            # Cria o novo backup na posição 1 (mais recente)
            new_backup = self._get_backup_path(file_path, 1)
            shutil.copy2(file_path, new_backup)
            
            jardimgis_logger.info(f"Backup criado: {os.path.basename(file_path)} -> {os.path.basename(new_backup)}")
            return True
            
        except Exception as e:
            jardimgis_logger.error(f"Erro ao criar backup de {file_path}: {e}")
            return False
    
    def list_backups(self, file_path: str) -> list:
        """
        Lista todos os backups existentes para um arquivo.
        
        Args:
            file_path: Caminho do arquivo original
            
        Returns:
            Lista de tuplas (numero_backup, caminho_backup, tamanho, data_modificacao)
            Ordenada por número do backup (1 = mais recente)
        """
        backups = []
        
        try:
            # Lista todos os arquivos de backup que realmente existem
            filename = os.path.basename(file_path)
            backup_prefix = f"{filename}.bak"
            
            if os.path.exists(self.backup_dir):
                for arquivo in os.listdir(self.backup_dir):
                    if arquivo.startswith(backup_prefix):
                        try:
                            # Extrai o número do backup do nome do arquivo
                            numero_str = arquivo[len(backup_prefix):]
                            numero = int(numero_str)
                            
                            backup_path = os.path.join(self.backup_dir, arquivo)
                            if os.path.exists(backup_path):
                                stat = os.stat(backup_path)
                                backups.append((
                                    numero,
                                    backup_path,
                                    stat.st_size,
                                    stat.st_mtime
                                ))
                        except (ValueError, OSError) as e:
                            jardimgis_logger.warning(f"Erro ao processar backup {arquivo}: {e}")
                            continue
            
            # Remove duplicatas baseadas em tamanho e data de modificação
            backups = self._remove_duplicate_backups(backups)
            
            # Ordena por número do backup (mais recente primeiro)
            backups.sort(key=lambda x: x[0])
            
        except Exception as e:
            jardimgis_logger.error(f"Erro ao listar backups de {file_path}: {e}")
        
        return backups
    
    def _remove_duplicate_backups(self, backups: list) -> list:
        """
        Remove backups duplicados baseados em tamanho e data de modificação.
        
        Args:
            backups: Lista de tuplas (numero, caminho, tamanho, mtime)
            
        Returns:
            Lista sem duplicatas
        """
        seen = set()
        unique_backups = []
        
        for backup in backups:
            numero, caminho, tamanho, mtime = backup
            # Cria uma chave única mais específica incluindo o número do backup
            # Isso evita remover backups legítimos com tamanhos similares
            key = (tamanho, int(mtime * 10))  # Precisão de décimos de segundo
            
            if key not in seen:
                seen.add(key)
                unique_backups.append(backup)
            else:
                # Verifica se são realmente duplicatas por conteúdo, não apenas por tamanho/tempo
                backup_exists = os.path.exists(caminho)
                if not backup_exists:
                    continue  # Pula se o arquivo não existe
                    
                # Só remove se for realmente uma duplicata muito recente (mesma hora e minuto)
                is_real_duplicate = False
                for existing_backup in unique_backups:
                    existing_mtime = existing_backup[3]
                    if abs(mtime - existing_mtime) < 60 and tamanho == existing_backup[2]:  # Menos de 1 minuto
                        is_real_duplicate = True
                        break
                
                if is_real_duplicate:
                    jardimgis_logger.warning(f"Backup duplicado detectado: {os.path.basename(caminho)}")
                    try:
                        os.remove(caminho)
                        jardimgis_logger.info(f"Backup duplicado removido: {os.path.basename(caminho)}")
                    except Exception as e:
                        jardimgis_logger.error(f"Erro ao remover backup duplicado {caminho}: {e}")
                else:
                    # Não é duplicata real, mantém o backup
                    unique_backups.append(backup)
        
        return unique_backups
    
    def verify_backup_integrity(self, file_path: str) -> dict:
        """
        Verifica a integridade dos backups e corrige problemas encontrados.
        
        Args:
            file_path: Caminho do arquivo original
            
        Returns:
            Dicionário com informações sobre a verificação
        """
        result = {
            'total_backups': 0,
            'duplicates_removed': 0,
            'gaps_fixed': 0,
            'errors': []
        }
        
        try:
            # Lista todos os backups atuais
            all_backups = []
            for i in range(1, self.max_backups + 1):
                backup_path = self._get_backup_path(file_path, i)
                if os.path.exists(backup_path):
                    stat = os.stat(backup_path)
                    all_backups.append((i, backup_path, stat.st_size, stat.st_mtime))
            
            result['total_backups'] = len(all_backups)
            
            # Remove duplicatas
            unique_backups = self._remove_duplicate_backups(all_backups)
            result['duplicates_removed'] = len(all_backups) - len(unique_backups)
            
            # Reorganiza backups para eliminar gaps
            if unique_backups:
                # Ordena por data de modificação (mais recente primeiro)
                unique_backups.sort(key=lambda x: x[3], reverse=True)
                
                # Renomeia para sequência contínua
                for new_num, (old_num, old_path, size, mtime) in enumerate(unique_backups, 1):
                    expected_path = self._get_backup_path(file_path, new_num)
                    
                    if old_path != expected_path:
                        if os.path.exists(expected_path):
                            os.remove(expected_path)
                        os.rename(old_path, expected_path)
                        result['gaps_fixed'] += 1
                        jardimgis_logger.debug(f"Backup reorganizado: bak{old_num} -> bak{new_num}")
            
        except Exception as e:
            error_msg = f"Erro na verificação de integridade: {e}"
            result['errors'].append(error_msg)
            jardimgis_logger.error(error_msg)
        
        return result
    
    def restore_backup(self, file_path: str, backup_number: int) -> bool:
        """
        Restaura um backup específico sobre o arquivo original.
        
        Args:
            file_path: Caminho do arquivo original
            backup_number: Número do backup a restaurar
            
        Returns:
            True se a restauração foi bem-sucedida, False caso contrário
        """
        backup_path = self._get_backup_path(file_path, backup_number)

        if not os.path.exists(backup_path):
            jardimgis_logger.error(f"Backup não encontrado: {backup_path}")
            return False

        try:
            # 1. Copia o conteúdo do backup selecionado para um arquivo temporário
            #    (isso evita perder o conteúdo quando rotacionarmos os backups ao criar o backup do estado atual)
            temp_restore_path = backup_path + ".restaurando"
            shutil.copy2(backup_path, temp_restore_path)
            jardimgis_logger.debug(f"Backup #{backup_number} copiado para temporário: {temp_restore_path}")

            # 2. Cria backup do estado atual usando a lógica padrão (rotaciona e salva como bak1)
            if os.path.exists(file_path):
                self.create_backup(file_path)
                jardimgis_logger.debug("Backup do estado atual criado antes da restauração (agora em .bak1)")

            # 3. Restaura o conteúdo salvo temporariamente sobre o arquivo original
            shutil.copy2(temp_restore_path, file_path)

            # 4. Remove o temporário
            try:
                os.remove(temp_restore_path)
            except OSError:
                pass

            # 5. Força sincronização em disco (quando suportado) e pequena espera
            if hasattr(os, 'sync'):
                try:
                    os.sync()
                except Exception:
                    pass
            import time
            time.sleep(0.05)

            # 6. Log e invalidação de caches
            new_mod_time = os.path.getmtime(file_path)
            jardimgis_logger.info(f"Arquivo restaurado a partir de backup #{backup_number}. Novo mtime: {new_mod_time}")
            self._invalidate_caches(file_path)
            return True

        except Exception as e:
            jardimgis_logger.error(f"Erro ao restaurar backup {backup_path}: {e}")
            # Tenta remover temporário se existir
            try:
                if 'temp_restore_path' in locals() and os.path.exists(temp_restore_path):
                    os.remove(temp_restore_path)
            except Exception:
                pass
            return False
    
    def _invalidate_caches(self, file_path):
        """Invalida caches específicos baseado no arquivo restaurado"""
        try:
            filename = os.path.basename(file_path)
            
            # Para arquivos JSON principais, força recarregamento removendo da memória
            # qualquer cache que possa existir em instâncias de outros gerenciadores
            if filename in ['controle_nfs.json']:
                jardimgis_logger.info(f"Arquivo principal {filename} restaurado - outras instâncias podem precisar recarregar dados")
            
        except Exception as e:
            jardimgis_logger.warning(f"Erro ao invalidar caches: {str(e)}")
    
    def cleanup_old_backups(self, file_path: str, keep_count: Optional[int] = None) -> int:
        """
        Remove backups antigos, mantendo apenas os mais recentes.
        
        Args:
            file_path: Caminho do arquivo original
            keep_count: Número de backups a manter (padrão: self.max_backups)
            
        Returns:
            Número de backups removidos
        """
        if keep_count is None:
            keep_count = self.max_backups
        
        removed_count = 0
        
        try:
            for i in range(keep_count + 1, self.max_backups + 1):
                backup_path = self._get_backup_path(file_path, i)
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                    removed_count += 1
                    jardimgis_logger.debug(f"Backup antigo removido: {backup_path}")
        except Exception as e:
            jardimgis_logger.error(f"Erro ao limpar backups antigos de {file_path}: {e}")
        
        return removed_count
    
    def get_backup_info(self, file_path: str) -> dict:
        """
        Retorna informações sobre os backups de um arquivo.
        
        Args:
            file_path: Caminho do arquivo original
            
        Returns:
            Dicionário com informações dos backups
        """
        backups = self.list_backups(file_path)
        total_size = sum(backup[2] for backup in backups)
        
        return {
            'total_backups': len(backups),
            'total_size_bytes': total_size,
            'oldest_backup': max(backups, key=lambda x: x[0])[0] if backups else 0,
            'newest_backup': min(backups, key=lambda x: x[0])[0] if backups else 0,
            'backups': backups
        }


# Instância global para uso em todo o sistema
backup_manager = GerenciadorBackupJSON()


def create_backup(file_path: str) -> bool:
    """
    Função de conveniência para criar backup de um arquivo.
    
    Args:
        file_path: Caminho completo do arquivo
        
    Returns:
        True se o backup foi criado com sucesso
    """
    return backup_manager.create_backup(file_path)


def list_backups(file_path: str) -> list:
    """
    Função de conveniência para listar backups de um arquivo.
    
    Args:
        file_path: Caminho do arquivo original
        
    Returns:
        Lista de backups disponíveis
    """
    return backup_manager.list_backups(file_path)


def restore_backup(file_path: str, backup_number: int) -> bool:
    """
    Função de conveniência para restaurar um backup.
    
    Args:
        file_path: Caminho do arquivo original
        backup_number: Número do backup a restaurar
        
    Returns:
        True se a restauração foi bem-sucedida
    """
    return backup_manager.restore_backup(file_path, backup_number)
