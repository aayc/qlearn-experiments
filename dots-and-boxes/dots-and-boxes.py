from dotnode import Node;
from dots_ai import AI_Player;
from collections import deque;

BOARD_LENGTH = 3;
GRAPHICS = True;
PREPROCESS_ITERATIONS = 300000;
STEP_PLAY = True;
USER_PLAY = False;
USER_INPUT = True;

board = [[Node(str(i) + "," + str(j)) for j in range(0, BOARD_LENGTH)] for i in range(0, BOARD_LENGTH)]
complete = [[0 for i in range(0, BOARD_LENGTH - 1)] for j in range(0, BOARD_LENGTH - 1)]

def playTurn (ais, cnt, board):
	board = ais[cnt].act(board);

	# Try all squares in the board.
	for i in range(0, len(board) - 1):
		for j in range(0, len(board) - 1):
			# Each i is the top left corner of a square.
			if complete[i][j] == 0:
				topCornerConnected = board[i][j].hasNeighbor(board[i + 1][j]) and board[i][j].hasNeighbor(board[i][j + 1]);
				bottomCornerConnected = board[i + 1][j].hasNeighbor(board[i + 1][j + 1]) and board[i][j + 1].hasNeighbor(board[i + 1][j + 1]);
				if topCornerConnected and bottomCornerConnected:
					complete[i][j] = ais[cnt].playNum + 1;
					ais[cnt].learn(100);
					ais[(cnt + 1) % len(ais)].learn(-100);

def boardIsDone(complete):
	# Make sure there are still turns left. - all complete = no turns left.
	ans = len(filter(lambda x: 0 in x, complete)) == 0
	return ans;


ais = [AI_Player(0), AI_Player(1)];
numWins = [0, 0];
cnt = 0;
reset = False;
print "RUNNING ", PREPROCESS_ITERATIONS, " TURNS"
for i in range(0, PREPROCESS_ITERATIONS):
	playTurn(ais, cnt, board);
	if boardIsDone(board):
		board = [[Node(str(i) + "," + str(j)) for j in range(0, BOARD_LENGTH)] for i in range(0, BOARD_LENGTH)]
		complete = [[0 for i in range(0, BOARD_LENGTH - 1)] for j in range(0, BOARD_LENGTH - 1)]
		cnt = 0;
		continue;
	cnt = (cnt + 1) % len(ais);
print "EXECUTING GRAPHICS"

if GRAPHICS:
	import sys, pygame;
	pygame.init();
	screen = pygame.display.set_mode((800, 600));
	done = False;

	mouseOverColor = (0, 200, 0);
	playerColors = ((200, 0, 0), (0, 0, 200))
	while not done:
		screen.fill((255, 255, 255));

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True;
			elif USER_INPUT and not USER_PLAY and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
				if reset:
					board = [[Node(str(i) + "," + str(j)) for j in range(0, BOARD_LENGTH)] for i in range(0, BOARD_LENGTH)]
					complete = [[0 for i in range(0, BOARD_LENGTH - 1)] for j in range(0, BOARD_LENGTH - 1)]
					cnt = 0;
					reset = False;

				playTurn(ais, cnt, board)
				
				if boardIsDone(complete):
					reset = True;
					continue;

				cnt = (cnt + 1) % len(ais);

		for i in range(0, len(board)):
			for j in range(0, len(board[i])):
				rect = pygame.Rect(i*50, j*50, 20, 20);
				pygame.draw.rect(screen, (100, 100, 100), rect);
				for neighbor in board[i][j].neighbors:
					neighborLoc = (int(neighbor[0].name.split(",")[0]), int(neighbor[0].name.split(",")[1]));
					width = 50*(neighborLoc[0] - i);
					height = 50*(neighborLoc[1] - j);
					nRect = pygame.Rect(i*50 + 10, j*50 + 10, width if width != 0 else 10, height if height != 0 else 10);
					pygame.draw.rect(screen, playerColors[neighbor[1]], nRect);

		for i in range(0, len(complete)):
			for j in range(0, len(complete)):
				if complete[i][j] != 0:
					pygame.draw.rect(screen, playerColors[complete[i][j] - 1], pygame.Rect(i*50 + 25, j*50 + 25, 30, 30));

		pygame.display.flip();

	pygame.quit();
	sys.exit()
