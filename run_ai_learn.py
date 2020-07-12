from ai.game_simulator import GameSimulator
import os
import sys

destination_path = os.getcwd() + "/ai/games.csv"

number_of_games = sys.argv[1] if len(sys.argv) > 1 else 1000
    
GameSimulator().simulateAndSave(number_of_games, destination_path)