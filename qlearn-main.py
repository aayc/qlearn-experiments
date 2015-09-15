from random import randint;
from collections import deque;
board = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 2, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]];

rewards = [[0 for j in range(0, len(board[i]))] for i in range(0, len(board))];
for i in range(0, len(board)):
    for j in range(0, len(board[i])):
        if board[i][j] == 2:
            rewards[i][j] = 10;
            break;

print "BOARD: ";
for b in board:
    print b;

print "------------";
print "REWARDS: ";
for b in rewards:
    print b;

# We want some sort of set of all possible states, r,c for agent.
# for all states, we want directional actions

class Agent:
    def __init__(self, r, c):
        self.pos = (r, c);
        self.MAX_MEM = 1;
        self.env = {};
        self.memory = deque();
        self.env[self.pos] = 0;
        print self.pos;
        

    def act (self):
        # where can I go?
        nextStates = [];
        print "Position: ", self.pos;
        
        N = (self.pos[0] - 1, self.pos[1]);
        S = (self.pos[0] + 1, self.pos[1]);
        E = (self.pos[0], self.pos[1] + 1);
        W = (self.pos[0], self.pos[1] - 1);
        if N[0] < len(board) and board[N[0]][N[1]] == 0:
            nextStates.append(N);
        if S[0] >= 0 and board[S[0]][S[1]] == 0:
            nextStates.append(S);
        if E[1] < len(board[self.pos[0]]) and board[E[0]][E[1]] == 0:
            nextStates.append(E);
        if W[1] >= 0 and board[W[0]][W[1]] == 0:
            nextStates.append(W);

        print nextStates;

        Q = [self.getQ(i) for i in nextStates];
        # choose the highest Q value, and if there is a tie, then select randomly from them.
        maxQ = max(Q);

        possibleActions = [nextStates[i] for i in range(0, len(Q)) if Q[i] == maxQ];
        choice = possibleActions[randint(0, len(possibleActions) - 1)];
        # record our latest position in memory.
        self.memory.append(self.pos);
        if (len(self.memory) > self.MAX_MEM):
            self.memory.popleft();
            
        self.pos = choice;

        # Distribute the reward according to Q(s, a) formula.
        
        

    def getQ(self, state):
        if state in self.env:
            return self.env[state];
        else:
            self.env[state] = 0;
            return 0;

agentStart = [3, 4];
dude = Agent(agentStart[0], agentStart[1]);
for i in range(0, 10):
    dude.act();
