import json
import os

DB_FILE = "db.json"

def init_db():
    if not os.path.exists(DB_FILE):
        default_data = {
            "user_id_123": {
                "name": "Ramesh",
                "leave_balance": 12,
                "role": "Factory Worker"
            }
        }
        with open(DB_FILE, "w") as f:
            json.dump(default_data, f, indent=4)

def get_user_data(user_id="user_id_123"):
    init_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return data.get(user_id, None)

def apply_leave(days, user_id="user_id_123"):
    init_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    
    user = data.get(user_id)
    if not user:
        return False, "User not found."
    
    if user["leave_balance"] >= days:
        user["leave_balance"] -= days
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True, f"Leave approved. Remaining balance: {user['leave_balance']}"
    else:
        return False, f"Insufficient balance. You only have {user['leave_balance']} days left."

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
    print("Current data:", get_user_data())
