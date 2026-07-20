import os
import shutil
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("GhostOptimizer")

from ghost_optimizer.core import BaseTweak

class TempCleaner(BaseTweak):
    @property
    def name(self):
        return "Deep Temp Cleaning"

    @property
    def description(self):
        return "Cleans Windows Temp, Prefetch, and AppData Temp folders."

    def apply(self) -> bool:
        temp_folders = []
        if os.name == 'nt':
            temp_folders = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r"C:\Windows\Temp",
                r"C:\Windows\Prefetch"
            ]

        temp_folders = list(set([f for f in temp_folders if f]))
        cleaned = False

        for folder in temp_folders:
            if not os.path.exists(folder):
                continue
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    cleaned = True
                except Exception:
                    pass
        return cleaned

    def restore(self) -> bool:
        logger.info("Cannot restore deleted temp files.")
        return False
