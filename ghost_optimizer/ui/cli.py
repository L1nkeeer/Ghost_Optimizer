import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.box import ROUNDED, HEAVY, DOUBLE
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.rule import Rule

from ghost_optimizer.utils.system import get_system_info
from ghost_optimizer.tweaks.cleaner import TempCleaner
from ghost_optimizer.tweaks.services import SysMainDisabler
from ghost_optimizer.tweaks.network import NetworkOptimizer
from ghost_optimizer.tweaks.telemetry import TelemetryDisabler

console = Console()

# Единая цветовая палитра — легко поменять тему приложения в одном месте
ACCENT = "#b388ff"       # основной акцент (светло-фиолетовый)
ACCENT_DIM = "#7c4dff"   # приглушённый акцент
OK = "#69f0ae"
ERR = "#ff5252"
MUTED = "#9e9e9e"
BG_PANEL = "#1a1625"


class GhostOptimizerUI:
    def __init__(self):
        self.sys_info = get_system_info()
        self.tweaks = {
            "1": TelemetryDisabler(),
            "2": NetworkOptimizer(),
            "3": SysMainDisabler(),
            "4": TempCleaner(),
        }
        self.status_message = "Готов к работе"

    # ------------------------------------------------------------------ #
    #  Header
    # ------------------------------------------------------------------ #
    def generate_header(self) -> Panel:
        title = Text()
        title.append("GHOST", style=f"bold {ACCENT}")
        title.append(" OPTIMIZER", style=f"bold white")

        subtitle = Text("Оптимизация системы в один клик", style=f"italic {MUTED}")

        content = Align.center(
            Text.assemble(title, "\n", subtitle),
            vertical="middle",
        )

        return Panel(
            content,
            box=HEAVY,
            border_style=ACCENT,
            style=f"on {BG_PANEL}",
            padding=(1, 2),
        )

    # ------------------------------------------------------------------ #
    #  Dashboard (система)
    # ------------------------------------------------------------------ #
    def generate_dashboard(self) -> Panel:
        table = Table(show_header=False, expand=True, box=None, padding=(0, 1))
        table.add_column("icon", width=2, justify="center")
        table.add_column("Key", style=f"{MUTED}", justify="left", ratio=2)
        table.add_column("Value", style="bold white", justify="left", ratio=3)

        admin_status = (
            Text("ДА", style=f"bold {OK}")
            if self.sys_info.is_admin
            else Text("НЕТ", style=f"bold {ERR}")
        )

        table.add_row("🖥", "ОС", f"{self.sys_info.os_name} {self.sys_info.os_version}")
        table.add_row("⚙", "Процессор", self.sys_info.cpu_name)
        table.add_row("🎮", "Видеокарта", self.sys_info.gpu_name)
        table.add_row("🛡", "Администратор", admin_status)

        return Panel(
            table,
            title=f"[bold {ACCENT}]СИСТЕМА[/]",
            title_align="left",
            box=ROUNDED,
            border_style=ACCENT_DIM,
            padding=(1, 1),
        )

    # ------------------------------------------------------------------ #
    #  Меню оптимизаций
    # ------------------------------------------------------------------ #
    def generate_menu(self) -> Panel:
        table = Table(
            show_header=True,
            expand=True,
            box=ROUNDED,
            border_style=ACCENT_DIM,
            header_style=f"bold {ACCENT}",
            padding=(0, 1),
        )
        table.add_column("№", style=f"bold {ACCENT}", width=4, justify="center")
        table.add_column("Оптимизация", style="bold white", ratio=2)
        table.add_column("Описание", style=MUTED, ratio=3)

        icons = {"1": "📡", "2": "🌐", "3": "🧠", "4": "🧹"}

        for key, tweak in self.tweaks.items():
            table.add_row(
                f"{icons.get(key, '•')} {key}",
                tweak.name,
                tweak.description,
            )

        table.add_row("⏻ Q", "Выход", "Закрыть приложение", style=MUTED)

        return Panel(
            table,
            title=f"[bold {ACCENT}]ДОСТУПНЫЕ ДЕЙСТВИЯ[/]",
            title_align="left",
            box=ROUNDED,
            border_style=ACCENT,
            padding=(1, 1),
        )

    # ------------------------------------------------------------------ #
    #  Нижняя панель со статусом / подсказками
    # ------------------------------------------------------------------ #
    def generate_footer(self) -> Panel:
        hint = Text()
        hint.append(" ↵ ", style=f"bold {BG_PANEL} on {ACCENT}")
        hint.append(" Выбрать   ", style=MUTED)
        hint.append(" Q ", style=f"bold {BG_PANEL} on {ACCENT}")
        hint.append(" Выход", style=MUTED)

        status = Text(f"● {self.status_message}", style=f"{OK}")

        table = Table.grid(expand=True)
        table.add_column(justify="left")
        table.add_column(justify="right")
        table.add_row(status, hint)

        return Panel(table, box=ROUNDED, border_style=ACCENT_DIM, padding=(0, 2))

    # ------------------------------------------------------------------ #
    #  Полный layout
    # ------------------------------------------------------------------ #
    def build_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(self.generate_header(), size=5),
            Layout(name="main", ratio=1),
            Layout(self.generate_footer(), size=3),
        )
        layout["main"].split_row(
            Layout(self.generate_dashboard(), ratio=1),
            Layout(self.generate_menu(), ratio=2),
        )
        return layout

    # ------------------------------------------------------------------ #
    #  Выполнение задачи с прогресс-баром
    # ------------------------------------------------------------------ #
    def run_task(self, task_id: str):
        tweak = self.tweaks.get(task_id)
        if not tweak:
            return

        console.print(Rule(style=ACCENT_DIM))
        console.print(Align.center(Text(tweak.name, style=f"bold {ACCENT}")))
        console.print(Rule(style=ACCENT_DIM))

        with Progress(
            SpinnerColumn(spinner_name="dots", style=ACCENT),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style=ACCENT, finished_style=OK, bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task(f"[white]Применение...", total=100)

            for _ in range(50):
                time.sleep(0.02)
                progress.update(task, advance=1)

            success = tweak.apply()

            for _ in range(50):
                time.sleep(0.01)
                progress.update(task, advance=1)

        console.print()
        if success:
            self.status_message = f"{tweak.name} — успешно"
            console.print(
                Panel(
                    Align.center(Text(f"✓  {tweak.name} применено успешно", style=f"bold {OK}")),
                    box=ROUNDED,
                    border_style=OK,
                )
            )
        else:
            self.status_message = f"Ошибка: {tweak.name}"
            console.print(
                Panel(
                    Align.center(Text(f"✗  Не удалось применить {tweak.name}", style=f"bold {ERR}")),
                    box=ROUNDED,
                    border_style=ERR,
                )
            )

        console.input(f"\n[{MUTED}]Нажмите Enter для продолжения...[/]")

    # ------------------------------------------------------------------ #
    #  Главный цикл
    # ------------------------------------------------------------------ #
    def run(self):
        console.clear()

        while True:
            console.print(self.build_layout())

            choice = console.input(
                f"\n[bold {ACCENT}]▶ Выберите опцию: [/]"
            ).strip().upper()

            if choice == "Q":
                console.clear()
                console.print(Align.center(Text("До встречи! 👋", style=f"bold {ACCENT}")))
                break
            elif choice in self.tweaks:
                console.clear()
                self.run_task(choice)
            else:
                self.status_message = "Некорректный выбор — попробуйте снова"

            console.clear()


if __name__ == "__main__":
    app = GhostOptimizerUI()
    app.run()
