import random
import json
import os

logged_in = False
current_user = None

## Everything related to Save/Load ##
# Function to load data from a JSON file
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

# Function to save data to a JSON file
def save_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def login_menu():
    while not logged_in:
        user_id = int(input("Enter your User ID: "))
        user = next((u for u in users if u['id'] == user_id), None)
        if user is None:
            print("User ID not found. Please try again.")
            continue

        password = input("Enter your password: ")
        if user['password'] == password:
            print(f"Welcome, {user['name']}!")
            current_user = user
        else:
            print("Incorrect password. Please try again.")

## Main Menu ##
# Function to display the main menu
def main_menu():
    print(f'Logged in: {logged_in}, ID: {current_user["id"]}, Name: {current_user["name"]}, Is_Admin: {current_user["is_admin"]}')
    while True:
        print("\nMain Menu:")
        print("1- Inventory Menu")
        print("2- Order Menu")
        print("3- Manifest Menu")
        if current_user['is_admin']: print('4- User Menu')
        print("0- Exit")
        choice = int(input("Enter choice: "))

        if choice == 0:
            app_quit()
        elif choice == 1:
            inventory_menu()
        elif choice == 2:
            orders_menu()
        elif choice == 3:
            manifest_menu()
        elif choice == 4 and current_user['is_admin']:
            user_menu()
        else:
            print("Invalid choice.")

## Everything related to Inventory ##
# Function to display the inventory menu
def inventory_menu():
    while True:
        print("\nInventory Menu:")
        print("1- View Inventory")
        print("2- Add Item")
        print("3- Remove Item")
        print("4- Edit Item")
        print("0- Main Menu")
        choice = int(input("Enter choice: "))

        if choice == 0:
            break
        elif choice == 1:
            view_inventory()
        elif choice == 2:
            add_inventory_item()
        elif choice == 3:
            remove_inventory_item()
        elif choice == 4:
            edit_inventory_item()
        else:
            print("Invalid choice.")

def view_inventory():
    return

def add_inventory_item():
    return

def remove_inventory_item():
    return

def edit_inventory_item():
    return

## Everything related to Orders ##
# Orders menu
def orders_menu():
    while True:
        print("\nOrders Menu:")
        print("1- Create Order")
        print("2- Remove Order")
        print("3- Edit Order")
        print("4- View Order")
        print("5- View All Orders")
        print("6- Save Orders")
        print("0- Main Menu")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            create_order()
        elif choice == 2:
            remove_order()
        elif choice == 3:
            edit_order()
        elif choice == 4:
            view_order()
        elif choice == 5:
            view_all_orders()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

def create_order():
    return

def remove_order():
    return

def edit_order():
    return

def view_order():
    return

def view_all_orders():
    return

## Everything related to Manifests ##
# Function to display the manifest menu
def manifest_menu():
    while True:
        print("\nManifest Menu:")
        print("1- Generate Manifest")
        print("2- Receive Manifest")
        print("3- Delete Manifest")
        print("4- Update Manifest Pool")
        print("0- Main Menu")
        choice = int(input("Enter choice: "))

        if choice == 0:
            break
        elif choice == 1:
            generate_manifest(manifests, item_pool)
        elif choice == 2:
            receive_manifest(manifests, inventory)
        elif choice == 3:
            delete_manifest(manifests)
        elif choice == 4:
            update_items(item_pool)
        else:
            print("Invalid choice.")

def generate_manifest():
    return

def receive_manifest():
    return

def delete_manifest():
    return

def update_items():
    return

def user_menu():
    while True:
        print("\nUser Menu:")
        print("1- Add User")
        print("2- Remove User")
        print("0- Main Menu")
        choice = int(input("Enter choice: "))
        if choice == 0:
            break
        elif choice == 1:
            add_user(users)
        elif choice == 2:
            remove_user(users)
        else:
            print("Invalid choice.")

# Add User
def add_user(users):
    name = input("Enter user name: ")
    user_id = int(input("Enter user ID: "))
    if any(u['id'] == user_id for u in users):
        print("User ID already exists. Please choose a different ID.")
        return
    password = input("Enter user password: ")
    is_admin = input("Is the user an admin? (1- Yes, 2- No): ") == '1'
    users.append({'id': user_id, 'password': password, 'name': name, 'is_admin': is_admin})
    print("User added successfully.")

# Remove User
def remove_user(users):
    for u in users:
        print(f"Name: {u['id']}, Items: {u['name']}")
    user_id = int(input("Enter the user ID to remove: "))
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        print("User ID not found.")
        return
    confirm_id = int(input("Confirm by typing the user ID again: "))
    if user_id == confirm_id:
        users.remove(user)
        print("User removed successfully.")
    else:
        print("User ID does not match. Aborting.")

def app_quit():
    save_data(inventory, 'save_Inventory.json')
    save_data(orders, 'save_Orders.json')
    save_data(manifests, 'save_Manifests.json')
    save_data(item_pool, 'save_Items.json')
    save_data(users, 'save_Users')
    print('Thank you for using the Inventory system.')

## Everything related to Startup ##
# Initialize data structures
inventory = load_data('save_Inventory.json')
orders = load_data('save_Orders.json')
manifests = load_data('save_Manifests.json')
item_pool = load_data('save_Items.json')
users = load_data('save_Users.json')

# Main execution
if __name__ == "__main__":
    login_menu()
