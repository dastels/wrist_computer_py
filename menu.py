import board

# ---------- Sound Effects ------------- #
error_sound = "/sounds/sound.wav"
beep_sound = "/sounds/beep.wav"
tab_sound = "/sounds/tab.wav"


class MenuItem(object):
    def __init__(self, text, nested_menu=None, function=None):
        self._text = text
        self._nested_menu = nested_menu
        self._function = function
        self._selected = False

    @property
    def text(self):
        return self._text

    @property
    def is_nested(self):
        return self._nested_menu is not None

    @property
    def menu(self):
        return self._nested_menu

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, val):
        self._selected = val

    @property
    def function(self):
        return self._function


class Menu(object):
    def __init__(self, pyportal, menu_group, parent=None):
        self._pyportal = pyportal
        self._group = menu_group
        self._items = []
        self._parent = parent
        self._current_item_index = 0
        self._top_item_index = 0
        self._bottom_group_index = (len(menu_group) / 2) - 1

    @property
    def items(self):
        """Hands off!"""
        return None

    @items.setter
    def items(self, items):
        self._items = items

    def reset(self):
        self._current_item_index = 0
        for i in self._items:
            i.selected = False
        if len(self._items) > 0:
            self._items[0].selected = True

    def redraw(self):
        for row in range(len(self._group) / 2):
            item_index = row + self._top_item_index

            # set select indicator
            if item_index < len(self._items) and self._items[item_index].selected:
                self._group[row * 2].text = ">"
            else:
                self._group[row * 2].text = ""

            # set text
            if item_index < len(self._items):
                self._group[row * 2 + 1].text = self._items[item_index].text + (
                    " >" if self._items[item_index].is_nested else ""
                )
            else:
                self._group[row * 2 + 1].text = ""

    def up(self):
        if self._current_item_index > 0:
            if self._current_item_index == self._top_item_index:
                self._top_item_index -= 1
            self._items[self._current_item_index].selected = False
            self._current_item_index -= 1
            self._items[self._current_item_index].selected = True
            self.redraw()
        else:
            self._pyportal.play_file(error_sound)

    def down(self):
        if self._current_item_index < len(self._items) - 1:
            if (
                self._current_item_index - self._top_item_index
                == self._bottom_group_index
            ):
                self._top_item_index += 1
            self._items[self._current_item_index].selected = False
            self._current_item_index += 1
            self._items[self._current_item_index].selected = True
            self.redraw()
        else:
            self._pyportal.play_file(error_sound)

    def right(self):
        item = self._items[self._current_item_index]
        if item.is_nested:
            item.menu.reset()
            item.menu.redraw()
            return item.menu
        else:
            if item.function is not None:
                item.function()
            return self

    def left(self):
        if self._parent is not None:
            self._parent.redraw()
            return self._parent
        else:
            return self
