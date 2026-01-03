import threading
import xbmc

# Логируем старт плагина
xbmc.log("[ConsumerMapper] Plugin starting...", xbmc.LOGINFO)

# Попытка импортировать основной скрипт
try:
    import sys
    import os

    addon_dir = os.path.dirname(__file__)
    sys.path.append(os.path.join(addon_dir, "resources", "lib"))

    import consumer_mapper
    #from resources.lib import consumer_mapper
    consumer_mapper_available = True
    xbmc.log("[ConsumerMapper] consumer_mapper module found.", xbmc.LOGINFO)
except ImportError as e:
    xbmc.log(f"[ConsumerMapper] consumer_mapper module not found! {e}", xbmc.LOGERROR)
    consumer_mapper_available = False

# Запускаем слушатель в отдельном демонском потоке
if consumer_mapper_available:
    try:
        t = threading.Thread(target=consumer_mapper.run_mapper, daemon=True)
        t.start()
        xbmc.log("[ConsumerMapper] consumer_mapper thread started successfully.", xbmc.LOGINFO)
    except Exception as e:
        xbmc.log(f"[ConsumerMapper] Failed to start consumer_mapper thread: {e}", xbmc.LOGERROR)
else:
    xbmc.log("[ConsumerMapper] Plugin running without consumer_mapper.", xbmc.LOGWARNING)
