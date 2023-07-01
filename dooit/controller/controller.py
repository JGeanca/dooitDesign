from dooit.api.manager import Manager
from dooit.utils.watcher import Watcher
from dooit.ui.widgets import WorkspaceTree, TodoTree, StatusBar 


class Controller():
  manager = Manager()
  
  def create_widgets(self):
    self.navbar = WorkspaceTree()
    self.todos = TodoTree()
    self.bar = StatusBar()

  def set_environment(self):
    self.watcher = Watcher()
    self.current_focus = "navbar"
    self.navbar.toggle_highlight()

  def has_changed(self):
    return (not self.manager.is_locked() and self.watcher.has_modified())

  def refresh_model_data(self):
    return self.manager.refresh_data()

  def refresh_view_data(self):
    return self.navbar._refresh_data()

  def refresh_data(self):
    if not self.manager.is_locked() and self.watcher.has_modified():
      if (self.manager.refresh_data()):
        return self.navbar._refresh_data()
  
  def generate_widgets(self):
    yield self.navbar
    yield self.todos
    yield self.bar
    
  def commit(self):
    self.manager.commit()

  def update_table(self, event):
    return self.todos.update_table(event.item)

  def switch_tab(self):
    self.navbar.toggle_highlight()
    self.todos.toggle_highlight()
