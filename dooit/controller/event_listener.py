from textual.app import App
from textual import events
from dooit.ui.events.events import ExitApp
from dooit.ui.events import (
    TopicSelect,
    SwitchTab,
    ApplySortMethod,
    ChangeStatus,
    Notify,
    SpawnHelp,
)
from dooit.ui.widgets import HelpScreen
from dooit.ui.css.screen import screen_CSS
from dooit.controller.controller import Controller

class EventListener(App):
    CSS = screen_CSS
    SCREENS = {"help": HelpScreen(name="help")}
    controller = Controller()

    async def on_load(self):
      self.controller.create_widgets()

    async def on_mount(self):
      self.controller.set_environment()
      self.set_interval(1, self.poll)

    async def poll(self):
      if self.controller.has_changed():
        if (self.controller.refresh_model_data()):
          await self.controller.refresh_view_data()

    def compose(self):
      yield from self.controller.generate_widgets()

    async def action_quit(self) -> None:
      self.controller.commit()
      return await super().action_quit()

    async def on_key(self, event: events.Key) -> None:
        if self.controller.navbar.has_focus:
            await self.controller.navbar.handle_key(event)
        else:
            await self.controller.todos.handle_key(event)

    async def on_topic_select(self, event: TopicSelect):
        await self.controller.todos.update_table(event.item)

    async def on_switch_tab(self, _: SwitchTab):
      self.controller.switch_tab()

    async def on_apply_sort_method(self, event: ApplySortMethod):
        w = event.widget_obj
        w.sort(attr=event.method)

    async def on_change_status(self, event: ChangeStatus):
        self.controller.bar.set_status(event.status)

    async def on_notify(self, event: Notify):
        self.controller.bar.set_message(event.message)

    async def on_spawn_help(self, event: SpawnHelp):
        self.push_screen("help")

    async def on_exit_app(self, event: ExitApp):
        await self.action_quit()
