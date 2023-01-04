from Components.Screen.Screen import Screen


class ScreenManager:
    _screens: dict[str, Screen] = {}
    current_screen: str = None

    def add_screen(self, name: str, screen: Screen):
        self._screens[name] = screen

    def del_screen(self, name:str):
        self._screens.pop(name)

    def set_screen(self, name: str, screen: Screen = None):
        if screen is not None:
            self.add_screen(name, screen)
        self.current_screen = name
        self._screens[self.current_screen].make_screen()

    def get_screen(self, name: str):
        return self._screens[name]

    def draw(self):
        self._screens[self.current_screen].draw()

    def tick(self):
        self._screens[self.current_screen].tick()

    def check_open(self):
        return self._screens[self.current_screen].check_open()
