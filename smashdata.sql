--------- Example Data:

INSERT INTO characters (char_name, weight_class, tier_rank) VALUES 
('Mario', 'Middle', 'A'), ('Donkey Kong', 'Super Heavy', 'C'), ('Link', 'Heavy', 'B'),
('Samus', 'Heavy', 'A'), ('Dark Samus', 'Heavy', 'A'), ('Yoshi', 'Middle', 'A'),
('Kirby', 'Light', 'D'), ('Fox', 'Light', 'A'), ('Pikachu', 'Light', 'S'),
('Luigi', 'Middle', 'A'), ('Ness', 'Middle', 'A'), ('Captain Falcon', 'Heavy', 'A'),
('Peach', 'Middle', 'S'), ('Daisy', 'Middle', 'S'), ('Bowser', 'Super Heavy', 'B'),
('Ice Climbers', 'Middle', 'C'), ('Sheik', 'Light', 'A'), ('Zelda', 'Light', 'D'),
('Dr. Mario', 'Middle', 'F'), ('Pichu', 'Very Light', 'B'), ('Falco', 'Middle', 'A'),
('Marth', 'Middle', 'B'), ('Lucina', 'Middle', 'A'), ('Young Link', 'Middle', 'A'),
('Ganondorf', 'Super Heavy', 'F'), ('Mewtwo', 'Light', 'B'), ('Roy', 'Middle', 'S'),
('Chrom', 'Middle', 'B'), ('Mr. Game & Watch', 'Light', 'S'), ('Meta Knight', 'Middle', 'B'),
('Pit', 'Middle', 'B'), ('Dark Pit', 'Middle', 'B'), ('Zero Suit Samus', 'Middle', 'A'),
('Wario', 'Heavy', 'S'), ('Snake', 'Heavy', 'S'), ('Ike', 'Heavy', 'C'),
('Pokemon Trainer', 'Middle', 'A'), ('Diddy Kong', 'Middle', 'S'), ('Lucas', 'Middle', 'B'),
('Sonic', 'Middle', 'S'), ('King Dedede', 'Super Heavy', 'D'), ('Olimar', 'Light', 'A'),
('Lucario', 'Middle', 'C'), ('R.O.B.', 'Super Heavy', 'S'), ('Toon Link', 'Middle', 'B'),
('Wolf', 'Middle', 'A'), ('Villager', 'Middle', 'C'), ('Mega Man', 'Heavy', 'B'),
('Wii Fit Trainer', 'Middle', 'B'), ('Rosalina & Luma', 'Middle', 'A'), ('Little Mac', 'Middle', 'F'),
('Greninja', 'Middle', 'A'), ('Mii Brawler', 'Middle', 'A'), ('Mii Swordfighter', 'Middle', 'C'),
('Mii Gunner', 'Middle', 'C'), ('Palutena', 'Middle', 'A'), ('Pac-Man', 'Middle', 'S'),
('Robin', 'Middle', 'B'), ('Shulk', 'Middle', 'A'), ('Bowser Jr.', 'Heavy', 'C'),
('Duck Hunt', 'Middle', 'D'), ('Ryu', 'Heavy', 'A'), ('Ken', 'Heavy', 'A'),
('Cloud', 'Middle', 'S'), ('Corrin', 'Middle', 'A'), ('Bayonetta', 'Middle', 'A'),
('Inkling', 'Middle', 'B'), ('Ridley', 'Heavy', 'C'), ('Simon', 'Heavy', 'D'),
('Richter', 'Heavy', 'D'), ('King K. Rool', 'Super Heavy', 'D'), ('Isabelle', 'Light', 'D'),
('Incineroar', 'Heavy', 'B'), ('Piranha Plant', 'Heavy', 'D'), ('Joker', 'Middle', 'S'),
('Hero', 'Middle', 'B'), ('Banjo & Kazooie', 'Heavy', 'D'), ('Terry', 'Heavy', 'A'),
('Byleth', 'Middle', 'B'), ('Min Min', 'Middle', 'A'), ('Steve', 'Middle', 'SS'),
('Sephiroth', 'Light', 'B'), ('Pyra/Mythra', 'Middle', 'S'), ('Kazuya', 'Super Heavy', 'S'),
('Sora', 'Light', 'A');

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

---------------------------- To update scouting reports for all players with default values, we can use the following SQL statement:
INSERT INTO scouting_reports (player_id, habits, weaknesses) 
SELECT player_id, 'No notes yet', 'No weaknesses recorded' FROM players;