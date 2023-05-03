from simulation import Simulation


if __name__ == "__main__":
    ## Initialize Simulation

    simulation = Simulation()

    ####### SIMULATION LOOP #######

    # start the game
    simulation.startGame()

    while True:
        # process a round
        simulation.processRound()
