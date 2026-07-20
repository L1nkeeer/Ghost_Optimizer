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
        return "Minimizes system latency and improves responsiveness."

    def apply(self) -> bool:
        if not winreg:
            logger.error("Registry manipulation is only supported on Windows.")
            return False

        success = True

        tweaks = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 10),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "AlwaysOn", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NoLazyMode", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "TimerResolution", 1),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\AutoComplete", "Append Completion", "yes", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\AutoComplete", "AutoSuggest", "yes", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "menuShowDelay", "100", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "MouseHoverTime", "20", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "LowLevelHooksTimeout", "300", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "AutoEndTasks", "1", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "WaitToKillAppTimeout", "3000", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "HungAppTimeout", "2000", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "ForegroundLockTimeout", 50),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseHoverTime", "20", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "ExtendedUIHoverTime", 20),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control", "WaitToKillServiceTimeout", "3000", winreg.REG_SZ),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel", "MinTimerResolution", 5000),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel", "ClockTimerResolution", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel", "DistributeTimers", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "ExitLatency", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "ExitLatencyCheckEnabled", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "Latency", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "LatencyToleranceDefault", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "FrameLatency", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\DXGKrnl", "MonitorLatencyTolerance", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\DXGKrnl", "MonitorRefreshLatencyTolerance", 1),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\DXGKrnl", "TdrLevel", 3),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\DXGKrnl", "TdrDelay", 10),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\DXGKrnl", "TdrDdiDelay", 10),
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

        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 20)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "menuShowDelay", "400", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Desktop", "MouseHoverTime", "400", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power", "Latency", 0)
        delete_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel", "MinTimerResolution")

        return True

class KeyboardMouseTweaks(BaseTweak):
    @property
    def name(self):
        return "Mouse & Keyboard"

    @property
    def description(self):
        return "Tweaks for minimal input lag and precise control."

    def apply(self) -> bool:
        if not winreg:
            logger.error("Registry manipulation is only supported on Windows.")
            return False

        success = True

        tweaks = [
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseSpeed", "0", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseThreshold1", "0", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseThreshold2", "0", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\PrecisionTouchPad", "EnablePrecision", 0),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\mouclass\Parameters", "MouseDataQueueSize", 64),
            (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\kbdclass\Parameters", "KeyboardDataQueueSize", 64),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "DoubleClickSpeed", "300", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Keyboard", "KeyboardDelay", "1", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Keyboard", "KeyboardSpeed", "31", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Accessibility\StickyKeys", "Flags", "506", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Accessibility\Keyboard Response", "Flags", "122", winreg.REG_SZ),
            (winreg.HKEY_CURRENT_USER, r"Control Panel\Accessibility\ToggleKeys", "Flags", "58", winreg.REG_SZ),
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

        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseSpeed", "1", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseThreshold1", "6", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_CURRENT_USER, r"Control Panel\Mouse", "MouseThreshold2", "10", winreg.REG_SZ)
        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\mouclass\Parameters", "MouseDataQueueSize", 100)
        set_reg_key(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\kbdclass\Parameters", "KeyboardDataQueueSize", 100)

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
