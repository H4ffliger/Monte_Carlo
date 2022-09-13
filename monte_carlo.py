from gamefield_min_max import GameField
import numpy as np
from copy import deepcopy
import time



#GPU stuff
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

#Introduction
import pyfiglet
ascii_banner = pyfiglet.figlet_format("GNeuroNetWK")
print(ascii_banner)

print("Version 0.01\n"+
	"Genetic neuronal network developed by Huffliger \n" +
	"Designed to solve compute intense problems\n" +
	"Currently test boilerplate to check functionality\n" + 
	"Beat the randomness function\n\n")



ROUND_COUNT = 25000

#Data for graph
roundsCompleted = 0

if(ROUND_COUNT==0):
	ROUND_COUNT = 1000000

gameFieldSize = 7
gamePerformanceMove = 0


def getMinMaxMove(choice):
	winCount = np.zeros(gameFieldSize)
	drawCount = np.zeros(gameFieldSize)
	loseCount = np.zeros(gameFieldSize)
	moveProbabiltyScore =  np.zeros(gameFieldSize)
	print(winCount)

	for p in range(depth-1, -1, -1):
		gamesToPlay = []
		#Play full game based on randomness
		for i1 in range(gameFieldSize):
			gamesToPlay.append(deepcopy(game))
			game_ended = False


			if(gamesToPlay[i1].turn(i1) == False):
				#print("Move " + str(i1) + " not possible")
				winCount[i1] = depth/7
				drawCount[i1] = -100000
				loseCount[i1] = depth/7
			else:
				#Check if it's an imediate win
				if(gamesToPlay[i1].check_winner()):
					winCount[i1] = depth * 1000
				movesPlayed = 0
				while not game_ended:
					gamesToPlay[i1].turn(np.random.randint(0, gameFieldSize))
					if not any(-1 in a for a in gamesToPlay[i1].board):
						drawCount[i1] += 1
						game_ended = True

					if(gamesToPlay[i1].check_winner()):
						if(movesPlayed % 2 == 0):
							loseCount[i1] += 1
						else:
							winCount[i1] += 1
						game_ended = True
					movesPlayed += 1
					#if(movesPlayed > 100):
					#	print(movesPlayed)

	
	winRateAIW = 0
	winRateAID = 0
	winRateAIL = 0
	for i1 in range(gameFieldSize):
		print("Field " + str(i1+1) + " w" + str(winCount[i1]) + "/d" + str(drawCount[i1]) + "/l" + str(loseCount[i1]))
		winRateAIW += winCount[i1]
		winRateAID += drawCount[i1]
		winRateAIL += loseCount[i1]
		moveProbabiltyScore[i1] = loseCount[i1] - '''(drawCount[i1]/5) -''' winCount[i1]

	#print("Unsorted list")
	#print(moveProbabiltyScore)
	s = np.array(moveProbabiltyScore)
	print("AI is winning with " + str(int(100/depth*(winRateAIW/7-winRateAIL/7)+50)) + "% confidence.")
	sort_index = np.argsort(s)
	print(sort_index)
	#print(sort_index[choice])
	return sort_index[choice]





for b in range(ROUND_COUNT-1, 0, -1):
	user = 0
	game_over = False
	game = GameField()
	loopCheck = 0
	gamePerformanceMove = 0
	depth = 1000
	while not game_over:
		depth += gamePerformanceMove*15
		print("Current depth: " + str(depth))
		loopCheck = 0
		game.print_board()
		if(user == 0):
			# Ask the user for input, but only accept valid turns
			valid_move = False
			while not valid_move:
				user_move = input(f"{game.which_turn()}'s Turn - pick a column (1-X): ")
				try:
					valid_move = game.turn(int(user_move)-1)
				except:
					print(f"Please choose a number between 1 and X")
				'''
				minMaxMove = -2
				valid_move = game.turn(getMinMaxMove(loopCheck))
				loopCheck += 1;
				time.sleep(0.5)'''
			user = 1
		else:
			#MinMax function
			valid_move = False
			while not valid_move:
				minMaxMove = -2
				valid_move = game.turn(getMinMaxMove(loopCheck))
				loopCheck += 1;
				print(f"Please choose a number between 1 and X | " + str(valid_move) + " is not valid.")
				time.sleep(0.5)
			user = 0

		gamePerformanceMove +=1

		# End the game if there is a winner
		game_over = game.check_winner()
		#print(game_over)
		#print(game.board)

		# End the game if there is a tie
		if not any(-1 in a for a in game.board):
			print("The game is a draw..")
	

	
	roundsCompleted += 1
	print("Round: " + str(roundsCompleted))