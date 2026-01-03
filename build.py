import os
import zipfile
import xml.etree.ElementTree as ET
import shutil
import sys
import platform

def get_kodi_addons_path():
    """Определяет путь к папке addons в зависимости от операционной системы"""
    system = platform.system()
    home = os.path.expanduser('~')
    
    if system == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'Kodi', 'addons')
    elif system == 'Darwin':  # macOS
        return os.path.join(home, 'Library', 'Application Support', 'Kodi', 'addons')
    elif system == 'Linux':
        return os.path.join(home, '.kodi', 'addons')
    return None

def build_addon(install=False):
    src_dir = 'src'
    dist_dir = 'dist'
    
    # 1. Получаем ID и версию из addon.xml
    addon_xml_path = os.path.join(src_dir, 'addon.xml')
    if not os.path.exists(addon_xml_path):
        print(f"Error: {addon_xml_path} not found!")
        return

    tree = ET.parse(addon_xml_path)
    root = tree.getroot()
    addon_id = root.get('id')
    version = root.get('version')
    
    print(f"--- Processing {addon_id} (v{version}) ---")

    # 2. Создаем ZIP (Build)
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
        
    zip_name = f"{addon_id}-{version}.zip"
    zip_path = os.path.join(dist_dir, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root_dir, _, files in os.walk(src_dir):
            for file in files:
                full_path = os.path.join(root_dir, file)
                # Важно: внутри ZIP должна быть папка с ID аддона
                arcname = os.path.join(addon_id, os.path.relpath(full_path, src_dir))
                zipf.write(full_path, arcname)
    
    print(f"[*] Archive created: {zip_path}")

    # 3. Установка в Kodi (Install)
    if install:
        kodi_path = get_kodi_addons_path()
        if kodi_path and os.path.exists(kodi_path):
            dest_path = os.path.join(kodi_path, addon_id)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            
            # Копируем содержимое src напрямую в папку аддонов Kodi
            shutil.copytree(src_dir, dest_path)
            print(f"[+] Installed directly to Kodi: {dest_path}")
            print("(!) Restart Kodi to see changes.")
        else:
            print("[!] Could not find Kodi addons folder. Zip is still available in /dist.")

if __name__ == "__main__":
    # Проверяем аргументы командной строки
    do_install = '--install' in sys.argv
    build_addon(install=do_install)