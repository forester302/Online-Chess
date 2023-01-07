from Components.Board import Board


class Popup:
    def __init__(self, name, image, pos, size):
        self.name = name
        self.image = image
        self.location = pos
        self.size = size

    def popup(self, board: Board):
        # for the chess game the popup only needs to show until the player clicks on a piece.
        # when a piece is clicked the board is redrawn
        board.board.set_ui("popup", self.image, self.location, self.size)
        board.board.draw()
        board.board.del_ui("popup")


popups = {
    "Check": Popup("Check", "images/check.png", (150, 225), (300, 150)),
    "Checkmate": Popup("Checkmate", "images/checkmate.png", (150, 225), (300, 150)),
    "Stalemate": Popup("Stalemate", "images/stalemate.png", (75, 225), (450, 150)),
    "WinCheckmate": Popup("WinCheckmate", "images/wincheckmate.png", (150, 225), (300, 150))
}
