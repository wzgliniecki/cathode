from rich.panel import Panel
from rich.table import Table

from cathode.converters import CONVERTERS

class EffectsLayout:
    def __init__(self, current_converter: str, current_effects: (str) | None = None):
        self.current_converter = current_converter
        self.converter_classes = CONVERTERS
        self.current_effects = current_effects

    def update(self, user_input: str | None):
        if user_input is not None:
            self.next_converter()


    def next_converter(self):
        if self.current_converter == "ascii":
            self.current_converter = "color_blocks"
        else:
            self.current_converter = "ascii"


    def get_panel(self) -> Panel:
        table = Table(show_header=False, box=None)
        for name in self.converter_classes.keys():
            style = "bold green" if name == self.current_converter else "dim"
            table.add_row(f"[{style}]{name}[/{style}]")
        return Panel(table, title="Effects")
