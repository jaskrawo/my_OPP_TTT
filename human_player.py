class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def chooseMove(self, positions):
        while True:
            try:
                row = int(input("Input your action row (1-3): ")) - 1
                column = int(input("Input your action column (1-3): ")) - 1
                action = (row, column)
                if action in positions:
                    return action
            except ValueError:
                print("Input valid number, try again!")
            print("input valid action position!")

    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass
