from aiplayer import AI_Player;


board = [[0 for i in range(0, 3)] for j in range(0, 3)];
REWARD_TERM = 50;

def getReward (board, playNum):
    for i in range(0, len(board)):
        if max(board[i]) == min(board[i]) and max(board[i]) != 0:
            return REWARD_TERM if board[i][0] == playNum else -REWARD_TERM;
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0:
            return REWARD_TERM if board[0][i] == playNum else -REWARD_TERM;
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
        return REWARD_TERM if board[0][0] == playNum else -REWARD_TERM;
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
        return REWARD_TERM if board[0][0] == playNum else -REWARD_TERM;
    return 0;

def aiMakeMove (ai):
    board = ai.act(board);
    return (board, getReward(board, ai.playNum) != 0);
        

ais = [AI_Player(getReward, 1), AI_Player(getReward, 2)];
cnt = 0;
for i in range(0, 9):
    print "------------"
    
    board = ai1.act(board);
    for b in board:
        print b;
    if (getReward(board, ai1.playNum)):
        print "AI 1 wins!  Resetting board:";
        board = [[0 for i in range(0, 3)] for j in range(0, 3)];
    print "------------"
