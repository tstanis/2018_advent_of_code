from collections import defaultdict
from blist import blist

def gen_marbles(num_players, max_marble):
    board = blist([0, 1])
    scores = defaultdict(int)
    current_marble_index = 1
    next_marble = 2
    cur_player = 1
    next_marble = 2
    while next_marble <= max_marble:
        cur_player += 1
        if cur_player > num_players:
            cur_player = 1
        
        if next_marble % 23 == 0:
            scores[cur_player] += next_marble
            other_score_idx = current_marble_index - 7
            while other_score_idx < 0:
                other_score_idx = len(board) + other_score_idx
            scores[cur_player] += board.pop(other_score_idx)
            current_marble_index = other_score_idx
        else:
            next_spot = (current_marble_index + 2) % len(board)
            if next_spot == 0:
                board.append(next_marble)
                current_marble_index = len(board) - 1
            else:
                board.insert(next_spot, next_marble)
                current_marble_index = next_spot
        next_marble += 1
        if next_marble % (max_marble / 100) == 0:
            print float(next_marble) / max_marble
            print len(board)

        # def str_marble(marble):
        #     if marble == current_marble:
        #         return "(" + str(marble) + ")"
        #     else:
        #         return marble
        #print "[" + str(cur_player) + "] " + str(map(str_marble, board))
    return scores

scores = gen_marbles(411, 71170 * 100)
#print scores
print "High Score"
print scores[max(scores, key=scores.get)]
