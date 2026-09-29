"""
easy_terminal is meant to make it easy to get styled output in the terminal.
"""


from rich.console import Console


class EasyTerminal:
    def __init__(self, text: str):
        self.text = text
        self.color = "#ffffff"
        self.bg_color = None
        self.color_scheme = None


    def set_color(self, color: str):
        self.color = color
        return self


    def set_bg_color(self, color: str):
        self.bg_color = color
        return self


    def _check_color_scheme(self):
        if self.color is not None and self.bg_color is not None:
            self.color_scheme = f"{self.color} on {self.bg_color}"
        else:
            self.color_scheme = self.color
        return self


    def show(self):
        self._check_color_scheme()
        c = Console()
        c.print(self.text, style=self.color_scheme)


if __name__ == "__main__":
    text1 = EasyTerminal("Hello World").set_bg_color("blue")
    text1.show()
