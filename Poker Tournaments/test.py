import matplotlib.pyplot as plt
import re
import os
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import messagebox

FOLDER_PATH = "C:\\Users\\km154756\\TournamentTracker\\data\\Kevin12345Mc"

tournament_data = {}
total_hands_played = 0
total_tournament_cost = 0

hand_pattern = re.compile(
    r"PokerStars Hand #(\d+): Tournament #(\d+), (\$\d+\.\d+\+\$\d+\.\d+) USD .*? - (\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2} \w+)"
)

chip_pattern = re.compile(
    r"Kevin12345Mc \((\d+) in chips\)"
)

existing_tournaments = set(tournament_data.keys())

for file_name in os.listdir(FOLDER_PATH):
    if file_name.endswith(".txt"):
        file_path = os.path.join(FOLDER_PATH, file_name)
        
        with open(file_path, "r", encoding="utf-8") as file:
            current_hand = None
            current_tournament = None
            current_chips = None
            current_hand_time = None
            current_cards = None

            for line in file:
                match_hand = hand_pattern.search(line)
                match_chips = chip_pattern.search(line)

                if match_hand:
                    ##tournament_number = match_hand.group(2)

                    
                    ##if tournament_number in existing_tournaments:
                    ##    break

                    current_hand = match_hand.group(1)
                    current_tournament = match_hand.group(2)
                    current_tournament_cost = match_hand.group(3)
                    current_hand_time = match_hand.group(4)
                    current_chips = None


                elif match_chips:
                    current_chips = match_chips.group(1)

                
                if current_hand and current_chips:
                    if current_tournament not in tournament_data:
                        tournament_data[current_tournament] = {"hand_number": [], "start_chips": [], "cost": current_tournament_cost, "hand_time": [], "end_chips": []}

                    tournament_data[current_tournament]["hand_number"].append(int(current_hand))
                    tournament_data[current_tournament]["start_chips"].append(int(current_chips))
                    tournament_data[current_tournament]["hand_time"].append(current_hand_time)
                    

                    current_hand = None
                    current_chips = None
                    current_hand_time = None

                    existing_tournaments.add(current_tournament)

print("All new tournaments have been read!")

for tournament, data in tournament_data.items():
    total_hands_played += len(data["hand_number"])
    cost = data["cost"]
    
    cost_parts = cost.split('+')
    cost_value = float(cost_parts[0][1:]) + float(cost_parts[1][1:])
    total_tournament_cost += cost_value
    
print(total_hands_played)
average_tournament_cost = total_tournament_cost / len(tournament_data)

all_hands_played = 0

# Prepare data for insertion into MySQL
data_to_insert = []
for tournament, data in tournament_data.items():
    for hand_number, start_chips, hand_time in zip(data["hand_number"], data["start_chips"], data["hand_time"]):
        data_to_insert.append((tournament, hand_number, start_chips, hand_time))

# Convert data to DataFrame
df = pd.DataFrame(data_to_insert, columns=['tournament_id', 'hand_number', 'starting_chip_count', 'date'])

# Set up MySQL database connection
db_url = 'mysql+pymysql://root:21isComing!@localhost/poker' # Update with your credentials
engine = create_engine(db_url)

# Insert data into MySQL table
df.to_sql('tournament_hands', engine, if_exists='append', index=False)

print("Data successfully inserted into the database.")