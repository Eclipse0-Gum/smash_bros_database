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

# 2. Database

def add_player(conn, tag, region):
    """Adds a player using parameters to prevent SQL injection"""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (tag, region) VALUES (%s, %s)", (tag, region))
        conn.commit()
        print(f"Player '{tag}' added!")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

def get_players(conn):
    """Gets all players"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT player_id, tag, region FROM players")
        return cursor.fetchall()
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()

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
    """Records the match and updates scouting report for future reference."""
    try:
        cursor = conn.cursor()
        conn.start_transaction() 

        # Step 1: Insert the match result
        cursor.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (winner_id, loser_id))
        
        # Step 2: Update the scout report for the loser
        cursor.execute("UPDATE scouting_reports SET weaknesses = %s WHERE player_id = %s", (notes, loser_id))

        conn.commit() # If done right, should be safe to commit
        print("Transaction Complete: Match recorded and Scouting updated.")
    except Error as e:
        conn.rollback() # Prevents updating if there's an error anywhere 
        print(f"Transaction Failed: {e}")
    finally:
        cursor.close()

# 3. The User Interface

def main():
    db = get_connection()
    if not db: return

    while True:
        print("\n--- SSBU SCOUTING SYSTEM ---")
        print("1. View Players\n2. Add Player\n3. Record Match (Transaction)\n4. Delete Player\n5. Exit")
        choice = input("Choice: ")

        if choice == '1':
            data = get_players(db)
            print(f"\n{'ID':<5} {'Tag':<20} {'Region':<15}")
            for p in data: print(f"{p[0]:<5} {p[1]:<20} {p[2]:<15}")

        elif choice == '2':
            tag = input("Tag: ")
            reg = input("Region: ")
            add_player(db, tag, reg)

        elif choice == '3':
            win = input("Winner ID: ")
            los = input("Loser ID: ")
            note = input("Anything new to note? ")
            record_match_and_scout(db, win, los, note)

        elif choice == '4':
            pid = input("Player ID to delete: ")
            if input(f"Confirm delete ID {pid}? (y/n): ").lower() == 'y':
                delete_player(db, pid)

        elif choice == '5':
            db.close()
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()