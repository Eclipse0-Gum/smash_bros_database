import mysql.connector
from mysql.connector import Error

# 1. Connection 
def get_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            port=3306,
            database='smash_players',
            user='root',
            password='password'

        )
    except Error as e:
        print(f"Connection error: {e}")
        return None
    
#----------------------------------------------------------------------
# 2. Database

def list_characters(conn):
    """Helper function to show IDs so you actually know what to type."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT char_id, char_name, tier_rank FROM characters ORDER BY char_name ASC")
        chars = cursor.fetchall()
        print("\n--- AVAILABLE CHARACTERS ---")
        # Printing in columns so it doesn't take up too much vertical space
        for i in range(0, len(chars), 3):
            chunk = chars[i:i+3]
            line = ""
            for c in chunk:
                line += f"ID {c[0]:>2}: {c[1]:<15} ({c[2]}) | "
            print(line)
    except Error as e:
        print(f"Error fetching characters: {e}")

def add_player(conn, tag, region):
    """Adds a player and shows the character list so you know the IDs."""
    cursor = None
    try:
        cursor = conn.cursor()
        # Start the transaction 
        conn.start_transaction()

        # 1. Insert into players table
        cursor.execute("INSERT INTO players (tag, region) VALUES (%s, %s)", (tag, region))
        new_id = cursor.lastrowid 
        
        # 2. Create the necessary scouting_reports row
        cursor.execute("INSERT INTO scouting_reports (player_id, weaknesses) VALUES (%s, %s)", (new_id, "No notes yet"))
        
        # 3. SHOW THE LIST SO YOU KNOW THE ID
        list_characters(conn)
        
        print(f"\n--- ASSIGN MAIN FOR {tag.upper()} ---")
        char_id_input = input("Enter Character ID from the list above: ")
        skill_input = input("Enter Proficiency Level (1-10): ")

        if char_id_input.isdigit() and skill_input.isdigit():
            # Update Junction Table
            cursor.execute(
                "INSERT INTO player_characters (player_id, char_id, proficiency_level) VALUES (%s, %s, %s)",
                (new_id, int(char_id_input), int(skill_input))
            )
            # Update the main_char_id 
            cursor.execute("UPDATE players SET main_char_id = %s WHERE player_id = %s", (int(char_id_input), new_id))
            print(f"\n Success: {tag} linked to character ID {char_id_input}.")
        else:
            print("\n Invalid ID or Skill. Player created, but no character linked.")

        # FINAL COMMIT
        conn.commit()
        print(f" Database Updated: Player '{tag}' is now live.")

    except Error as e:
        if conn:
            conn.rollback()
        print(f"\n DATABASE ERROR: {e}")
    finally:
        if cursor:
            cursor.close()

def get_players(conn):
    try:
        cursor = conn.cursor()
        # This query joins all 3 tables to get the full list of players, their mains, and proficiency levels. It uses GROUP_CONCAT to handle multiple characters per player.
        query = """
            SELECT p.player_id, p.tag, 
                   GROUP_CONCAT(CONCAT(c.char_name, ' [', c.weight_class, ' - ', c.tier_rank, ']') SEPARATOR '; '), 
                   MAX(pc.proficiency_level)
            FROM players p
            LEFT JOIN player_characters pc ON p.player_id = pc.player_id
            LEFT JOIN characters c ON pc.char_id = c.char_id
            GROUP BY p.player_id, p.tag
            ORDER BY p.player_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()

def update_player_info(conn):
    """Updates character assignment and skill for an existing player ID."""
    cursor = None
    try:
        p_id = input("Enter the Player ID you want to update: ")
        cursor = conn.cursor()
        
        print("\n--- NEW ASSIGNMENT ---")
        new_char_id = input("Enter New Character ID: ")
        new_skill = input("Enter New Proficiency (1-10): ")
        
        if new_char_id.isdigit() and new_skill.isdigit():
            # Update the junction table by using a replace logic
            cursor.execute("""
                INSERT INTO player_characters (player_id, char_id, proficiency_level) 
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE char_id = VALUES(char_id), proficiency_level = VALUES(proficiency_level)
            """, (int(p_id), int(new_char_id), int(new_skill)))
            
            # Also update Main in the players table
            cursor.execute("UPDATE players SET main_char_id = %s WHERE player_id = %s", (int(new_char_id), int(p_id)))
            
            conn.commit()
            print(f" Player {p_id} updated successfully!")
    except Error as e:
        print(f" Error: {e}")
    finally:
        if cursor: cursor.close()

def delete_player(conn, p_id):
    """Removes a player by player ID"""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM players WHERE player_id = %s", (p_id,))
        conn.commit()
        print("Player removed.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def record_match_and_scout(conn, winner_id, loser_id, notes):
    cursor = None
    try:
        # Convert inputs to integers immediately
        w_id, l_id = int(winner_id), int(loser_id)
        
        cursor = conn.cursor()
        
        # 1. Get Tournament Context
        print("\n--- TOURNAMENT SELECTION ---")
        view_tournaments(conn) # Show them the options
        t_id = input("Enter Tournament ID: ")

        conn.start_transaction() 

        # 2. Record Match
        cursor.execute("INSERT INTO matches (tournament_id, winner_id, loser_id) VALUES (%s, %s, %s)", 
                       (int(t_id), w_id, l_id))
        
        # 3. FORCE Update Scouting Report
        # This replaces the old record or creates a new one if it's missing
        cursor.execute("""
            INSERT INTO scouting_reports (player_id, weaknesses) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE weaknesses = %s, last_updated = CURRENT_TIMESTAMP
        """, (l_id, notes, notes))

        conn.commit() 
        print(f"\n SUCCESS: Match recorded. Player {l_id}'s report updated.")
        
    except Exception as e:
        if conn: conn.rollback()
        print(f" ERROR: {e}")
    finally:
        if cursor: cursor.close()
        
def view_scouting_reports(conn):
    """Shows notes and the date they were last changed"""
    try:
        cursor = conn.cursor()
        query = """
            SELECT p.tag, s.weaknesses, s.last_updated 
            FROM scouting_reports s
            JOIN players p ON s.player_id = p.player_id
        """
        cursor.execute(query)
        reports = cursor.fetchall()
        print(f"\n{'Tag':<15} {'Weakness':<30} {'Last Updated':<20}")
        print("-" * 65)
        for r in reports:
            # r[2] is the timestamp from the database
            print(f"{r[0]:<15} {r[1]:<30} {r[2]}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        
def view_tournaments(conn):
    """Lists available tournaments and their dates."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT tournament_id, t_name, t_date FROM tournaments")
        rows = cursor.fetchall()
        print(f"\n{'ID':<5} {'Tournament Name':<30} {'Date':<15}")
        print("-" * 50)
        for r in rows:
            print(f"{r[0]:<5} {r[1]:<30} {r[2]}")
    except Error as e:
        print(f"Error: {e}")