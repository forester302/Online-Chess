import os
import socket

import pygame

from Components.Screen.Screen import Screen
from Components.Screen.ScreenObjects.ScreenObject import ScreenObject
from Components.Screen.ScreenObjects.Button import Button
from Components.Screen.ScreenObjects.TextBox import TextBox
from Components.Screen.ScreenObjects.Text import Text
from Components.Screen.ScreenObjects.Image import Image
from Components.Screen.ScreenManager import ScreenManager


def client_main_menu():
    def join_button_clicked():
        ip_ = screen.get_object("ip_text_box").text.text
        username_ = screen.get_object("usn_text_box").text.text
        try:
            port_ = int(screen.get_object("port_text_box").text.text)
        except ValueError:
            return
        with open("lastjoin", "w") as lj:
            lj.write(username_ + "\n")
            lj.write(ip_ + "\n")
            lj.write(str(port_))
        import main
        main.play(username_, ip_, port_)

    with open("lastjoin", "r") as f:
        username, ip, port = f.read().split("\n")

    screen = Screen((500, 500))
    screen.add_object("title_image", Image(10, 10, 480, 100, "images/Title.png"))

    # username input
    screen.add_object("usn_background", ScreenObject(10, 120, 100, 75, (255, 255, 255)))
    screen.add_object("usn_text_box", TextBox(110, 120, 380, 75, colour=(255, 255, 255), newline=False))
    screen.get_object("usn_text_box").text.text = username
    screen.get_object("usn_text_box").make_rect()
    screen.add_object("usn_text", Text("Century", 30, "Name:"))
    screen.get_object("usn_text").position_left((30, 157.5))

    # ip input
    screen.add_object("ip_background", ScreenObject(10, 220, 100, 75, (255, 255, 255)))
    screen.add_object("ip_text", Text("Century", 30, "IP:"))
    screen.get_object("ip_text").position_left((30, 257.5))
    screen.add_object("ip_text_box", TextBox(110, 220, 380, 75, colour=(255, 255, 255), newline=False))
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
    screen.add_object("join_button", Button(10, 400, 480, 75, lambda: join_button_clicked(), colour=(155, 0, 0),
                                            hovercolour=(255, 0, 0)))
    screen.get_object("join_button").add_text("button_text", "Century", 30, "Join", centre=True)
    return screen


def server_main_menu(start_server, gen_new_game, screenmanager):
    def new_game(gen_new_game_, start_server_):
        gen_new_game_()
        pygame.quit()
        start_server_()

    screen = Screen((500, 500))
    screen.add_object("new_game", Button(10, 10, 480, 235, lambda: new_game(gen_new_game, start_server),
                                         colour=(155, 0, 0), hovercolour=(255, 0, 0)))
    screen.get_object("new_game").add_text("button_text", "Century", 70, "New Game", centre=True)
    screen.add_object("load_game",
                      Button(10, 255, 480, 235, lambda: screenmanager.set_screen("load"),
                             colour=(155, 0, 0), hovercolour=(255, 0, 0)))
    screen.get_object("load_game").add_text("button_text", "Century", 70, "Load Game", centre=True)
    return screen


def server_load_screen(load_from_file, start_server):
    def run(load_from_file_, i_, start_server_):
        load_from_file_(i_)
        pygame.quit()
        start_server_()

    screen = Screen((500, 500))
    saves = os.listdir("./Saves")
    for i in range(0, len(saves)):
        screen.add_object(f"save{i}_button",
                          Button(50, 50 + (150 * i), 400, 100, lambda i_=i: run(load_from_file, i_, start_server),
                                 colour=(155, 0, 0), hovercolour=(255, 0, 0)))
        screen.get_object(f"save{i}_button").add_text("button_text", 'Century', 30, saves[i][:-6],
                                                      colour=(0, 0, 0), centre=True)
    return screen


def server_running_menu(port, screenmanager: ScreenManager):
    screen = Screen((500, 500))
    screen.add_object("save_button",
                      Button(50, 50, 400, 300,
                             lambda: screenmanager.set_screen("save"),
                             colour=(155, 0, 0), hovercolour=(255, 0, 0)))
    screen.get_object("save_button").add_text("button_text", 'Century', 50, "Save Game", centre=True)
    screen.add_object("ip_object", ScreenObject(50, 350, 400, 50, (255, 255, 255)))
    screen.get_object("ip_object").add_text("ip_text", 'Century', 30,
                                            f"IP:{socket.gethostbyname(socket.gethostname())}", centre=True,
                                            colour=(0, 0, 0))
    screen.add_object("port_object", ScreenObject(50, 400, 400, 50, (255, 255, 255)))
    screen.get_object("port_object").add_text("port_text", 'Century', 30, f"Port:{port}", centre=True, colour=(0, 0, 0))
    return screen


def server_save_screen(save_to_file, screenmanager):
    def run(save_to_file_, i_, screenmanager_):
        save_to_file_(i_)
        screenmanager_.set_screen("run")

    screen = Screen((500, 500))
    saves = os.listdir("./Saves")
    for i in range(0, len(saves)):
        screen.add_object(f"save{i}_button", Button(50, 50 + (150 * i), 400, 100,
                                                    lambda i_=i: run(save_to_file, i_, screenmanager),
                                                    colour=(155, 0, 0), hovercolour=(255, 0, 0)))
        screen.get_object(f"save{i}_button").add_text("button_text", 'Century', 30, saves[i][:-6],
                                                      colour=(0, 0, 0), centre=True)
    return screen
