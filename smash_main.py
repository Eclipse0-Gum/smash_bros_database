import smash_database as db

def main():
    conn = db.get_connection()  
    if not conn: return

    while True:
        print("\n--- SMASH SCOUTING SYSTEM ---")
        print("1. Add Player")
        print("2. Update Player Main")
        print("3. Record Match & Note")
        print("4. View All Players")
        print("5. View Scouting Reports")
        print("6. Exit")
        print("7. DELETE Player")
        print("8. Get Player Insights (W/L + Notes)")
        
        choice = input("Select: ")

        if choice == '1':
            db.add_player(conn, input("Tag: "), input("Region: "))
        elif choice == '2':
            print("\n--- MANAGE MAINS ---")
            print("a. Add/Update a Main")
            print("b. Delete a Main")
            sub_choice = input("Select (a/b): ").lower()

            if sub_choice == 'a':
                db.list_characters(conn)
                p_id = input("\nEnter Player ID: ")
                c_id = input("Enter Character ID: ")
                level = input("Skill Level (1-10): ")
                db.update_mains(conn, p_id, c_id, level)
            elif sub_choice == 'b':
                p_id = input("Enter Player ID: ")
                c_id = input("Enter Character ID to REMOVE: ")
                db.delete_main(conn, p_id, c_id)
            else:
                print("Invalid sub-option.")
        elif choice == '3':
            w = input("Winner ID: ")
            l = input("Loser ID: ")
            n = input("Note: ")
            db.record_match_and_scout(conn, w, l, n)
        elif choice == '4':
            db.view_players(conn)
        elif choice == '5':
            db.view_reports(conn)
        elif choice == '6':
            conn.close()
            break
        elif choice == '7':
            target_id = input("Enter Player ID to DELETE: ")
            confirm = input(f"Are you sure you want to delete Player {target_id}? (y/n): ")
            if confirm.lower() == 'y':
                db.delete_player(conn, target_id)
        elif choice == '8':
            p_id = input("Enter Player ID for detailed insight: ")
            db.get_player_insight(conn, p_id)
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()