from collections import deque;
from random import randint;
class Agent:
    def __init__(self, r, c, board, rewards):
        self.pos = (r, c);
        self.lastAction = None;

        self.board = board;
        self.rewards = rewards;
        self.MAX_MEM = 1;
        self.env = {};
        self.memory = deque();
        self.alpha = 0.5;
        self.gamma = 0.9;

    def chooseAction (self, actions):
        Q = [self.getQ((self.pos, i)) for i in actions];
        # choose the highest Q value, and if there is a tie, then select randomly from them.
        maxQ = max(Q);

        best = [actions[i] for i in range(0, len(Q)) if Q[i] == maxQ];
        pick = best[randint(0, len(best) - 1)];
        
        # record our latest position in memory.
        self.memory.append((self.pos, pick));
        if (len(self.memory) > self.MAX_MEM):
            self.memory.popleft();

        return pick;
            
    def getPossibleActions (self, pos):
        nextStates = [];
        N = (pos[0] - 1, pos[1]);
        S = (pos[0] + 1, pos[1]);
        E = (pos[0], pos[1] + 1);
        W = (pos[0], pos[1] - 1);
        if N[0] < len(self.board) and self.board[N[0]][N[1]] == 0:
            nextStates.append((-1, 0));
        if S[0] >= 0 and self.board[S[0]][S[1]] == 0:
            nextStates.append((1, 0));
        if E[1] < len(self.board[E[0]]) and self.board[E[0]][E[1]] == 0:
            nextStates.append((0, 1));
        if W[1] >= 0 and self.board[W[0]][W[1]] == 0:
            nextStates.append((0, -1));

        return nextStates;

    def act (self):
        possibleActions = self.getPossibleActions(self.pos);

        thisState = self.pos;
        thisAction = self.chooseAction(possibleActions);
        nextState = (self.pos[0] + thisAction[0], self.pos[1] + thisAction[1]);
        nextActions = self.getPossibleActions(nextState);
        #print thisState, " to ", nextState;
        #if (thisState == (2, 3)):
            #print "Wow what a reward! +10";
        
        # Distribute the reward according to Q(s, a) formula.
        Qsa = self.getQ((thisState, thisAction));
        rewardTerm = self.rewards[nextState[0]][nextState[1]];
        gammaTerm = self.gamma * max([self.getQ((nextState, a)) for a in nextActions]);
        self.env[(thisState, thisAction)] = Qsa + self.alpha*(rewardTerm + gammaTerm - Qsa);
        self.pos = nextState;
        self.lastAction = thisAction;
        # (2, 3) is the optimal reward position, the best case for this artificial intel is to
        # move from (3, 3) to (2, 3) or something over and over and over to keep maximizing that
        # reward, like a rat who has been given cocaine.

        

    def getQ(self, pair):
        if pair in self.env:
            return self.env[pair];
        else:
            self.env[pair] = 0;
            return 0;
