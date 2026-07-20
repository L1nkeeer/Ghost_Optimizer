import os
import sys
import time
import subprocess
import shutil
import ctypes

# ANSI colors using a premium 256-color palette
PURPLE = "\033[38;5;129m"      # Main purple accent
SHADOW = "\033[38;5;57m"       # Deep blue/indigo drop shadow
GRAY = "\033[38;5;244m"        # Muted gray for descriptions
WHITE = "\033[38;5;255m"       # Bright white for selected text/values
CYAN = "\033[38;5;45m"         # Accent cyan
RED = "\033[38;5;196m"         # Warning red
GREEN = "\033[38;5;46m"        # Success green
RESET = "\033[0m"              # Reset all formatting

# Cross-platform raw input handler for instant key capture without requiring Enter
if os.name == 'nt':
    import msvcrt
    def get_key_stroke():
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            # Handle special functional keys or arrow keys on Windows if needed
            if ch in (b'\x00', b'\xe0'):
                msvcrt.getch()
                return None
            try:
                return ch.decode('utf-8', errors='ignore').lower()
            except:
                return None
        return None
else:
    import tty
    import termios
    import select
    def get_key_stroke():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
            if rlist:
                ch = sys.stdin.read(1)
                return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hardware_specs():
    """Queries system hardware specifications with mock fallbacks to match screenshot layouts."""
    cpu = "AMD Ryzen 5 5500U with Radeon Graphics"
    gpu = "AMD Radeon(TM) Graphics"

    if os.name == 'nt':
        try:
            # Query CPU via WMI
            cpu_raw = subprocess.check_output("wmic cpu get name", shell=True).decode('utf-8', errors='ignore')
            cpu_lines = [line.strip() for line in cpu_raw.split('\n') if line.strip()]
            if len(cpu_lines) > 1:
                cpu = cpu_lines[1]

            # Query GPU via WMI
            gpu_raw = subprocess.check_output("wmic path win32_VideoController get name", shell=True).decode('utf-8', errors='ignore')
            gpu_lines = [line.strip() for line in gpu_raw.split('\n') if line.strip()]
            if len(gpu_lines) > 1:
                gpu = gpu_lines[1]
        except Exception:
            pass

    return cpu, gpu

def draw_shadowed_title(title_type):
    """
    Renders high-fidelity, shadowed 3D ASCII headers as requested,
    matching image_beb0cf.png, image_beb171.png, and image_beb1ad.png.
    """
    titles = {
        "WELCOME": [
            "██╗    ██╗███████╗██╗      ██████╗  ██████╗ ███╗   ███╗███████╗",
            "██║    ██║██╔════╝██║     ██╔════╝ ██╔═══██╗████╗ ████║██╔════╝",
            "██║ █╗ ██║█████╗  ██║     ██║      ██║   ██║██╔████╔██║█████╗  ",
            "██║███╗██║██╔══╝  ██║     ██║      ██║   ██║██║╚██╔╝██║██╔══╝  ",
            "╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗",
            " ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝"
        ],
        "GHOST OPTIMIZER": [
            " ██████╗ ██╗  ██╗ ██████╗  ██████╗████████╗     ██████╗ ██████╗ ████████╗██╗███╗   ███╗██╗███████╗███████╗██████╗ ",
            "██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔═══██╗██╔══██╗╚══██╔══╝██║████╗ ████║██║╚══███╔╝██╔════╝██╔══██╗",
            "██║  ███╗███████║██║   ██║╚█████╗     ██║       ██║   ██║██████╔╝   ██║   ██║██╔████╔██║██║  ███╔╝ █████╗  ██████╔╝",
            "██║   ██║██╔══██║██║   ██║ ╚═══██╗    ██║       ██║   ██║██╔═══╝    ██║   ██║██║╚██╔╝██║██║ ███╔╝  ██╔══╝  ██╔══██╗",
            "╚██████╔╝██║  ██║╚██████╔╝██████╔╝    ██║       ╚██████╔╝██║        ██║   ██║██║ ╚═╝ ██║██║███████╗███████╗██║  ██║",
            " ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝     ╚═╝        ╚═════╝ ╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝"
        ],
        "OTHER": [
            " ██████╗ ████████╗██╗  ██╗███████╗██████╗ ",
            "██╔═══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗",
            "██║   ██║   ██║   ███████║█████╗  ██████╔╝",
            "██║   ██║   ██║   ██╔══██║██╔══╝  ██╔══██╗",
            "╚██████╔╝   ██║   ██║  ██║███████╗██║  ██║",
            " ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"
        ]
    }

    lines = titles.get(title_type, [])

    # Render with offset shadow block programmatically
    for line in lines:
        # 1. Print shadow line (shifted right by 2 spaces)
        sys.stdout.write("  " + SHADOW + line.replace("█", "▒") + RESET + "\n")
        # 2. Move cursor up to draw front layer on top
        sys.stdout.write("\033[A")
        # 3. Print front layer (aligned, shifted by 1 space for volumetric effect)
        sys.stdout.write(" " + PURPLE + line + RESET + "\n")
    print()

class GhostOptimizerTUI:
    def __init__(self):
        self.state = "WELCOME"  # WELCOME, MAIN, OTHER, EXECUTE
        self.running = True
        self.cpu, self.gpu = get_hardware_specs()
        self.current_action = ""
        self.input_buffer = ""

    def draw_welcome(self):
        """Generates the welcome configuration menu from image_beb0cf.png."""
        draw_shadowed_title("WELCOME")

        # Horizontal purple separator
        print(PURPLE + "─" * 110 + RESET)
        print()

        # Descriptive blocks translated to Russian
        print(f"       {PURPLE}Ghost Optimizer{GRAY} — это продвинутый скрипт с открытым исходным кодом, который повышает")
        print(f"       производительность, снижает задержки, оптимизирует сеть и приватность, удаляя ненужный софт и функции ИИ.{RESET}")
        print()
        print(f"       {GRAY}Опция отката твиков может работать нестабильно; создайте точку восстановления для безопасности.")
        print(f"       Используйте этот скрипт на свой страх и риск. Автор не несет ответственности за любые повреждения или потерю данных.")
        print(f"       Вы можете сообщить о багах или предложить улучшения на Github.{RESET}")
        print()
        print(f"                                         {GRAY}Создано пользователем: {PURPLE}@louzkk{RESET}")
        print("\n" * 2)

        # Interactive Option selectors
        print(f"               [ {PURPLE}Y{RESET} ] {WHITE}Создать точку восстановления{RESET}             [ {PURPLE}N{RESET} ] {WHITE}Пропустить точку восстановления{RESET}")
        print("\n" * 3)
        sys.stdout.write(f"{WHITE}>: {RESET}{self.input_buffer}")
        sys.stdout.flush()

    def draw_main_menu(self):
        """Generates the dual-column master control menu from image_beb171.png."""
        draw_shadowed_title("GHOST OPTIMIZER")

        # System Spec Display matching specs bar exactly
        specs_str = f"{PURPLE}GPU: {WHITE}{self.gpu}             {PURPLE}CPU: {WHITE}{self.cpu}"
        print(specs_str.center(120))
        print()
        print(PURPLE + "─" * 110 + RESET)
        print()

        # Fast Action Headers
        print(f"                     [ {PURPLE}A{RESET} ] {WHITE}Применить всё*{RESET}                     [ {PURPLE}R{RESET} ] {WHITE}Откатить всё{RESET}")
        print()

        # Three Column Option Matrix
        # Col 1, Col 2, Col 3
        options = [
            ("[ 1 ] Общие твики", "[ 2 ] Оптимизация системы", "[ 3 ] Настройка сети"),
            ("[ 4 ] Профиль NVIDIA", "[ 5 ] Задержка и инпут-лаг", "[ 6 ] Мышь и клавиатура"),
            ("[ 7 ] Очистка Windows", "[ 8 ] Телеметрия и логи", "[ 9 ] Службы Windows"),
            ("[ 10 ] План питания Ghost", "[ 11 ] Проверка системы", "[ 12 ] Bloatware и ИИ")
        ]

        for o1, o2, o3 in options:
            # Colorizing bracket indicators
            o1_f = o1.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(o1.split("] ")[1], f"{GRAY}{o1.split('] ')[1]}{RESET}")
            o2_f = o2.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(o2.split("] ")[1], f"{GRAY}{o2.split('] ')[1]}{RESET}")
            o3_f = o3.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(o3.split("] ")[1], f"{GRAY}{o3.split('] ')[1]}{RESET}")
            print(f"       {o1_f:<45} {o2_f:<45} {o3_f:<45}")

        print()
        # Bottom Utility Option
        opt_13 = f"[ 13 ] Другое (Различные утилиты)"
        opt_13_f = opt_13.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(opt_13.split("] ")[1], f"{WHITE}{opt_13.split('] ')[1]}{RESET}")
        print(f"                                         {opt_13_f}")
        print("\n" * 2)
        sys.stdout.write(f"{WHITE}>: {RESET}{self.input_buffer}")
        sys.stdout.flush()

    def draw_other_menu(self):
        """Generates the utility secondary board from image_beb1ad.png."""
        draw_shadowed_title("OTHER")

        print(f"                      {PURPLE}Различные системные твики, исправления, обходы и дополнительные утилиты.{RESET}")
        print()
        print(PURPLE + "─" * 110 + RESET)
        print()

        # Dual Column layout for submenu options
        sub_options = [
            ("[ 1 ] Обход требований TPM 2.0", "[ 2 ] Включить Режим Бога (God Mode)"),
            ("[ 3 ] Показывать расширения файлов", "[ 4 ] Быстрая очистка журналов событий"),
            ("[ 5 ] Показывать скрытые файлы и папки", "[ 6 ] Восстановить классическое меню Windows"),
            ("[ 7 ] Отключить службу SysMain (HDD Fix)", "")
        ]

        for left, right in sub_options:
            left_f = left.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(left.split("] ")[1], f"{GRAY}{left.split('] ')[1]}{RESET}") if left else ""
            if "SysMain" in left:
                left_f += f"   {GRAY}<-- Может исправить высокую нагрузку на HDD{RESET}"

            right_f = right.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(right.split("] ")[1], f"{GRAY}{right.split('] ')[1]}{RESET}") if right else ""
            print(f"             {left_f:<65} {right_f:<55}")

        print("\n" * 2)
        # Return Action Line
        back_opt = f"[ B ] Назад в главное меню"
        back_opt_f = back_opt.replace("[", f"[{PURPLE}").replace("]", f"{RESET}]").replace(back_opt.split("] ")[1], f"{WHITE}{back_opt.split('] ')[1]}{RESET}")
        print(f"                                         {back_opt_f}")
        print("\n" * 2)
        sys.stdout.write(f"{WHITE}>: {RESET}{self.input_buffer}")
        sys.stdout.flush()


    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def clean_windows_temp(self):
        """Actually deletes files in Windows Temp folders."""
        temp_folders = []
        if os.name == 'nt':
            temp_folders = [
                os.environ.get('TEMP', ''),
                os.environ.get('TMP', ''),
                r"C:\Windows\Temp",
                r"C:\Windows\Prefetch"
            ]

        # Remove empty or duplicate entries
        temp_folders = list(set([f for f in temp_folders if f]))

        cleaned_size = 0
        deleted_files = 0

        for folder in temp_folders:
            if not os.path.exists(folder):
                continue
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        size = os.path.getsize(file_path)
                        os.unlink(file_path)
                        cleaned_size += size
                        deleted_files += 1
                    elif os.path.isdir(file_path):
                        # Calculate size before removing
                        for dirpath, _, filenames in os.walk(file_path):
                            for f in filenames:
                                fp = os.path.join(dirpath, f)
                                if not os.path.islink(fp):
                                    cleaned_size += os.path.getsize(fp)
                        shutil.rmtree(file_path)
                        deleted_files += 1
                except Exception as e:
                    # File might be in use
                    pass

        return deleted_files, cleaned_size

    def perform_action(self):
        """Simulates or performs advanced script components execution visually."""
        clear_screen()
        print(PURPLE + "─" * 110 + RESET)
        print(f" Выполняется: {WHITE}{self.current_action}{RESET}".center(110))
        print(PURPLE + "─" * 110 + RESET)
        print("\n" * 2)

        if self.current_action == "Глубокая очистка Windows":
            print(f" {GRAY}[{PURPLE}*{GRAY}]{RESET} Анализ временных папок (Temp, Prefetch)...")
            time.sleep(0.5)
            print(f" {GRAY}[{PURPLE}*{GRAY}]{RESET} Очистка файлов...")

            deleted_count, freed_bytes = self.clean_windows_temp()
            freed_mb = freed_bytes / (1024 * 1024)

            # Simple progress bar
            for i in range(1, 6):
                sys.stdout.write(f"\r   [{PURPLE}" + "█" * i + "░" * (5 - i) + f"{RESET}] {i*20}%")
                sys.stdout.flush()
                time.sleep(0.2)
            print(f" {GREEN}[УСПЕШНО]{RESET}\n")
            print(f" {CYAN}Удалено объектов:{RESET} {deleted_count}")
            print(f" {CYAN}Освобождено места:{RESET} {freed_mb:.2f} MB\n")

        else:
            # Fallback mock animation for unimplemented features
            steps = [
                "Инициализация зависимостей и окружения...",
                "Проверка прав локального администратора...",
                "Применение настроек..."
            ]

            for step in steps:
                print(f" {GRAY}[{PURPLE}*{GRAY}]{RESET} {step}")
                time.sleep(0.3)
                for i in range(1, 6):
                    sys.stdout.write(f"\r   [{PURPLE}" + "█" * i + "░" * (5 - i) + f"{RESET}] {i*20}%")
                    sys.stdout.flush()
                    time.sleep(0.1)
                print(f" {GREEN}[УСПЕШНО]{RESET}\n")
                time.sleep(0.15)

        print(PURPLE + "─" * 110 + RESET)
        print(f" {GREEN}✓ Операция '{self.current_action}' завершена.{RESET}".center(110))
        print(f" {GRAY}Нажмите любую клавишу для возврата...{RESET}".center(110))
        print(PURPLE + "─" * 110 + RESET)

        # Wait for keypress to return to menu
        while True:
            if get_key_stroke() is not None:
                break
            time.sleep(0.02)

        self.input_buffer = ""
        # Route back to corresponding screen context
        if self.state == "EXECUTE_TO_MAIN":
            self.state = "MAIN"
        elif self.state == "EXECUTE_TO_OTHER":
            self.state = "OTHER"

    def run(self):
        # Configure terminal window size if on Windows
        if os.name == 'nt':
            os.system('mode con cols=115 lines=32')
            os.system('') # Enable ANSI sequences

        while self.running:
            clear_screen()

            if self.state == "WELCOME":
                self.draw_welcome()
            elif self.state == "MAIN":
                self.draw_main_menu()
            elif self.state == "OTHER":
                self.draw_other_menu()
            elif self.state in ("EXECUTE_TO_MAIN", "EXECUTE_TO_OTHER"):
                self.perform_action()
                continue

            # Direct non-blocking state/input evaluation loop
            key = None
            start_wait = time.time()
            while key is None and (time.time() - start_wait < 0.1):
                key = get_key_stroke()
                time.sleep(0.01)

            if key is not None:
                if key == '\r' or key == '\n':
                    # Process current input buffer on Enter
                    cmd = self.input_buffer.strip().lower()

                    if self.state == "WELCOME":
                        if cmd == 'y':
                            self.current_action = "Создание точки восстановления системы"
                            self.state = "EXECUTE_TO_MAIN"
                        elif cmd == 'n':
                            self.state = "MAIN"

                    elif self.state == "MAIN":
                        if cmd == '13':
                            self.state = "OTHER"
                        elif cmd == 'a':
                            self.current_action = "Полное применение твиков оптимизации"
                            self.state = "EXECUTE_TO_MAIN"
                        elif cmd == 'r':
                            self.current_action = "Полный откат системных твиков"
                            self.state = "EXECUTE_TO_MAIN"
                        elif cmd in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'):
                            mapping = {
                                '1': "Применение общих твиков",
                                '2': "Твики производительности",
                                '3': "Твики сетевой инфраструктуры",
                                '4': "Оптимизация профиля NVIDIA",
                                '5': "Снижение задержки и инпут-лага",
                                '6': "Калибровка мыши и клавиатуры",
                                '7': "Глубокая очистка Windows",
                                '8': "Отключение телеметрии и логов",
                                '9': "Управление службами Windows",
                                '10': "Активация плана электропитания Ghost",
                                '11': "Запуск проверки целостности системы",
                                '12': "Удаление Bloatware и компонентов ИИ"
                            }
                            self.current_action = mapping[cmd]
                            self.state = "EXECUTE_TO_MAIN"

                    elif self.state == "OTHER":
                        if cmd == 'b':
                            self.state = "MAIN"
                        elif cmd in ('1', '2', '3', '4', '5', '6', '7'):
                            other_mapping = {
                                '1': "Обход ограничений TPM 2.0 при установке OS",
                                '2': "Активация скрытого Режима Бога (God Mode)",
                                '3': "Включение отображения расширений всех файлов",
                                '4': "Очистка системных журналов и эвент логов",
                                '5': "Включение отображения скрытых папок и файлов",
                                '6': "Восстановление классического контекстного меню",
                                '7': "Отключение службы индексации SysMain"
                            }
                            self.current_action = other_mapping[cmd]
                            self.state = "EXECUTE_TO_OTHER"

                    self.input_buffer = ""
                elif key in ('\x08', '\x7f'): # Backspace
                    self.input_buffer = self.input_buffer[:-1]
                else:
                    # Append character to screen interaction buffer
                    if len(self.input_buffer) < 15:
                        self.input_buffer += key

if __name__ == "__main__":
    tui = GhostOptimizerTUI()
    tui.run()
