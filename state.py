import numpy as np
import dimensions


class State:
    def __init__(self, player1, player2):
        self.BOARD_ROWS = dimensions.BOARD_ROWS
        self.BOARD_COLUMNS = dimensions.BOARD_COLUMNS
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLUMNS))
        self.isEnd = False
        self.boardHash = None
        self.playerSymbol = 1
        self.player1 = player1
        self.player2 = player2

    def winner(self):
        for i in range(self.BOARD_ROWS):
            if sum(self.board[i, :]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3:
                self.isEnd = True
                return -1
        for i in range(self.BOARD_COLUMNS):
            if sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1
        diagonal1 = sum(
            [self.board[i, i]
                for i in range(self.BOARD_COLUMNS)])
        diagonal2 = sum(
            [self.board[i, self.BOARD_COLUMNS-i-1]
                for i in range(self.BOARD_COLUMNS)])
        diag_sum = max(abs(diagonal1), abs(diagonal2))
        if diag_sum == 3:
            self.isEnd = True
            if diagonal1 == 3 or diagonal2 == 3:
                return 1
            else:
                return -1

        if len(self.availablePositions()) == 0:
            self.isEnd = True
            return 0
        self.isEnd = False
        return None

    def getHash(self):
        boardHash = str(self.board.reshape(
            self.BOARD_ROWS
            * self.BOARD_COLUMNS))
        return boardHash

    def availablePositions(self):
        positions = []
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLUMNS):
                if self.board[i, j] == 0:
                    positions.append((i, j))
        return positions

    def updateBoard(self, position):
        self.board[position] = self.playerSymbol
        self.playerSymbol = -1 if self.playerSymbol == 1 else 1

    def giveReward(self):
        result = self.winner()
        if result == 1:
            self.player1.feedReward(1)
            self.player2.feedReward(0)
        elif result == -1:
            self.player1.feedReward(0)
            self.player2.feedReward(1)
        else:
            self.player1.feedReward(0.1)
            self.player2.feedReward(0.5)

    def train(self, rounds=1000):
        for i in range(rounds):
            if i % 100 == 0:
                print(f'Round {i}')
            while not self.isEnd:
                positions = self.availablePositions()
                player1_move = self.player1.chooseMove(
                    positions, self.board, self.playerSymbol)
                self.updateBoard(player1_move)
                board_hash = self.getHash()
                self.player1.addState(board_hash)

                win = self.winner()
                if win is not None:
                    self.giveReward()
                    self.player1.reset()
                    self.player2.reset()
                    self.reset()
                    break

                else:
                    positions = self.availablePositions()
                    player2_move = self.player2.chooseMove(
                        positions, self.board, self.playerSymbol)
                    self.updateBoard(player2_move)
                    board_hash = self.getHash()
                    self.player2.addState(board_hash)

                    win = self.winner()
                    if win is not None:
                        self.giveReward()
                        self.player1.reset()
                        self.player2.reset()
                        self.reset()
                        break

    def play(self):
        while not self.isEnd:
            positions = self.availablePositions()
            player1_move = self.player1.chooseMove(
                positions, self.board, self.playerSymbol)
            self.updateBoard(player1_move)
            board_hash = self.getHash()
            self.player1.addState(board_hash)
            self.printBoard()

            win = self.winner()
            if win is not None:
                if win == 1:
                    print(self.player1.name, "wins!")
                else:
                    print("It is a Tie!")
                self.reset()
                break

            else:
                positions = self.availablePositions()
                player2_move = self.player2.chooseMove(positions)
                self.updateBoard(player2_move)

                win = self.winner()
                if win is not None:
                    if win == -1:
                        print(self.player2.name, "wins!")
                    else:
                        print("It is a Tie!")
                    self.reset()
                    break

    def reset(self):
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLUMNS))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    def printBoard(self):
        for i in range(self.BOARD_ROWS):
            print("#############")
            row = "# "
            for j in range(self.BOARD_COLUMNS):
                if self.board[i, j] == 1:
                    token = "X"
                elif self.board[i, j] == -1:
                    token = "O"
                else:
                    token = " "
                row += token + " # "
            print(row)
        print("#############")
