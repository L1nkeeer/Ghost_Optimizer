import subprocess
from ghost_optimizer.tweaks.cleaner import BaseTweak, logger

class SysMainDisabler(BaseTweak):
    @property
    def name(self):
        return "Disable SysMain (Superfetch)"

    @property
    def description(self):
        return "Disables the SysMain service to reduce high disk usage on HDDs/SSDs."

    def apply(self) -> bool:
        try:
            subprocess.run(["sc", "stop", "SysMain"], capture_output=True)
            res = subprocess.run(["sc", "config", "SysMain", "start=", "disabled"], capture_output=True)
            return res.returncode == 0
        except Exception as e:
            logger.error(f"Failed to disable SysMain: {e}")
            return False

    def restore(self) -> bool:
        try:
            res = subprocess.run(["sc", "config", "SysMain", "start=", "auto"], capture_output=True)
            subprocess.run(["sc", "start", "SysMain"], capture_output=True)
            return res.returncode == 0
        except Exception as e:
            logger.error(f"Failed to restore SysMain: {e}")
            return False
