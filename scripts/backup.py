"""Backup Script for TNT Media"""
import os
import sys
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.database import DatabaseManager
from src.utils.logger import TNTLogger


def create_full_backup():
    """Create a full backup of the entire media workspace"""
    logger = TNTLogger()
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path("backups") / f"full_backup_{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating full backup at {backup_dir}")
    
    # Backup critical directories
    critical_dirs = ['memory', 'config', 'channels', 'src']
    
    for dir_name in critical_dirs:
        source = Path(dir_name)
        if source.exists():
            dest = backup_dir / dir_name
            shutil.copytree(source, dest, dirs_exist_ok=True)
            print(f"  - Backed up {dir_name}/")
    
    # Backup database
    try:
        db = DatabaseManager()
        db_backup = db.backup_database(str(backup_dir))
        print(f"  - Database backed up to {db_backup}")
    except Exception as e:
        print(f"  - Database backup failed: {e}")
    
    # Create backup manifest
    manifest = {
        "backup_id": f"backup_{timestamp}",
        "created_at": datetime.now().isoformat(),
        "type": "full_backup",
        "contents": {
            "directories": critical_dirs,
            "database": "backed_up"
        }
    }
    
    manifest_path = backup_dir / "manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"\nFull backup completed: {backup_dir}")
    print(f"Manifest saved to: {manifest_path}")
    
    return str(backup_dir)


def restore_backup(backup_dir: str):
    """Restore from a backup"""
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        print(f"Error: Backup directory {backup_dir} does not exist")
        return False
    
    print(f"Restoring from {backup_dir}")
    
    # Restore critical directories
    critical_dirs = ['memory', 'config', 'channels', 'src']
    
    for dir_name in critical_dirs:
        source = backup_path / dir_name
        if source.exists():
            dest = Path(dir_name)
            if dest.exists():
                # Create a backup of current state first
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                shutil.copytree(dest, Path("backups") / f"pre_restore_{dir_name}_{timestamp}", dirs_exist_ok=True)
            
            shutil.copytree(source, dest, dirs_exist_ok=True)
            print(f"  - Restored {dir_name}/")
    
    print("Restore completed successfully")
    return True


def list_backups():
    """List all available backups"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("No backups found")
        return []
    
    backups = []
    for item in backup_dir.iterdir():
        if item.is_dir():
            manifest = item / "manifest.json"
            if manifest.exists():
                with open(manifest, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    backups.append({
                        "directory": str(item),
                        "created_at": data.get("created_at"),
                        "type": data.get("type")
                    })
    
    if backups:
        print("\nAvailable backups:")
        for b in sorted(backups, key=lambda x: x['created_at'] or '', reverse=True):
            print(f"  - {b['directory']}")
            print(f"    Created: {b['created_at']}")
            print(f"    Type: {b['type']}")
    else:
        print("No backups found")
    
    return backups


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='TNT Media Backup Tool')
    parser.add_argument('action', choices=['backup', 'restore', 'list'],
                       help='Action to perform')
    parser.add_argument('--dir', type=str, help='Backup directory (for restore)')
    
    args = parser.parse_args()
    
    if args.action == 'backup':
        create_full_backup()
    elif args.action == 'restore':
        if not args.dir:
            print("Error: --dir is required for restore")
        else:
            restore_backup(args.dir)
    elif args.action == 'list':
        list_backups()
