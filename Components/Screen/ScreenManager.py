from Components.Screen.Screen import Screen


class ScreenManager:
    _screens: dict[str, Screen] = {}
    current_screen: str = None

    def add_screen(self, name: str, screen: Screen):
        # Add a new screen to the screen dictionary
        self._screens[name] = screen

    def del_screen(self, name:str):
        # Remove a screen from the screen dictionary
        self._screens.pop(name)

    def set_screen(self, name: str, screen: Screen = None):
        # Set the current screen, hiding the previous one and showing the new one
        if self.current_screen is not None:
            self._screens[self.current_screen].hide_screen()
        if screen is not None:
            self.add_screen(name, screen)
        self.current_screen = name
        self._screens[self.current_screen].make_screen()

    def get_screen(self, name: str):
        # Get a screen from the screen dictionary
        return self._screens[name]

    def draw(self):
        # Draw the current screen
        self._screens[self.current_screen].draw()

    def tick(self):
        # Increment the clock on the current screen
        self._screens[self.current_screen].tick()

    def check_open(self):
        # Check if the current screen is open and handle events
        return self._screens[self.current_screen].check_open()
