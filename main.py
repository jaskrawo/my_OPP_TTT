import state
import player
import human_player


if __name__ == "__main__":
    player1 = player.Player("player1")
    player2 = player.Player("player2")
    training_state = state.State(player1, player2)
    training_state.train(1300)
    player1.savePolicy()
    player2.savePolicy()

    computer = player.Player("Computer", explore_rate=0)
    computer.loadPolicy("policy_player1")
    human = human_player.HumanPlayer("Human")
    playing_state = state.State(computer, human)
    playing_state.play()
