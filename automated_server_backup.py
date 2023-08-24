import os
import shutil
import logging
import configparser
from datetime import datetime

def create_backup(src_dir, dest_dir):
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_dir = os.path.join(dest_dir, f"backup_{timestamp}")
        shutil.copytree(src_dir, backup_dir)
        logging.info(f"Backup of {src_dir} created successfully at {backup_dir}")
    except Exception as e:
        logging.error(f"Failed to create backup of {src_dir}. Error: {str(e)}")

def delete_old_backups(dest_dir, max_backups):
    backups = sorted([f for f in os.listdir(dest_dir) if f.startswith("backup_")])
    if len(backups) > max_backups:
        backups_to_delete = backups[:len(backups) - max_backups]
        for backup in backups_to_delete:
            backup_dir = os.path.join(dest_dir, backup)
            shutil.rmtree(backup_dir)
            logging.info(f"Deleted old backup: {backup_dir}")

def main():
    config = configparser.ConfigParser()
    config.read("backup_config.ini")

    src_dirs = config.sections()
    dest_dir = config.get("Global", "destination")
    max_backups = int(config.get("Global", "max_backups"))
    
    logging.basicConfig(filename="backup.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    for src_dir in src_dirs:
        create_backup(src_dir, dest_dir)

    delete_old_backups(dest_dir, max_backups)

if __name__ == "__main__":
    main()
