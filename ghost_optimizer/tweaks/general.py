import os
import logging
from ghost_optimizer.core import BaseTweak
from ghost_optimizer.utils.registry import set_reg_key, delete_reg_key

try:
    import winreg
except ImportError:
    winreg = None

logger = logging.getLogger("GhostOptimizer")

class GeneralTweaks(BaseTweak):
    @property
    def name(self):
        return "General Tweaks"

    @property
    def description(self):
        return "Applies essential tweaks to make system cleaner and faster."

    def apply(self) -> bool:
        if not winreg:
            logger.error("Registry manipulation is only supported on Windows.")
            return False

        success = True

        # UI & Explorer Tweaks
        tweaks = [
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 0),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme", 0),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize", "StartupDelayInMSec", 0),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ShowTaskViewButton", 0),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "HideSCAMeetNow", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "HideSCAMeetNow", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Dsh", "AllowNewsAndInterests", 0),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics", "MinAnimate", "0", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", "2", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "EnableTransparency", 0),
        ]

        for t in tweaks:
             hkey, subkey, name, value = t[:4]
             vtype = t[4] if len(t) == 5 else winreg.REG_DWORD
             if not set_reg_key(hkey, subkey, name, value, vtype):
                 success = False

        return success

    def restore(self) -> bool:
        if not winreg:
            return False

        # In a full implementation, we'd revert these to Windows defaults.
        # For this step, we'll restore just the dark mode and animations to their normal state.
        set_reg_key(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 1)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize", "SystemUsesLightTheme", 1)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop\WindowMetrics", "MinAnimate", "1", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "EnableTransparency", 1)

        return True

class PerformanceTweaks(BaseTweak):
    @property
    def name(self):
        return "Performance Tweaks"

    @property
    def description(self):
        return "Applies advanced tweaks to boost system performance."

    def apply(self) -> bool:
        if not winreg:
            logger.error("Registry manipulation is only supported on Windows.")
            return False

        success = True

        tweaks = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", "AllowAutoGameMode", 1),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\GameBar", "AutoGameModeEnabled", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", 0),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", 0),
            (winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", "GameDVR_Enabled", 0),
            (winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", "GameDVR_FSEBehaviorMode", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\Dwm", "OverlayTestMode", 5),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", 38),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 10),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 8),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", 6),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling", "PowerThrottlingOff", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager", "CoalescingTimerInterval", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "CsEnabled", 0),
        ]

        for hkey, subkey, name, value in tweaks:
             if not set_reg_key(hkey, subkey, name, value, winreg.REG_DWORD):
                 success = False

        return success

    def restore(self) -> bool:
        if not winreg:
            return False

        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", 1)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", "GameDVR_Enabled", 1)
        delete_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\Dwm", "OverlayTestMode")
        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling", "PowerThrottlingOff", 0)

        return True

class NvidiaProfile(BaseTweak):
    @property
    def name(self):
        return "NVIDIA Profile"
    @property
    def description(self):
        return "Optimizes NVIDIA drivers to improve performance (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class LatencyTweaks(BaseTweak):
    @property
    def name(self):
        return "Latency & Input-Lag"
    @property
    def description(self):
        return "Minimizes system latency and improves responsiveness (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class KeyboardMouseTweaks(BaseTweak):
    @property
    def name(self):
        return "Mouse & Keyboard"
    @property
    def description(self):
        return "Tweaks for minimal input lag and precise control (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class PowerplanTweaks(BaseTweak):
    @property
    def name(self):
        return "Ghost Powerplan"
    @property
    def description(self):
        return "Applies custom Power Plan for highest performance (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class HealthTweaks(BaseTweak):
    @property
    def name(self):
        return "Integrity & Health"
    @property
    def description(self):
        return "Repairs corrupted files, system health, and updates (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class DebloatTweaks(BaseTweak):
    @property
    def name(self):
        return "Bloatware & AI"
    @property
    def description(self):
        return "Uninstall pre-installed apps, AI and Paid services (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True

class OtherTweaks(BaseTweak):
    @property
    def name(self):
        return "Other"
    @property
    def description(self):
        return "A variety of system tweaks, fixes and utilities (Stub)."
    def apply(self) -> bool:
        return True
    def restore(self) -> bool:
        return True
