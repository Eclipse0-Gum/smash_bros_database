CREATE DATABASE smash_players;
USE smash_players;

-- 1. Characters Table
CREATE TABLE characters (
    char_id INT PRIMARY KEY AUTO_INCREMENT,
    char_name VARCHAR(50) NOT NULL UNIQUE,
    weight_class VARCHAR(20),
    tier_rank CHAR(2)
);

-- 2. Players Table
CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    tag VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(50)
);

-- 3. Player Character Links
CREATE TABLE player_characters (
    player_id INT,
    char_id INT,
    proficiency_level INT DEFAULT 1,
    PRIMARY KEY (player_id, char_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE
);

-- 4. Matches Table
CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    winner_id INT,
    loser_id INT,
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (winner_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (loser_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- 5. Scouting Reports Table
CREATE TABLE scouting_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT UNIQUE,
    weaknesses TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);