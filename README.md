# TournamentTracker
Poker tournament and hand analyzer project

### Initial Metrics

    - Hands Played
    - Tournaments Played
    - Total Buy-Ins
    - Total Winnings
    - Net Profit/Loss
    - ROI %
    - Average Tournament Cost

### Secondary Metrics

    - (All In) EV BB/100
    - Hand BBs (Most Won / Most Lost)

### Process

    1. Read hand/tournament in Python
    2a. Write hand/tournament to SQL tables
       - 2b. Archive txt file so duplicate data is not inserted, keep check on previous tournaments to stop duplicate data from being inserted. 
    3. Retrieve data from SQL tables
    4. Display data in metrics and visualizations

### Tasks

    - Create Python script to read data from txt files
    - Create SQL database and tables (possibly do this with Python script)
    - Create Python script to write data to SQL tables
    - Create Python script to retrieve data from SQL
    - Create Python script to calculate metrics
    - Create Python script to visualize data
    - Create Python UI to integrate most or all of these features