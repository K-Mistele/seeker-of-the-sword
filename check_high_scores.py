import csv
import time
from local_resources.colorama_master import colorama
from time import sleep

def check_high_scores(user, high_score, board_size):
    board_size = "{}x{}".format(str(board_size), str(board_size))
    day = time.strftime("%m/%d/%Y")
    with open('high_scores.csv', 'r', newline='') as csvfile:
        scores_reader = csv.reader(csvfile, dialect="excel")
        current_scores = []
        for row in scores_reader:
            current_scores.append(row)
        for row in list(current_scores):
            if len(row) < 3:
                current_scores.remove(row)
        if len(current_scores) < 3:
            for i in range(0, 3):
                current_scores.append(['Kyle', 40+i, day])
        if len(current_scores) >= 7:
            current_scores = sorted(current_scores, key=lambda x: x[1], reverse=True)

            #print(current_scores)
            if high_score > int(current_scores[-1][1]): # if player high score is higher than any of current scores
                current_scores.remove(current_scores[-1]) # remove last item in list
                current_scores.append([user, high_score, day, board_size]) # append player high score
                for row in current_scores:
                    row[1] = int(row[1])
                current_scores = sorted(current_scores, key= lambda x: x[1], reverse=True)
        else:
            current_scores.append([user, high_score, day, board_size])
        for row in current_scores:
            row[1] = int(row[1])


        #print(current_scores)
        current_scores = sorted(current_scores, key=lambda x: x[1], reverse=True)
    with open("high_scores.csv", 'w', newline="") as csvfile:
        scores_writer = csv.writer(csvfile, dialect="excel")
        for row in current_scores:
            scores_writer.writerow(row)
    return current_scores

def print_high_scores(scores, with_colors):

    for score in scores:
        # make sure all names have same amount of white space
        if len(score[0]) > 20:
            score[0] = score[0][0:15]
            # trim overly long usernames
        score[0] = "|" + score[0]
        for i in range(len(score[0]), 20):
            score[0] += " "
        score[0] += "|"

        #make sure all scores have same amount of white space
        score[1] = str(score[1])
        for i in range(len(str(score[1])), 18):
            score[1] += " "
        score[1] += "|"

        #make sure all dates have same amount of white space
        for i in range(len(score[2]), 18):
            score[2] += " "
        score[2] += "|"

        #make sure all board dimensions have same amount of white space
        for i in range(len(score[3]), 10):
            score[3] += " "
        score[3] += "|"
    if with_colors: print(colorama.Fore.BLUE)
    start_row = "*-------------------------------------------------------------------*"
    mid_row =   "|--------------------------------------------------------------------|"
    end_row =   "*-------------------------------------------------------------------*"
    print(start_row)
    counter = 0
    for row in scores:

        print("{}{}{}{}".format(row[0], row[1], row[3], row[2]))
        counter += 1
        if counter != len(scores): print(mid_row)
    print(end_row)
    if with_colors: print(colorama.Fore.WHITE)
    sleep(5)
