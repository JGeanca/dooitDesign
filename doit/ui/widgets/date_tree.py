import datetime
from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode

from . import TreeEdit


class DateTree(TreeEdit):
    # async def edit_current_node(self) -> None:
    #     pass

    async def validate(self, day, month, year) -> bool:
        try:
            datetime.datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            return False

    async def handle_key(self, key: str) -> None:
        if key == "d":
            await self.edit_current_node()

        return await super().handle_key(key)

    def render_node(self, node: TreeNode) -> RenderableType:

        color = "yellow"

        # setup text
        if data := node.data:
            label = Text(str(data.todo.due))
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"
        else:
            label = Text()

        if not label.plain:
            label = Text("No due date")

        # fix padding
        label = Text(" ") + label
        label.plain += " " * (13 - len(label.plain))
        if node.id == self.highlighted:
            label.stylize("bold reverse blue")

        # setup pre-icons
        label = Text.from_markup(f"[{color}]   [/{color}]") + label

        return label