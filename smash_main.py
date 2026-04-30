import smash_database as database # This imports all your functions from database.py

def main():
    db = database.get_connection()
    if not db: return

    while True:
        print("\n--- SSBU SCOUTING SYSTEM ---")
        print("1. View Players")
        print("2. View Reports")
        print("3. Record Match & Note") # This is your Option 5
        print("4. Exit")
        
        choice = input("Select: ")
        if choice == '1':
            players = database.get_players(db)
            for p in players: print(p)
        elif choice == '2':
            database.view_scouting_reports(db)
        elif choice == '3':
            w = input("Winner ID: ")
            l = input("Loser ID: ")
            n = input("New Weakness Note: ")
            database.record_match_and_scout(db, w, l, n)
        elif choice == '4':
            db.close()
            break

if __name__ == "__main__":
    main()