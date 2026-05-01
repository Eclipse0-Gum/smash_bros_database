import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        return mysql.connector.connect(
            host='localhost', user='root', password='password', database='smash_players'
        )
    except Error as e:
        print(f"Connection error: {e}")
        return None

def add_player(conn, tag, region):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO players (tag, region) VALUES (%s, %s)", (tag, region))
        conn.commit()
        print(f" Player '{tag}' created!")
    except Error as e:
        print(f" Error: {e}")
    finally:
        cursor.close()

def update_mains(conn, p_id, c_id, level):
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO player_characters (player_id, char_id, proficiency_level) 
                 VALUES (%s, %s, %s) 
                 ON DUPLICATE KEY UPDATE proficiency_level = VALUES(proficiency_level)"""
        cursor.execute(sql, (p_id, c_id, level))
        conn.commit()
        print(f" Main character updated for Player ID {p_id}!")
    except Error as e:
        print(f" Error: {e}")
    finally:
        cursor.close()
        
def delete_main(conn, p_id, c_id):
    cursor = None
    try:
        if conn.in_transaction:
            conn.rollback()
        
        cursor = conn.cursor()
        conn.start_transaction()
        
        # Deletes the link between player and specific character
        query = "DELETE FROM player_characters WHERE player_id = %s AND char_id = %s"
        cursor.execute(query, (int(p_id), int(c_id)))
        
        conn.commit()
        print(f" Character ID {c_id} removed from Player {p_id}'s mains.")
    except Exception as e:
        if conn: conn.rollback()
        print(f" Error deleting main: {e}")
    finally:
        if cursor: cursor.close()


def record_match_and_scout(conn, winner_id, loser_id, notes):
    cursor = None
    try:
        # FORCE RESET
        if conn.in_transaction:
            conn.rollback()
            
        w_id, l_id = int(winner_id), int(loser_id)
        cursor = conn.cursor()
        conn.start_transaction()
        
        # Force a rollback BEFORE starting the transaction to clear any ghost transactions that might be lingering from previous operations.
        try:
            conn.rollback()
        except:
            pass

        conn.start_transaction() 

        # Record the match
        cursor.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (w_id, l_id))

        # Update the scouting report 
        sql = """
            INSERT INTO scouting_reports (player_id, weaknesses) 
            VALUES (%s, %s) 
            ON DUPLICATE KEY UPDATE 
                weaknesses = VALUES(weaknesses), 
                last_updated = CURRENT_TIMESTAMP
        """
        cursor.execute(sql, (l_id, notes))

        conn.commit()
    except Exception as e:
        if conn: conn.rollback() # Emergency exit in case something goes wrong
        print(f" Error: {e}")
    finally:
        if cursor: cursor.close()
        

def view_players(conn):
    """Shows all players along with their main characters and proficiency levels."""
    cursor = conn.cursor()
    try:
        query = """
            SELECT p.player_id, p.tag, 
                   GROUP_CONCAT(CONCAT(c.char_name, ' (Lvl ', pc.proficiency_level, ')') SEPARATOR ', ') AS mains
            FROM players p
            LEFT JOIN player_characters pc ON p.player_id = pc.player_id
            LEFT JOIN characters c ON pc.char_id = c.char_id
            GROUP BY p.player_id, p.tag
            ORDER BY p.player_id ASC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print(f"\n{'ID':<5} {'Tag':<15} {'Main Characters'}")
        print("-" * 60)
        for r in rows:
            mains = r[2] if r[2] else "No mains assigned"
            print(f"{r[0]:<5} {r[1]:<15} {mains}")
    except Exception as e:
        print(f" Error viewing players: {e}")
    finally:
        cursor.close()

def list_characters(conn):
    """Lists all characters and their IDs in order for easy reference."""
    cursor = conn.cursor()
    try:
        # Sort by ID to easily find the number you need
        cursor.execute("SELECT char_id, char_name FROM characters ORDER BY char_id ASC")
        rows = cursor.fetchall()
        
        print("\n--- CHARACTER REFERENCE LIST ---")
        # Loop prints 3 characters per line to keep the screen clean
        for i in range(0, len(rows), 3):
            chunk = rows[i:i+3]
            line = ""
            for c in chunk:
                line += f"[{c[0]:>2}] {c[1]:<15} | "
            print(line)
            
    except Exception as e:
        print(f" Error listing characters: {e}")
    finally:
        cursor.close()

def view_reports(conn):
    cursor = conn.cursor()
    try:
        # LEFT JOIN makes sure that even if player is missing a tag, the scouting note still shows up.
        query = """
            SELECT p.tag, s.weaknesses, s.last_updated 
            FROM scouting_reports s 
            LEFT JOIN players p ON s.player_id = p.player_id
            ORDER BY s.last_updated DESC
        """
        cursor.execute(query)
        reports = cursor.fetchall()
        
        if not reports:
            print("\n[!] The scouting table is currently empty.")
            print("Try recording a match (Option 3) first!")
            return

        print(f"\n{'Player Tag':<15} {'Scouting Note':<35} {'Last Updated'}")
        print("-" * 75)
        for r in reports:
            tag = r[0] if r[0] else "Unknown ID"
            print(f"{tag:<15} {r[1]:<35} {r[2]}")
    except Exception as e:
        print(f" Error Loading Reports: {e}")
    finally:
        cursor.close()
        
def delete_player(conn, player_id):
    cursor = None
    try:
        # FORCE RESET
        if conn.in_transaction:
            conn.rollback()

        p_id = int(player_id)
        cursor = conn.cursor()
        conn.start_transaction()


        # Deletes scouting reports first to avoid Foreign Key errors
        cursor.execute("DELETE FROM scouting_reports WHERE player_id = %s", (p_id,))
        
        # Delete match records where the player is either winner or loser 
        cursor.execute("DELETE FROM matches WHERE winner_id = %s OR loser_id = %s", (p_id, p_id))
        
        # Delete from player_characters 
        cursor.execute("DELETE FROM player_characters WHERE player_id = %s", (p_id,))

        # Finally, delete the player
        cursor.execute("DELETE FROM players WHERE player_id = %s", (p_id,))

        conn.commit()
    except Exception as e:
        if conn: conn.rollback() # Emergency exit
        print(f" Error: {e}")
    finally:
        if cursor: cursor.close()
        
def get_player_insight(conn, player_id):
    cursor = None
    try:
        p_id = int(player_id)
        cursor = conn.cursor()
        
        # Query gets Win/Loss Stats
        stats_query = """
            SELECT 
                (SELECT COUNT(*) FROM matches WHERE winner_id = %s) as wins,
                (SELECT COUNT(*) FROM matches WHERE loser_id = %s) as losses
        """
        cursor.execute(stats_query, (p_id, p_id))
        stats = cursor.fetchone()

        # Query 2:Gets the specific scouting report
        report_query = "SELECT tag, weaknesses FROM players LEFT JOIN scouting_reports ON players.player_id = scouting_reports.player_id WHERE players.player_id = %s"
        cursor.execute(report_query, (p_id,))
        report = cursor.fetchone()

        if report:
            print(f"\n--- INSIGHTS FOR: {report[0]} ---")
            print(f"Record: {stats[0]}W - {stats[1]}L")
            print(f"Scouting Notes: {report[1] if report[1] else 'No notes recorded yet.'}")
        else:
            print("\n[!] Player not found.")

    except Exception as e:
        print(f" Insight Error: {e}")
    finally:
        if cursor: cursor.close()