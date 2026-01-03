import xbmc
import evdev
from evdev import InputDevice, ecodes
import select

LOG_TAG = "ConsumerMapper"

# Словарь для соответствия клавиш Kodi-командам
KEY_MAP = {
    ecodes.KEY_SELECT: "Action(Select)",
    ecodes.KEY_PLAYPAUSE: "Action(PlayPause)",
    ecodes.KEY_STOPCD: "Action(Stop)",
    ecodes.KEY_NEXTSONG: "Action(Next)",
    ecodes.KEY_PREVIOUSSONG: "Action(Previous)"
}

def log_info(msg):
    xbmc.log(f"[{LOG_TAG}] {msg}", xbmc.LOGINFO)

def log_error(msg):
    xbmc.log(f"[{LOG_TAG}] {msg}", xbmc.LOGERROR)

def run_mapper():
    log_info("Starting Consumer Mapper...")

    monitor = xbmc.Monitor()
    devices = [InputDevice(path) for path in evdev.list_devices()]
    input_dev = None

    # Находим устройства с хотя бы одной из нужных клавиш
    candidate_devices = []
    for dev in devices:
        caps = dev.capabilities()
        if ecodes.EV_KEY in caps and any(code in caps[ecodes.EV_KEY] for code in KEY_MAP.keys()):
            candidate_devices.append(dev)

    if candidate_devices:
        # Выбираем устройство с названием "Consumer Control", если есть
        for dev in candidate_devices:
            if "Consumer Control" in dev.name:
                input_dev = dev
                break
        if not input_dev:
            input_dev = candidate_devices[0]
        log_info(f"Selected device: {input_dev.path} ({input_dev.name})")
    else:
        log_error("No Consumer Control device found!")
        return

    # Основной цикл с select для неблокирующего чтения
    try:
        while not monitor.abortRequested():
            r, _, _ = select.select([input_dev], [], [], 0.5)
            if input_dev in r:
                for event in input_dev.read():
                    if event.type == ecodes.EV_KEY and event.code in KEY_MAP:
                        if event.value == 1:  # key down
                            cmd = KEY_MAP[event.code]
                            log_info(f"Key {event.code} pressed, sending {cmd}")
                            xbmc.executebuiltin(cmd)
                        elif event.value == 0:  # key up
                            log_info(f"Key {event.code} released")
    except Exception as e:
        log_error(f"Error reading input device: {e}")
    finally:
        input_dev.close()
        log_info("Consumer Mapper stopped, device closed.")
