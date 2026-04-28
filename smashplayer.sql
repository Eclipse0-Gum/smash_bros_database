-- Create Characters first (since Players and Matches need it)
CREATE TABLE characters (
    char_id INT PRIMARY KEY AUTO_INCREMENT,
    char_name VARCHAR(50) NOT NULL UNIQUE,
    weight_class ENUM('Very Light','Light', 'Middle', 'Heavy', 'Super Heavy'),
    tier_rank CHAR(2) CHECK (tier_rank IN ('SS','S', 'A', 'B', 'C', 'D', 'F'))
);

-- Create Tournaments (it stands alone)
CREATE TABLE tournaments (
    tournament_id INT PRIMARY KEY AUTO_INCREMENT,
    t_name VARCHAR(100) NOT NULL,
    t_date DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    tag VARCHAR(50) NOT NULL UNIQUE,
    region VARCHAR(50),
    main_char_id INT NULL
);

-- M:M Junction Table
CREATE TABLE player_characters (
    player_id INT,
    char_id INT,
    proficiency_level INT DEFAULT 1 CHECK (proficiency_level BETWEEN 1 AND 10),
    PRIMARY KEY (player_id, char_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (char_id) REFERENCES characters(char_id) ON DELETE CASCADE
);

-- Matches Table
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

-- Scouting Reports
CREATE TABLE scouting_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT UNIQUE,
    habits TEXT,
    weaknesses TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
);

ALTER TABLE players 
ADD CONSTRAINT fk_main_char 
FOREIGN KEY (main_char_id) REFERENCES characters(char_id) ON DELETE SET NULL;

---------------------------------------------------

Example Data:
INSERT INTO characters (char_name, weight_class, tier_rank) VALUES 
('Steve', 'Middle', 'S'),
('Sonic', 'Middle', 'S'),
('Aegis', 'Middle', 'S'),
('Joker', 'Middle', 'S'),
('Snake', 'Heavy', 'A'),
('Cloud', 'Middle', 'A'),
('Game & Watch', 'Light', 'A'),
('R.O.B.', 'Super Heavy', 'A'),
('Fox', 'Light', 'A'),
('Peach', 'Middle', 'A'),
('Kazuya', 'Super Heavy', 'A'),
('Mario', 'Middle', 'B'),
('Donkey Kong', 'Super Heavy', 'C'),
('Ganondorf', 'Super Heavy', 'F'),
('Wolf', 'Middle', 'A'); 

INSERT INTO players (tag, region) VALUES 
('MkLeo', 'Mexico'),
('Sparg0', 'Mexico'),
('Sonix', 'Dominican Republic'),
('Tweek', 'USA'),
('Miya', 'Japan'),
('Acola', 'Japan'),
('Light', 'USA'),
('Zomba', 'USA'),
('Riddles', 'Canada'),
('Glutonny', 'France'),
('Shuton', 'Japan'),
('Tea', 'Japan'),
('Maister', 'Mexico'),
('Big D', 'Canada'),
('Skyjay', 'Mexico');

INSERT INTO tournaments (t_name, t_date) VALUES 
('Genesis X', '2024-02-15'),
('Super Smash Con', '2024-08-10'),
('Luminosity Makes Moves', '2024-10-25'),
('The Big House', '2024-11-05');

INSERT INTO scouting_reports (player_id, habits, weaknesses) 
SELECT player_id, 'No notes yet', 'No weaknesses recorded' FROM players;