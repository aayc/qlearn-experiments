from random import random;
from random import randint;
from copy import deepcopy;
class AI_Player:
    def __init__(self, rewardFcn, playNum):
        self.alpha = 0.5;
        self.gamma = 0.9;
        self.epsilon = 0.1;
        self.playNum = playNum;
        self.q = {};
        self.rewardFcn = rewardFcn;

    def getActions(self, board):
        actions = [];
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == 0:
                    actions.append((i, j));
        return actions;
    
    def chooseAction(self, state, actions):
        Q = [self.q.get((state, a), 0.0) for a in actions];
        maxQ = max(Q);

        if random() < self.epsilon:
            mag = max(abs(min(Q)), abs(maxQ));
            Q = [self.q.get((state, a), 0.0) + random() * mag - 0.5*mag
                     for i in actions];
            
        best = [actions[i] for i in range(0, len(Q)) if Q[i] == maxQ];
        pick = best[randint(0, len(best) - 1)];

        return pick;

    def act (self, board):
        actions = self.getActions(board);
        state = tuple([tuple(i) for i in board]);
        thisState = state;
        thisAction = self.chooseAction(state, actions);
        boardCopy = deepcopy(board);
        boardCopy[thisAction[0]][thisAction[1]] = self.playNum;
        nextState = tuple([tuple(i) for i in boardCopy]);
        nextActions = self.getActions(boardCopy);

        Qsa = self.q.get((thisState, thisAction), 0);
        rewardTerm = self.rewardFcn(boardCopy, self.playNum);
        print "I got reward ", rewardTerm;
        gammaTerm = self.gamma * max([self.q.get((nextState, a), 0) for a in nextActions]);
        self.q[(thisState, thisAction)] = Qsa + self.alpha*(rewardTerm + gammaTerm - Qsa);
        return boardCopy;
                                     
