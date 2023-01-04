from Components.Screen.Screen import Screen
from Components.Screen.ScreenObjects.ScreenObject import ScreenObject
from Components.Screen.ScreenObjects.Button import Button
from Components.Screen.ScreenObjects.TextBox import TextBox
from Components.Screen.ScreenObjects.Text import Text
from Components.Screen.ScreenObjects.Image import Image


def client_main_menu():
    def join_button_clicked():
        ip = screen.get_object("ip_text_box").text.text
        username = screen.get_object("usn_text_box").text.text
        try:
            port = int(screen.get_object("port_text_box").text.text)
        except:
            return
        with open("lastjoin", "w") as f:
            f.write(username + "\n")
            f.write(ip + "\n")
            f.write(str(port))
        import main
        main.play(username, ip, port)

    with open("lastjoin", "r") as f:
        username, ip, port = f.read().split("\n")

    screen = Screen((500, 500))
    screen.add_object("title_image", Image(10, 10, 480, 100, "images/Title.png"))

    # username input
    screen.add_object("usn_background", ScreenObject(10, 120, 100, 75, (255, 255, 255)))
    screen.add_object("usn_text_box",
                      TextBox(110, 120, 380, 75, colour=(255, 255, 255), newline=False))
    screen.get_object("usn_text_box").text.text = username
    screen.get_object("usn_text_box").make_rect()
    screen.add_object("usn_text", Text("Century", 30, "Name:"))
    screen.get_object("usn_text").position_left((30, 157.5))

    # ip input
    screen.add_object("ip_background", ScreenObject(10, 220, 100, 75, (255, 255, 255)))
    screen.add_object("ip_text", Text("Century", 30, "IP:"))
    screen.get_object("ip_text").position_left((30, 257.5))
    screen.add_object("ip_text_box",
                      TextBox(110, 220, 380, 75, colour=(255, 255, 255), newline=False))
    screen.get_object("ip_text_box").text.text = ip
    screen.get_object("ip_text_box").make_rect()

    # port input
    screen.add_object("port_background", ScreenObject(10, 300, 100, 75, (255, 255, 255)))
    screen.add_object("port_text", Text("Century", 30, "Port:"))
    screen.get_object("port_text").position_left((30, 337.5))
    screen.add_object("port_text_box",
                      TextBox(110, 300, 380, 75, colour=(255, 255, 255), newline=False, characterlimit=5))
    screen.get_object("port_text_box").text.text = port
    screen.get_object("port_text_box").make_rect()

    # submit button
    screen.add_object("join_button", Button(10, 400, 480, 75,
                                            lambda: join_button_clicked(),
                                            colour=(155, 0, 0), hovercolour=(255, 0, 0)))
    screen.get_object("join_button").add_text("button_text", "Century", 30, "Join", centre=True)
    return screen


def server_main_menu():
    pass


def server_load_screen():
    pass


def server_running_menu():
    pass


def server_save_screen():
    pass
