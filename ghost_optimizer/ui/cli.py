import time
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

from ghost_optimizer.utils.system import get_system_info
from ghost_optimizer.tweaks.cleaner import TempCleaner
from ghost_optimizer.tweaks.services import SysMainDisabler
from ghost_optimizer.tweaks.network import NetworkOptimizer
from ghost_optimizer.tweaks.telemetry import TelemetryDisabler

console = Console()

class GhostOptimizerUI:
    def __init__(self):
        self.sys_info = get_system_info()
        self.tweaks = {
            "1": TelemetryDisabler(),
            "2": NetworkOptimizer(),
            "3": SysMainDisabler(),
            "4": TempCleaner(),
        }

    def generate_header(self) -> Panel:
        title = """[magenta]
 ██████╗ ██╗  ██╗ ██████╗  ██████╗████████╗     ██████╗ ██████╗ ████████╗██╗███╗   ███╗██╗███████╗███████╗██████╗
██╔════╝ ██║  ██║██╔═══██╗██╔════╝╚══██╔══╝    ██╔═══██╗██╔══██╗╚══██╔══╝██║████╗ ████║██║╚══███╔╝██╔════╝██╔══██╗
██║  ███╗███████║██║   ██║╚█████╗     ██║       ██║   ██║██████╔╝   ██║   ██║██╔████╔██║██║  ███╔╝ █████╗  ██████╔╝
██║   ██║██╔══██║██║   ██║ ╚═══██╗    ██║       ██║   ██║██╔═══╝    ██║   ██║██║╚██╔╝██║██║ ███╔╝  ██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║╚██████╔╝██████╔╝    ██║       ╚██████╔╝██║        ██║   ██║██║ ╚═╝ ██║██║███████╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝     ╚═╝        ╚═════╝ ╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
[/magenta]"""
        return Panel(Align.center(title), style="magenta", border_style="bold magenta")

    def generate_dashboard(self) -> Panel:
        table = Table(show_header=False, expand=True, box=None)
        table.add_column("Key", style="cyan", justify="right", ratio=1)
        table.add_column("Value", style="white", justify="left", ratio=2)

        admin_status = "[green]YES[/green]" if self.sys_info.is_admin else "[red]NO[/red]"

        table.add_row("OS:", f"{self.sys_info.os_name} {self.sys_info.os_version}")
        table.add_row("CPU:", self.sys_info.cpu_name)
        table.add_row("GPU:", self.sys_info.gpu_name)
        table.add_row("Administrator:", admin_status)

        return Panel(table, title="[bold cyan]System Dashboard[/bold cyan]", border_style="cyan")

    def generate_menu(self) -> Panel:
        table = Table(show_header=True, expand=True, border_style="magenta")
        table.add_column("ID", style="bold magenta", width=5)
        table.add_column("Optimization Task", style="white")
        table.add_column("Description", style="dim white")

        for key, tweak in self.tweaks.items():
            table.add_row(f"[{key}]", tweak.name, tweak.description)

        table.add_row("[Q]", "Quit", "Exit the application")

        return Panel(table, title="[bold magenta]Available Optimizations[/bold magenta]", border_style="magenta")

    def run_task(self, task_id: str):
        tweak = self.tweaks.get(task_id)
        if not tweak:
            return

        with Progress(
            SpinnerColumn(spinner_name="dots", style="magenta"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="magenta", finished_style="green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task(f"[cyan]Applying {tweak.name}...", total=100)

            # Simulate progress for visual feedback
            for i in range(50):
                time.sleep(0.02)
                progress.update(task, advance=1)

            success = tweak.apply()

            for i in range(50):
                time.sleep(0.01)
                progress.update(task, advance=1)

        if success:
            console.print(f"[bold green]✓ {tweak.name} applied successfully![/bold green]")
        else:
            console.print(f"[bold red]✗ Failed to apply {tweak.name}.[/bold red]")

        console.input("\n[dim]Press Enter to continue...[/dim]")

    def run(self):
        console.clear()

        while True:
            layout = Layout()
            layout.split_column(
                Layout(self.generate_header(), size=9),
                Layout(name="main")
            )
            layout["main"].split_row(
                Layout(self.generate_dashboard(), ratio=1),
                Layout(self.generate_menu(), ratio=2)
            )

            console.print(layout)

            choice = console.input("\n[bold magenta]Select option > [/bold magenta]").strip().upper()

            if choice == 'Q':
                break
            elif choice in self.tweaks:
                console.clear()
                self.run_task(choice)

            console.clear()

if __name__ == "__main__":
    app = GhostOptimizerUI()
    app.run()
