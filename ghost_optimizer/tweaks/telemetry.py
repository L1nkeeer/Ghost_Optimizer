import os
import ctypes
import subprocess
from ghost_optimizer.tweaks.cleaner import BaseTweak, logger

class TelemetryDisabler(BaseTweak):
    @property
    def name(self):
        return "Disable Telemetry"

    @property
    def description(self):
        return "Disables Windows Telemetry and Data Collection (DiagTrack, WAPPush)."

    def apply(self) -> bool:
        if os.name != 'nt':
            return False

        try:
            # Stop services
            subprocess.run(["sc", "stop", "DiagTrack"], capture_output=True)
            subprocess.run(["sc", "stop", "dmwappushservice"], capture_output=True)

            # Disable services
            subprocess.run(["sc", "config", "DiagTrack", "start=", "disabled"], capture_output=True)
            subprocess.run(["sc", "config", "dmwappushservice", "start=", "disabled"], capture_output=True)

            # Registry tweaks
            cmds = [
                r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f',
                r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, capture_output=True)

            return True
        except Exception as e:
            logger.error(f"Failed to disable telemetry: {e}")
            return False

    def restore(self) -> bool:
        if os.name != 'nt':
            return False

        try:
            subprocess.run(["sc", "config", "DiagTrack", "start=", "auto"], capture_output=True)
            subprocess.run(["sc", "config", "dmwappushservice", "start=", "auto"], capture_output=True)

            cmds = [
                r'reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\DataCollection" /v AllowTelemetry /f',
                r'reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v AllowCortana /f'
            ]
            for cmd in cmds:
                subprocess.run(cmd, shell=True, capture_output=True)

            return True
        except Exception as e:
            logger.error(f"Failed to restore telemetry: {e}")
            return False
