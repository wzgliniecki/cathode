from rich.panel import Panel
from rich.table import Table

from cathode.converters import CONVERTERS

class EffectsLayout:
    def __init__(self):
        self.converter_classes = CONVERTERS

    def get_layout(self, current_converter_name: str) -> Panel:
        table = Table(show_header=False, box=None)
        for name in self.converter_classes.keys():
            style = "bold green" if name == current_converter_name else "dim"
            table.add_row(f"[{style}]{name}[/{style}]")
        return Panel(table, title="Effects")
