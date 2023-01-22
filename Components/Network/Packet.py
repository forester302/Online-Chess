from Components.Piece.piece import Pawn, Rook, Knight, Bishop, Queen, King


class Player:
    pieces = None

    def __init__(self, side, is_turn: bool, name: str = None):
        self.side = side
        self.is_turn = is_turn
        self.name = name

    def gen_pieces(self):
        # generates a list of all the pieces and their positions on the board
        if self.side == -1:
            king = King((4, 7), self.side)
            queen = Queen((3, 7), self.side)
        else:
            king = King((3, 7), self.side)
            queen = Queen((4, 7), self.side)
        pawn1 = Pawn((0, 6), self.side)
        pawn2 = Pawn((1, 6), self.side)
        pawn3 = Pawn((2, 6), self.side)
        pawn4 = Pawn((3, 6), self.side)
        pawn5 = Pawn((4, 6), self.side)
        pawn6 = Pawn((5, 6), self.side)
        pawn7 = Pawn((6, 6), self.side)
        pawn8 = Pawn((7, 6), self.side)
        bishop1 = Bishop((2, 7), self.side)
        bishop2 = Bishop((5, 7), self.side)
        knight1 = Knight((1, 7), self.side)
        knight2 = Knight((6, 7), self.side)
        rook1 = Rook((0, 7), self.side)
        rook2 = Rook((7, 7), self.side)
        # self.pieces = [king, pawn4]
        self.pieces = [king, bishop1, bishop2, knight1, knight2, pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8,
                       queen, rook1, rook2]


# EndGame of either Checkmate or Stalemate
class EndGame:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"EndGame of Type {self.type}"


class Quit:
    def __repr__(self):
        return "Quit"


class Check:
    def __repr__(self):
        return "Check"


class UpdateRequest:
    def __repr__(self):
        return "Update"


class NoUpdatesAvailable:
    def __repr__(self):
        return "No Updates Available"


class UsernameRequest:
    def __repr__(self):
        return "Username Request"


class Username:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class UsernameDenied:
    def __repr__(self):
        return "Username Denied"
