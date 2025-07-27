#!/usr/bin/env python3
"""
Скрипт для создания директории данных
"""

import os
from pathlib import Path

def create_data_directory():
    """Создает директорию для данных"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Директория данных создана: {data_dir.absolute()}")

if __name__ == "__main__":
    create_data_directory() 