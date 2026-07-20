import subprocess
from ghost_optimizer.tweaks.cleaner import BaseTweak, logger

class NetworkOptimizer(BaseTweak):
    @property
    def name(self):
        return "Network Optimization"

    @property
    def description(self):
        return "Flushes DNS, resets Winsock, and optimizes TCP auto-tuning."

    def apply(self) -> bool:
        commands = [
            ["ipconfig", "/flushdns"],
            ["netsh", "winsock", "reset"],
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"]
        ]
        success = True
        for cmd in commands:
            try:
                res = subprocess.run(cmd, capture_output=True)
                if res.returncode != 0:
                    success = False
            except Exception as e:
                logger.error(f"Network tweak {cmd} failed: {e}")
                success = False
        return success

    def restore(self) -> bool:
        # Revert to Windows default state
        commands = [
            ["netsh", "winsock", "reset"],
            ["netsh", "int", "tcp", "set", "global", "autotuninglevel=normal"]
        ]
        for cmd in commands:
            try:
                subprocess.run(cmd, capture_output=True)
            except:
                pass
        return True
