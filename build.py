import os
import zipfile
import xml.etree.ElementTree as ET
from shutil import copytree, rmtree

def build_kodi_addon():
    src_dir = 'src'
    dist_dir = 'dist'
    
    # 1. Парсим addon.xml, чтобы узнать ID и версию
    addon_xml_path = os.path.join(src_dir, 'addon.xml')
    if not os.path.exists(addon_xml_path):
        print(f"Ошибка: {addon_xml_path} не найден!")
        return

    tree = ET.parse(addon_xml_path)
    root = tree.getroot()
    addon_id = root.get('id')
    version = root.get('version')
    
    archive_name = f"{addon_id}-{version}.zip"
    
    # 2. Создаем папку dist, если её нет
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # 3. Путь к временной папке для упаковки
    # Kodi требует, чтобы внутри ZIP была папка с ID плагина
    tmp_build_path = os.path.join(dist_dir, addon_id)
    
    if os.path.exists(tmp_build_path):
        rmtree(tmp_build_path)
        
    print(f"Сборка плагина {addon_id} версии {version}...")
    
    try:
        # Копируем содержимое src во временную папку
        copytree(src_dir, tmp_build_path)
        
        # 4. Создаем ZIP архив
        zip_path = os.path.join(dist_dir, archive_name)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root_dir, dirs, files in os.walk(tmp_build_path):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    # Сохраняем структуру пути относительно папки dist
                    arcname = os.path.relpath(file_path, dist_dir)
                    zipf.write(file_path, arcname)
        
        print(f"Успех! Архив создан: {zip_path}")
    
    finally:
        # Очистка временной папки
        if os.path.exists(tmp_build_path):
            rmtree(tmp_build_path)

if __name__ == "__main__":
    build_kodi_addon()
