#!/usr/bin/env python3
"""
Cleanup Script for SINPE Banking System
Removes unnecessary files and organizes the project structure
"""

import os
import shutil
from pathlib import Path


def cleanup_project():
    """Clean up unnecessary files and directories"""
    print("🧹 SINPE Banking System - Project Cleanup")
    print("=" * 50)

    # Files to remove (if they exist)
    files_to_remove = [
        "main_backup.py",
        "ssl_config_backup.py",
        "ssl_config_fixed.py",
        "hmac_generator_backup.py",
        "pyproject.tom",  # Typo in filename
        "integration_summary.py",
        "fix_dependencies.py",
        "setup_dependencies.py",
        "notas-proyecto.txt",
    ]

    # Directories to clean (cache files)
    dirs_to_clean = ["__pycache__", ".pytest_cache", ".ruff_cache"]

    removed_files = 0
    cleaned_dirs = 0

    # Remove unnecessary files
    for file_name in files_to_remove:
        file_path = Path(file_name)
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"🗑️ Removed: {file_name}")
                removed_files += 1
            except Exception as e:
                print(f"⚠️ Could not remove {file_name}: {e}")

    # Clean cache directories recursively
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name in dirs_to_clean:
                dir_path = Path(root) / dir_name
                try:
                    shutil.rmtree(dir_path)
                    print(f"🧹 Cleaned cache: {dir_path}")
                    cleaned_dirs += 1
                except Exception as e:
                    print(f"⚠️ Could not clean {dir_path}: {e}")

    # Remove backup SSL config files in utils
    utils_backups = [
        "app/utils/ssl_config_backup.py",
        "app/utils/ssl_config_fixed.py",
        "app/utils/hmac_generator_backup.py",
    ]

    for backup_file in utils_backups:
        backup_path = Path(backup_file)
        if backup_path.exists():
            try:
                backup_path.unlink()
                print(f"🗑️ Removed backup: {backup_file}")
                removed_files += 1
            except Exception as e:
                print(f"⚠️ Could not remove {backup_file}: {e}")

    print("\n" + "=" * 50)
    print(f"✅ Cleanup completed:")
    print(f"   📄 Files removed: {removed_files}")
    print(f"   📁 Cache directories cleaned: {cleaned_dirs}")
    print("\n🎯 Project is now optimized and clean!")

    return removed_files + cleaned_dirs > 0


if __name__ == "__main__":
    success = cleanup_project()
    if success:
        print("\n💡 Tip: Run 'python run_tests.py' to validate the cleaned system")
    else:
        print("\n💡 Project was already clean!")
