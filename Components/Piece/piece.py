from Components.Piece.piececlass import Piece


# class representing a pawn in a chess game
class Pawn(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def possible_moves(self, board):
        # list to store the possible moves
        moves = []

        # move one square forward
        currentmove = [self.x, self.y - 1]
        # set the canmove flag to True
        canmove = True
        # check if there is a piece blocking the move
        for piece in board.pieces + board.otherpieces:
            if piece.x == currentmove[0] and piece.y == currentmove[1]:
                canmove = False
        # if the move is not blocked, add it to the list of possible moves
        if canmove:
            moves.append(currentmove)
            # only check two squares forward if one square forward is clear
            if not self.has_moved:
                # move two squares forward
                currentmove = [self.x, self.y - 1 - 1]
                # reset the canmove flag
                canmove = True
                # check if there is a piece blocking the move
                for piece in board.pieces + board.otherpieces:
                    if piece.x == currentmove[0] and piece.y == currentmove[1]:
                        canmove = False
                # if the move is not blocked, add it to the list of possible moves
                if canmove:
                    moves.append(currentmove)

        # check the taking moves
        takingmoves = [[self.x - 1, self.y - 1], [self.x + 1, self.y - 1]]
        for currentmove in takingmoves:
            for piece in board.otherpieces:
                if piece.x == currentmove[0] and piece.y == currentmove[1]:
                    moves.append(currentmove)

        # return the list of possible moves
        return self.adjust_moves(moves, board)

    def attack_moves(self, board):
        return [[self.x + 1, self.y + 1], [self.x - 1, self.y + 1]]

    def move(self, board, network):
        moved = super().move(board, network)
        if not moved:
            return moved
        if not self.y == 0:
            return moved

        # promotion
        from Components.Board import promotion
        promotion(self, board, network)
        return moved


# class representing a rook in a chess game
class Rook(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def attack_moves(self, board, enemy: bool = None):
        # get a list of all possible straight moves for the rook
        return self.get_moves_straight(board)

    def possible_moves(self, board):
        return self.adjust_moves(self.attack_moves(board), board)


# class representing a bishop in a chess game
class Bishop(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def attack_moves(self, board):
        # get a list of all possible diagonal moves for the bishop
        return self.get_moves_diagonal(board)

    def possible_moves(self, board):
        return self.adjust_moves(self.attack_moves(board), board)


# class representing a knight in a chess game
class Knight(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def attack_moves(self, board):
        return [[self.x - 1, self.y - 2], [self.x + 1, self.y - 2],
                [self.x - 1, self.y + 2], [self.x + 1, self.y + 2],
                [self.x - 2, self.y - 1], [self.x + 2, self.y - 1],
                [self.x - 2, self.y + 1], [self.x + 2, self.y + 1]]

    def possible_moves(self, board):
        return self.adjust_moves(self.attack_moves(board), board)


# class representing a queen in a chess game
class Queen(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def attack_moves(self, board, enemy: bool = None):
        return self.get_moves_straight(board) + self.get_moves_diagonal(board)

    def possible_moves(self, board):
        return self.adjust_moves(self.attack_moves(board), board)




# class representing a king in a chess game
class King(Piece):
    def __init__(self, pos, d):
        # call the parent class's __init__ method to initialize the piece
        super().__init__(pos, d)

    def is_in_check(self, board, currentmove):
        # Calculate the list of enemy moves after the current move is made
        enemy_moves = self.enemy_moves(board, currentmove)
        # Check if the current position of the king is in the list of enemy moves
        if [self.x, self.y] in enemy_moves:
            # If the current position of the king is in the list of enemy moves, return True
            return True
        # If the current position of the king is not in the list of enemy moves, return False
        return False

    def enemy_moves(self, board, currentmove):
        # List to hold the enemy moves
        moves = []
        # Iterate over the enemy pieces
        for piece in board.otherpieces:
            # Skip the current iteration if the current position of the enemy piece is the same as the current move
            if piece.x == currentmove[0] and piece.y == currentmove[1]:
                continue
            # Calculate the attack moves of the enemy piece
            moves += piece.attack_moves(board)
        # Return the list of enemy moves
        return moves

    def attack_moves(self, board):
        return [[self.x - 1, self.y - 1], [self.x, self.y - 1],
                [self.x + 1, self.y - 1], [self.x + 1, self.y],
                [self.x + 1, self.y + 1], [self.x, self.y + 1],
                [self.x - 1, self.y + 1], [self.x - 1, self.y]]

    def possible_moves(self, board):
        # list to store the possible moves
        moves = self.attack_moves(board)
        if not self.has_moved and not self.is_in_check(board, [-10,-10]):
            for d in (1, -1):
                cantmove = False
                for piece in board.pieces + board.otherpieces:
                    if self.x+(1*d) == piece.x and self.y == piece.y:
                        cantmove = True
                for piece in board.pieces + board.otherpieces:
                    if self.x+(2*d) == piece.x and self.y == piece.y:
                        cantmove = True
                for piece in board.pieces + board.otherpieces:
                    if self.x+(3*d) == piece.x and self.y == piece.y:
                        if not piece.__class__.__name__ == "Rook" or piece.has_moved:
                            cantmove = True
                for piece in board.pieces:
                    if self.x+(4*d) == piece.x and self.y == piece.y:
                        if not piece.__class__.__name__ == "Rook" or piece.has_moved:
                            cantmove = True
                if not cantmove:
                    moves.append([self.x+(2*d), self.y])
        # return the list of possible moves
        return self.adjust_moves(moves, board)

    def move(self, board, network):
        if self.selected:
            lastclick = board.board.lastclick
            for move in self.pos_moves:
                if move[0] == lastclick[0] and move[1] == lastclick[1]:
                    if self.__class__.__name__ == "King" and (self.y == 0 or self.y == 7):
                        if abs(self.x - lastclick[0]) > 1:
                            if self.x - lastclick[0] > 0:
                                x = 1
                            else:
                                x = -1
                            done = False
                            for piece in board.pieces:
                                if piece.x == self.x - x - x and piece.y == self.y and piece.__class__.__name__ == "Rook":
                                    piece.x = lastclick[0] + x
                                    board.board[self.x - x - x][self.y].image = None
                                    piece.place_piece(board)
                                    done = True
                            if not done:
                                for piece in board.pieces:
                                    if piece.x == self.x - x - x - x and piece.y == self.y and piece.__class__.__name__ == "Rook":
                                        piece.x = lastclick[0] + x
                                        board.board[self.x - x - x -x][self.y].image = None
                                        piece.place_piece(board)
                                        done = True
                            if not done:
                                for piece in board.pieces:
                                    if piece.x == self.x - x - x - x - x and piece.y == self.y and piece.__class__.__name__ == "Rook":
                                        piece.x = lastclick[0] + x
                                        board.board[self.x - x - x - x -x][self.y].image = None
                                        piece.place_piece(board)
                                        done = True
                    return super().move(board, network)
