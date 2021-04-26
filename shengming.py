from collections import deque
from tinydb import TinyDB, Query
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import sys
import datetime

# Manually create a list of tags
tags = ["sleep", "exercise", "social", "research", "leisure", "school", "maintenance", "happiness"]

def graph():
    # TODO Create plots for each tag.
    db = TinyDB('db.json')
    days_table = db.table('days')
    gp = {'time':[], 'date':[], 'avg':[]}
    queue = deque([])
    total = 0
    days = []

    # Create plots for every tag.
    for tag in tags:
        total = 0
        gp['time'].clear()
        gp['date'].clear()
        gp['avg'].clear()
        queue.clear()
        # Iterate through each day's log.
        for day in days_table:
            tag_time = 0
            
            # Ignore tag if it is not in daily log.
            if not(tag in day['tags']):
                continue

            # If data is in minutes, convert to hours.
            if day['tags'][tag] > 30:
                tag_time = day['tags'][tag] / 60
            else:
                tag_time = day['tags'][tag]

            gp['time'].append(tag_time)
            gp['date'].append(day['date'])

            # Create graph out of average trend.
            total += tag_time
            queue.append(tag_time)
            gp['avg'].append(total / len(queue))

        df = pd.DataFrame(gp)

        fig, ax = plt.subplots()

        if tag == 'happiness':
            ax.set_title("Happiness score (1-10)")
            ax.set_ylabel('score')
            ax.set_xlabel('days')
        else:
            ax.set_title("Time spent on @{}".format(tag))
            ax.set_ylabel('hours')
            ax.set_xlabel('days')

        ax.plot('date', 'time', data=df, color="gainsboro")
        ax.plot('date', 'avg', data=df, color="black")

        fig.autofmt_xdate()

        plt.savefig("plots/" + tag + ".png")

def parse():
    # TODO: Add way for scores / 30 minutes
    # TODO: Happiness every day
    log = None
    tags = []

    lastScore = 0
    lastag_timeime = 0

    # TODO: Different tables for days/tags/etc.
    db = TinyDB('db.json')
    db2 = TinyDB('db2.json')
    days = db.table('days')
    days2 = db.table('days')

    try:
        log = open("life.sm", "r")
    except IOError:
        print("No daily file found")
        sys.exit()

    lines = log.readlines()
    dd = {}
    for line in lines:
        if line[0] == '#':
            continue

        words = line.split()

        # TODO: Handle subtag
        # Reset when you're on dates
        if len(words) == 0:
            continue
        elif "-" in words[0] and words[0][0].isdigit():
            dd['date'] = words[0].strip()
            dd['score'] = 0
            dd['tags'] = {}
            lastag_timeime = 0
            tags.clear()
            continue

        if not words[0][0].isdigit():
            continue

        time_passed = time_to_minutes(words[0])
        # Process last one
        if lastag_timeime != 0:
            dd['score'] += (time_passed - lastag_timeime) / 15 * lastScore
            for tag in tags:
                temp_tags = []
                tag_split = tag.split("(")
                for section in tag_split:
                    if ')' in section:
                        temp_tags.append(tag_split[0] + "(" + section)
                    else:
                        temp_tags.append(section)

                for tag_timeag in temp_tags:
                    dd['tags'].setdefault(tag_timeag, 0)
                    dd['tags'][tag_timeag] += time_passed - lastag_timeime

        # Push Current (Not if FIN)
        tags.clear()
        if words[1] == "FIN":
            days.insert(dd)
            dd.clear()
            continue

        lastag_timeime = time_passed
        lastScore = 0
        for word in words:
            if word[0] == '@':
                tags.append(word[1:])
            elif word[0] == '-':
                lastScore = int(word)
            elif word[0] == '+':
                lastScore = int(word[1:])

def paper_parse():
    day = {}

    # Store date month/day/year in the date key.
    date = datetime.datetime.now()
    day["date"] = date.strftime("%x")

    tag_hours = {}

    # Prompt user for hours spent on each tag and store it (in minutes) in a dictionary which will be stored in the tag
    # key.
    for tag in tags:
        if tag == "happiness":
            tag_hours[tag] = float(input(tag + ": "))
        else:
            tag_hours[tag] = float(input(tag + ": ")) * 60
    day["tags"] = tag_hours


    db = TinyDB('db.json')
    days = db.table('days')
    db2 = TinyDB('db2.json')
    days2 = db2.table('days')
    days.insert(day)
    days2.insert(day)
    print("Hours stored.")

def time_to_minutes(time):
    # TODO: Convert time to minutes
    split_time = time.split(":")
    return int(split_time[0]) * 60 + int(split_time[1])


# TODO: Proper way to name things and documentation
# TODO: Check for just the last week
# TODO: Score for every day
# TODO: Write states to JSON or something then also be able to output stats from that
# TODO: Have # be comment in the file
def main():
    # Arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("-u", "--update", help="Update database")
    group.add_argument("-g", "--graph", action='store_true', help="Create graph of hours")

    args = parser.parse_args()

    if args.graph != None:
        graph()
        sys.exit()

    paper_parse()



if __name__ == '__main__':
    main()
