CREATE TABLE characters (
    char_id INT PRIMARY KEY AUTO_INCREMENT,
    char_name VARCHAR(50) NOT NULL UNIQUE,
    weight_class ENUM('Very Light','Light', 'Middle', 'Heavy', 'Super Heavy'),
    tier_rank CHAR(2) CHECK (tier_rank IN ('SS','S', 'A', 'B', 'C', 'D', 'F'))
);

CREATE TABLE tournaments (
    tournament_id INT PRIMARY KEY AUTO_INCREMENT,
    t_name VARCHAR(100) NOT NULL,
    t_date DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    tag VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(50),
    main_char_id INT NULL,
    FOREIGN KEY (main_char_id) REFERENCES characters(char_id) ON DELETE SET NULL
);

CREATE TABLE player_characters (
    player_id INT,
    char_id INT,
    proficiency_level INT DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 10),
    PRIMARY KEY (player_id, char_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    tournament_id INT,
    winner_id INT,
    loser_id INT,
    FOREIGN KEY (tournament_id) REFERENCES tournaments(tournament_id) ON DELETE SET NULL,
    FOREIGN KEY (winner_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (loser_id) REFERENCES players(player_id) ON DELETE CASCADE
);

CREATE TABLE scouting_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT UNIQUE,
    weaknesses TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);
