import sys
import os

# 1. Настройка путей
# Получаем путь к корню проекта (на уровень выше папки dev)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Путь к папке, где лежит сам файл consumer_mapper.py
# Исходя из твоего default.py, это src/resources/lib
lib_path = os.path.join(project_root, 'src', 'resources', 'lib')
# Путь к папке src (для импорта default.py, если понадобится)
src_path = os.path.join(project_root, 'src')

# Добавляем в пути поиска Python
sys.path.insert(0, lib_path)
sys.path.insert(0, src_path)
sys.path.insert(0, current_dir) # Чтобы найти kodi_mock.py

# 2. Загружаем заглушку (kodi_mock.py должен лежать в папке dev/)
try:
    import kodi_mock
    print("--- [INFO] Kodi Mocks loaded ---")
except ImportError:
    print("--- [WARNING] kodi_mock.py not found in dev/ folder ---")

# 3. Импортируем и запускаем маппер
try:
    import consumer_mapper
    print(f"--- [SUCCESS] Found consumer_mapper at: {lib_path} ---")
    print("--- [STARTING] Press Ctrl+C to stop ---")
    consumer_mapper.run_mapper()
except ImportError as e:
    print(f"--- [ERROR] ---")
    print(f"Could not find consumer_mapper.py")
    print(f"Searched in: {lib_path}")
    print(f"Original error: {e}")
except KeyboardInterrupt:
    print("\n[STOPPED] Local test finished.")
except Exception as e:
    print(f"\n[RUNTIME ERROR] {e}")
