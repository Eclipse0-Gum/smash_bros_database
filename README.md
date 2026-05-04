# Super Smash Scouting System

## Project Description
The Super Smash Scouting System is a CLI-based tool and MySQL database for tracking pro Smash Bros. players, their mains, match results, and scouting reports.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Create DB: `mysql -u root -p < smashbase.sql`
3. Import Data: `mysql -u root -p smash_players < smashdata.sql`
4. Run: `python3 smash_main.py`

## Features
- Player and Character Management (Add/Delete/Update)
- Match and Note Recordings
- Automated Scouting Reports and W/L Insights (Helps understand a pattern recognition)

## Table Descriptions
- **players**: ID, Tag, Region
- **characters**: Reference list of all fighters (including DLC)
- **player_characters**: Links players to characters with proficiency levels (For threat level purposes)
- **matches**: Winner/Loser tracking
- **scouting_reports**: Opponent weakness logs
