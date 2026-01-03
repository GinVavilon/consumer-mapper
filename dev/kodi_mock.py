import sys
from unittest.mock import MagicMock

# Создаем эмуляцию модулей
xbmc_mock = MagicMock()
xbmcgui_mock = MagicMock()

# Настраиваем логи, чтобы они печатались в консоль
xbmc_mock.LOGINFO = 1
xbmc_mock.LOGERROR = 4
xbmc_mock.log = lambda msg, level: print(f"LOG ({level}): {msg}")

# Эмулируем монитор (чтобы цикл не прерывался сразу)
class MockMonitor:
    def abortRequested(self): return False
xbmc_mock.Monitor.return_value = MockMonitor()

# Прописываем в системные модули
sys.modules["xbmc"] = xbmc_mock
sys.modules["xbmcgui"] = xbmcgui_mock
sys.modules["xbmcaddon"] = MagicMock()
