-- 1. Players Table
CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    tag VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(50),
    main_char_id INT NULL, -- FK to characters, can be NULL if unknown
    FOREIGN KEY (main_char_id) REFERENCES characters(char_id) ON DELETE SET NULL
);

-- 2. Characters Table
CREATE TABLE characters (
    char_id INT PRIMARY KEY AUTO_INCREMENT,
    char_name VARCHAR(50) NOT NULL UNIQUE,
    weight_class ENUM('Very Light','Light', 'Middle', 'Heavy', 'Super Heavy'),
    tier_rank CHAR(1) CHECK (tier_rank IN ('SS','S', 'A', 'B', 'C', 'D', 'F'))
);

-- 3. Tournaments Table
CREATE TABLE tournaments (
    tournament_id INT PRIMARY KEY AUTO_INCREMENT,
    t_name VARCHAR(100) NOT NULL,
    t_date DATE DEFAULT (CURRENT_DATE)
);

-- 4. Player Characters (M:M Relationship)
-- There are many players who can be playing the same character, and many characters that a player can play.
CREATE TABLE player_characters (
    player_id INT,
    char_id INT,
    proficiency_level INT DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 10),
    PRIMARY KEY (player_id, char_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE
);

-- 5. Matching Tables
CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    tournament_id INT,
    winner_id INT,
    loser_id INT,
    winner_char_id INT,
    loser_char_id INT,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id),
    FOREIGN KEY (winner_id) REFERENCES players(player_id),
    FOREIGN KEY (loser_id) REFERENCES players(player_id),
    FOREIGN KEY (winner_char_id) REFERENCES characters(char_id),
    FOREIGN KEY (loser_char_id) REFERENCES characters(char_id)
);

-- 6. Scouting_Reports (1:1 Relationship)
CREATE TABLE scouting_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT UNIQUE, -- UNIQUE ensures a 1:1 relationship with players
    habits TEXT,
    weaknesses TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

ALTER TABLE players 
ADD CONSTRAINT fk_main_char 
FOREIGN KEY (main_char_id) REFERENCES characters(char_id);