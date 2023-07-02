from typing import Any, Dict, List, Optional, TypeVar
from uuid import uuid4
from dataclasses import dataclass
from rich.text import Text

T = TypeVar("T", bound="Model")


@dataclass
class Result:
    """
    Response class to return result of an operation
    """

    ok: bool
    cancel_op: bool
    message: Optional[str] = None
    color: str = "white"

    @classmethod
    def Ok(cls, message: Optional[str] = None):
        return cls(True, False, message, "green")

    @classmethod
    def Warn(cls, message: Optional[str] = None):
        return cls(False, False, message, "yellow")

    @classmethod
    def Err(cls, message: str):
        return cls(False, True, message, "red")

    def is_ok(self) -> bool:
        return self.ok

    def is_err(self) -> bool:
        return not self.ok

    def text(self):
        def colored(a, b):
            return f"[{b}]{a}[/{b}]"

        if self.message:
            return colored(self.message, self.color)

        return Text()


Ok = Result.Ok
Err = Result.Err
Warn = Result.Warn


class Model:
    """
    Model class to for the base tree structure
    """

    fields: List
    sortable_fields: List

    def __init__(
        self,
        parent: Optional["Model"] = None,
    ) -> None:
        self.name = str(uuid4())
        self.parent = parent

    @property
    def kind(self):
        return self.__class__.__name__.lower()

    @property
    def path(self):
        """
        Unique path for model
        """

        return "$"

    def _get_children(self, kind: str) -> List:
        """
        Get children list (workspace/todo)
        """
        pass

    def _get_child_index(self, kind: str, **kwargs) -> int:
        """
        Get child index by attr
        """

        key, value = list(kwargs.items())[0]
        for i, j in enumerate(self._get_children(kind)):
            if getattr(j, key) == value:
                return i

        return -1

    def _get_index(self, kind: str) -> int:
        """
        Get items's index among it's siblings
        """

        if not self.parent:
            return -1

        return self.parent._get_child_index(kind, name=self.name)

    def edit(self, key: str, value: str) -> Result:
        """
        Edit item's attrs
        """

        var = f"_{key}"
        if hasattr(self, var):
            return getattr(self, var).set(value)
        else:
            return Err("Invalid Request!")

    def shift_up(self) -> None:
        """
        Shift the item one place up among its siblings
        """

        idx = self._get_index(self.kind)

        if idx in [0, -1]:
            return

        if not self.parent:
            return
        arr = self.parent._get_children(self.kind)
        arr[idx], arr[idx - 1] = arr[idx - 1], arr[idx]

    def shift_down(self) -> None:
        """
        Shift the item one place down among its siblings
        """

        idx = self._get_index(self.kind)

        if idx == -1 or not self.parent:
            return

        arr = self.parent._get_children(self.kind)
        if idx == len(arr) - 1:
            return

        arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]

    def prev_sibling(self: T) -> Optional[T]:
        """
        Returns previous sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(self.kind, name=self.name)

        if idx:
            return self._get_children(self.kind)[idx - 1]

    def next_sibling(self: T) -> Optional[T]:
        """
        Returns next sibling item, if any, else None
        """

        if not self.parent:
            return

        idx = self.parent._get_child_index(self.kind, name=self.name)
        arr = self.parent._get_children(self.kind)

        if idx < len(arr) - 1:
            return arr[idx + 1]

    def add_sibling(self: T, inherit: bool = False) -> T:
        """
        Add item sibling
        """

        if self.parent:
            idx = self.parent._get_child_index(self.kind, name=self.name)
            return self.parent.add_child(self.kind, idx + 1, inherit)
        else:
            raise TypeError("Cannot add sibling")

    def add_child(self, kind: str, index: int = 0, inherit: bool = False) -> Any:
        """
        Adds a child to specified index (Defaults to first position)
        """
        pass

    def remove_child(self, kind: str, name: str) -> Any:
        """
        Remove the child based on attr
        """

        idx = self._get_child_index(kind, name=name)
        if idx != -1:
          return self._get_children(kind).pop(idx)

    def drop(self) -> None:
        """
        Delete the item
        """

        if self.parent:
            self.parent.remove_child(self.kind, self.name)

    def sort(self, attr: str) -> None:
        """
        Sort the children based on specific attr
        """

        if self.parent:
            children = self.parent._get_children(self.kind)
            children.sort(key=lambda x: getattr(x, f"_{attr}").get_sortable())

    def commit(self) -> Dict[str, Any]:
        """
        Get a object summary that can be stored
        """
        pass

    def from_data(self, data: Dict[str, Any]) -> None:
        """
        Fill in the attrs from data provided
        """
        pass
