from typing import Dict
from dooit.api import Todo
from dooit.utils.conf_reader import Config
from .formatter import Formatter




class TodoFormatter(Formatter):
    model_type = Todo
    def __init__(self, format):
        super().__init__(format)
        self.c = Config()
        self.RED = self.c.get("red")
        self.GREEN = self.c.get("green")
        self.YELLOW = self.c.get("yellow")
        self.ORANGE = self.c.get("orange")
        self.DURATION_LEGEND = {
            "m": "minute",
            "h": "hour",
            "d": "day",
            "w": "week",
        }

    def todo_highlight(self, text: str, is_highlighted: bool, todo: Todo):
        color = self.status_color(todo)
        if is_highlighted:
            return self.colored(text, "b " + color)
        else:
            return self.colored(text, "d " + color)

    def status_color(self, todo: Todo):
        status = todo.status
        if status == "COMPLETED":
            return self.GREEN
        elif status == "PENDING":
            return self.YELLOW
        else:
            return self.RED

    def style_description(
        self,
        item: model_type,
        is_highlighted: bool,
        editing: str,
        kwargs: Dict[str, str],
    ) -> str:
        text = kwargs["description"]

        if item.status == "COMPLETED":
            text = self.colored(text, "strike")

        # STATUS ICON
        status_icon = item.status.lower() + "_icon"
        status_icon = self.format[status_icon]
        text = self.colored(status_icon, self.status_color(item)) + text

        # DESCRIPTION
        if children := item.todos:
            d = {
                "total": len(children),
                "done": sum(i.status == "COMPLETED" for i in children),
                "remaining": sum(i.status != "COMPLETED" for i in children),
            }
            text += self.format["children_hint"].format(**d)

        # EFFORT
        if effort := kwargs["effort"]:
            icon = self.format["effort_icon"]
            color = self.format["effort_color"]
            text += self.color_combo(icon, effort, color)

        # TAGS
        if tags := kwargs["tags"]:
            tags = [i.strip() for i in kwargs["tags"].split(",")]
            icon = self.format["tags_icon"]
            seperator = self.format["tags_seperator"]
            color = self.format["tags_color"]
            t = f" {icon}"

            if seperator == "comma":
                t += ", ".join(tags)
            elif seperator == "pipe":
                t += " | ".join(tags)
            else:
                t += f" {icon}".join(tags)

            text += self.colored(t, color)

        # RECURRENCE
        if recurrence := kwargs["recurrence"]:

            if recurrence:
                if editing != "recurrence" or not is_highlighted:
                    frequency, value = recurrence[:-1], recurrence[-1]
                    recurrence = f"{frequency} {self.DURATION_LEGEND.get(value)}"
                    if frequency != "1":
                        recurrence += "s"

            color = self.format["recurrence_color"]
            icon = self.format["recurrence_icon"]
            text += self.color_combo(icon, recurrence, color)

        if self.format["color_todos"]:
            return self.todo_highlight(text, is_highlighted, item)
        else:
            return self.cursor_highlight(text, is_highlighted, editing)

    def style_due(
        self,
        item: model_type,
        is_highlighted: bool,
        editing: str,
        kwargs: Dict[str, str],
    ) -> str:
        icon_color = self.status_color(item)
        text = self.colored(self.format["due_icon"], icon_color)
        if item.status == "COMPLETED":
            text += self.colored(kwargs["due"], "strike")
        else:
            text += kwargs["due"]

        if self.format["color_todos"]:
            return self.todo_highlight(text, is_highlighted, item)
        else:
            return self.cursor_highlight(text, is_highlighted, editing)

    def style_urgency(
        self,
        item: model_type,
        is_highlighted: bool,
        editing: str,
        kwargs: Dict[str, str],
    ) -> str:
        val = item.urgency
        if val == 3:
            color = self.ORANGE
        elif val == 2:
            color = self.YELLOW
        elif val == 1:
            color = self.GREEN
        else:
            color = self.RED

        if item.status == "COMPLETED":
            color = "strike " + color

        icon = f"urgency{val}_icon"
        icon = self.format[icon]

        return self.colored(icon, color)
