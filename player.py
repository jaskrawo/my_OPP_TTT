import numpy as np
import pickle
import dimensions


class Player:
    def __init__(self, name, explore_rate=0.2):
        self.BOARD_ROWS = dimensions.BOARD_ROWS
        self.BOARD_COLUMNS = dimensions.BOARD_COLUMNS
        self.name = name
        self.states = []
        self.lr = 0.3
        self.explore_rate = explore_rate
        self.decay_gamma = 0.9
        self.states_value = {}

    def getHash(self, board):
        boardHash = str(board.reshape(self.BOARD_ROWS * self.BOARD_COLUMNS))
        return boardHash

    def chooseMove(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.explore_rate:
            index = np.random.choice(len(positions))
            move = positions[index]
        else:
            value_max = -99
            for position in positions:
                next_board = current_board.copy()
                next_board[position] = symbol
                next_boardHash = self.getHash(next_board)
                if self.states_value.get(next_boardHash) is None:
                    value = 0
                else:
                    value = self.states_value.get(next_boardHash)
                if value >= value_max:
                    value_max = value
                    move = position
        return move

    def addState(self, state):
        self.states.append(state)

    def feedReward(self, reward):
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.lr * (
                                                self.decay_gamma
                                                * reward
                                                - self.states_value[state]
                                                )
            reward = self.states_value[state]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()
