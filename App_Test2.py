import random
import json
import os

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

# Function to generate a manifest
def generate_manifest(manifests, item_pool):
    if not item_pool:
        print("Item pool is empty. Please update the item pool first.")
        return

    manifest_number = random.randint(1000, 9999)
    while any(manifest['manifest_number'] == manifest_number for manifest in manifests):
        manifest_number = random.randint(1000, 9999)

    num_items = random.randint(5, 50)
    items = []
    for _ in range(num_items):
        item = random.choice(item_pool)
        items.append(item)

    manifests.append({'manifest_number': manifest_number, 'items': items})
    sort_manifests(manifests)
    print(f"Manifest {manifest_number} generated with {num_items} items.")

# Function to sort manifests by manifest number
def sort_manifests(manifests):
    manifests.sort(key=lambda x: x['manifest_number'])

# Function to receive a manifest
def receive_manifest(manifests, inventory):
    if not manifests:
        print("No open manifests available.")
        return

    print("\nOpen Manifests:")
    for manifest in manifests:
        print(f"Manifest: {manifest['manifest_number']}, Items: {len(manifest['items'])}")

    manifest_number = int(input("\nEnter the manifest number to receive: "))
    manifest = next((m for m in manifests if m['manifest_number'] == manifest_number), None)
    
    if not manifest:
        print("Manifest not found.")
        return

    print(f"\nManifest: {manifest_number}")
    for item in manifest['items']:
        print(f"Name: {item['name']}, SKU: {item['SKU']}, Count: {item.get('count', 1)}")

    choice = int(input(f"\nAre you are sure you want to receive Manifest: {manifest_number}? (1- Yes, 0- No): "))

    if choice == 1:
        for item in manifest['items']:
            found = False
            for inv_item in inventory:
                if inv_item['SKU'] == item['SKU']:
                    inv_item['count'] += item.get('count', 1)
                    found = True
                    break
            if not found:
                inventory.append({
                    'name': item['name'],
                    'SKU': item['SKU'],
                    'price': item['price'],
                    'count': item.get('count', 1)
                })
        manifests.remove(manifest)
        sort_inventory(inventory)
        print("Manifest received and items added to inventory.")
    elif choice == 0:
        print("Manifest not received.")

# Function to delete a manifest
def delete_manifest(manifests):
    if not manifests:
        print("No open manifests available.")
        return

    print("\nOpen Manifests:")
    for manifest in manifests:
        print(f"Manifest: {manifest['manifest_number']}, Items: {len(manifest['items'])}")

    manifest_number = int(input("\nEnter the manifest number to delete: "))
    manifest = next((m for m in manifests if m['manifest_number'] == manifest_number), None)
    
    if not manifest:
        print("Manifest not found.")
        return

    confirm = int(input(f"Are you sure you want to delete Manifest {manifest_number}? (1- Yes, 2- No): "))
    if confirm == 1:
        manifests.remove(manifest)
        print("Manifest deleted.")

# Function to update the Item pool
def update_item_pool(item_pool):
    while True:
        print("\nUpdate Item Pool:")
        print("1- Add Item")
        print("2- Remove Item")
        print("3- Edit Item")
        print("0- Return to Manifest Menu")
        choice = int(input("Enter choice: "))

        if choice == 0:
            break
        elif choice == 1:
            add_manifest_item(item_pool)
        elif choice == 2:
            remove_manifest_item(item_pool)
        elif choice == 3:
            edit_manifest_item(item_pool)
        else:
            print("Invalid choice.")

# Function to add an item to the Item pool
def add_manifest_item(item_pool):
    name = input("Enter item name: ")
    sku = input("Enter item SKU: ")
    price = float(input("Enter item price: "))

    if any(item['SKU'] == sku for item in item_pool):
        print("SKU already exists. Please use a different SKU.")
        return

    item_pool.append({'name': name, 'SKU': sku, 'price': price})
    print("Item added to item pool.")

# Function to remove an item from the Item pool
def remove_manifest_item(item_pool):
    if not item_pool:
        print("Item pool is empty.")
        return

    print("\Item Pool:")
    for item in item_pool:
        print(f"Name: {item['name']}, SKU: {item['SKU']}")

    sku = input("\nEnter SKU of the item to remove: ")
    item = next((item for item in item_pool if item['SKU'] == sku), None)
    
    if not item:
        print("Item not found.")
        return

    confirm = int(input(f"Are you sure you want to remove {item['name']} (SKU: {sku})? (1- Yes, 2- No): "))
    if confirm == 1:
        item_pool.remove(item)
        print("Item removed from item pool.")

# Function to edit an item in the Item pool
def edit_manifest_item(item_pool):
    if not item_pool:
        print("Item pool is empty.")
        return

    print("\Item Pool:")
    for item in item_pool:
        print(f"Name: {item['name']}, SKU: {item['SKU']}")

    sku = input("\nEnter SKU of the item to edit: ")
    item = next((item for item in item_pool if item['SKU'] == sku), None)
    
    if not item:
        print("Item not found.")
        return

    print("\nSelect field to edit:")
    print("1- Name")
    print("2- SKU")
    print("3- Price")
    print("0- Cancel")
    choice = int(input("Enter choice: "))

    if choice == 0:
        return
    elif choice == 1:
        item['name'] = input("Enter new name: ")
    elif choice == 2:
        new_sku = input("Enter new SKU: ")
        if any(it['SKU'] == new_sku for it in item_pool):
            print("SKU already exists. Please use a different SKU.")
            return
        item['SKU'] = new_sku
    elif choice == 3:
        item['price'] = float(input("Enter new price: "))
    else:
        print("Invalid choice.")
    
    print("Item updated in item pool.")

# Function to sort inventory by SKU
def sort_inventory(inventory):
    inventory.sort(key=lambda x: x['SKU'])

# Function to display the main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1- Inventory Menu")
        print("2- Order Menu")
        print("3- Manifest Menu")
        print("0- Exit")
        choice = int(input("Enter choice: "))

        if choice == 0:
            save_data(inventory, 'save_Inventory.json')
            save_data(orders, 'save_Orders.json')
            save_data(manifests, 'save_Manifests.json')
            save_data(item_pool, 'save_Items.json')
            break
        elif choice == 1:
            inventory_menu()
        elif choice == 2:
            orders_menu()
        elif choice == 3:
            manifest_menu()
        else:
            print("Invalid choice.")

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

# View inventory
def view_inventory():
    if not inventory:
        print("Inventory is empty.")
        input("\nPress Enter to return to the menu...")
        return

    print("\nCurrent Inventory:")

    for item in inventory:
        total_cost = item['price'] * item['count']
        cost_per_item = item['price']
        print(f"{item['count']} {item['name']}(s), SKU: {item['SKU']}, Cost: ${cost_per_item:.2f}, Retail Price: ${total_cost:.2f}")

    choice = int(input("\nDo you want to see the inventory value? (1- Yes, 0- No): ").strip())
    if choice == 1:
        sku_count = {}
        total_items = 0
        total_value = 0.0
        for item in inventory:
            if item['SKU'] in sku_count:
                sku_count[item['SKU']]['count'] += item['count']
            else:
                sku_count[item['SKU']] = {'name': item['name'], 'price': item['price'], 'count': item['count']}
            total_items += item['count']
            total_value += item['price'] * item['count']

        print(f"\nUnique items: {len(sku_count)}")
        print(f"Total items: {total_items}")
        print(f"Total retail value: ${total_value:.2f}")
        input("\nPress Enter to return to the menu...")

# Function to add an item to inventory
def add_inventory_item():
    name = input("Enter item name: ")
    sku = input("Enter item SKU: ")
    price = float(input("Enter item price: "))
    count = int(input("Enter item count: "))

    if any(item['SKU'] == sku for item in inventory):
        print("SKU already exists in inventory. Please use a different SKU.")
        return

    inventory.append({'name': name, 'SKU': sku, 'price': price, 'count': count})
    print("Item added to inventory.")

# Function to remove an item from inventory
def remove_inventory_item():
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nInventory:")
    for item in inventory:
        print(f"Name: {item['name']}, SKU: {item['SKU']}")

    sku = input("\nEnter SKU of the item to remove: ")
    item = next((item for item in inventory if item['SKU'] == sku), None)
    
    if not item:
        print("Item not found in inventory.")
        return

    confirm = int(input(f"Are you sure you want to remove {item['name']} (SKU: {sku})? (1- Yes, 2- No): "))
    if confirm == 1:
        inventory.remove(item)
        print("Item removed from inventory.")

# Function to edit an item in inventory
def edit_inventory_item():
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nInventory:")
    for item in inventory:
        print(f"Name: {item['name']}, SKU: {item['SKU']}")

    sku = input("\nEnter SKU of the item to edit: ")
    item = next((item for item in inventory if item['SKU'] == sku), None)
    
    if not item:
        print("Item not found in inventory.")
        return

    print("\nSelect field to edit:")
    print("1- Name")
    print("2- SKU")
    print("3- Price")
    print("4- Count")
    print("0- Cancel")
    choice = int(input("Enter choice: "))

    if choice == 0:
        return
    elif choice == 1:
        item['name'] = input("Enter new name: ")
    elif choice == 2:
        new_sku = input("Enter new SKU: ")
        if any(it['SKU'] == new_sku for it in inventory):
            print("SKU already exists in inventory. Please use a different SKU.")
            return
        item['SKU'] = new_sku
    elif choice == 3:
        item['price'] = float(input("Enter new price: "))
    elif choice == 4:
        item['count'] = int(input("Enter new count: "))
    else:
        print("Invalid choice.")
    
    print("Item updated in inventory.")

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


# Sort orders by Order #
def sort_orders():
    global orders
    orders.sort(key=lambda order: order['order_number'])

# Create an order
def create_order():
    if not inventory:
        print('There are no items in the inventory. Add an item to the inventory first!')
        return
    name = input("Enter customer name: ")
    phone = input("Enter phone number: ")
    order_number = int(input("Enter order number: "))
    
    order_items = []
    while True:
        # Show current inventory
        print("\nCurrent Inventory (Name, SKU):")
        for item in inventory:
            print(f"{item['name']}, SKU: {item['SKU']}")

        sku = input("Enter item SKU to add to the order: ")
        item = next((item for item in inventory if item['SKU'] == sku), None)
        if not item:
            print("Item not found in inventory.")
            continue
        
        if item['count'] > 1:
            count = int(input(f"There are {item['count']} of this item. How many do you want to add? "))
        else:
            count = 1
        
        if count > item['count']:
            print(f"Cannot add {count} items. Only {item['count']} available.")
            continue
        
        order_items.append({'SKU': sku, 'name': item['name'], 'price': item['price'], 'count': count})
        item['count'] -= count
        if item['count'] == 0:
            inventory.remove(item)
        
        more_items = int(input("Do you want to add more items to the order? (1- Yes, 0- No): "))
        if more_items == 0:
            break
    
    total_price = sum(item['price'] * item['count'] for item in order_items)
    orders.append({'order_number': order_number, 'name': name, 'phone': phone, 'items': order_items, 'total_price': total_price})
    
    sort_orders()
    print("Order created successfully.")

# Remove an order
def remove_order():
    order_number = int(input("Enter the order number to remove: "))
    order = next((order for order in orders if order['order_number'] == order_number), None)
    if not order:
        print("Order not found.")
        return
    
    confirm = int(input("Are you sure you want to remove the order? (1- Yes, 0- No): "))
    if confirm == 1:
        orders.remove(order)
        print("Order removed successfully.")

# Edit an order
def edit_order():
    order_number = int(input("Enter the order number to edit: "))
    order = next((order for order in orders if order['order_number'] == order_number), None)
    if not order:
        print("Order not found.")
        return
    
    print("\nSelect field to edit:")
    print("1- Name")
    print("2- Phone #")
    print("3- Order #")
    print("4- Items")
    print("0- Cancel")
    choice = int(input("Enter choice: "))
    
    if choice == 0:
        return
    elif choice == 1:
        order['name'] = input("Enter new name: ")
    elif choice == 2:
        order['phone'] = input("Enter new phone number: ")
    elif choice == 3:
        order['order_number'] = int(input("Enter new order number: "))
    elif choice == 4:
        while True:
            print("\nCurrent items in order:")
            for item in order['items']:
                print(f"{item['name']}, SKU: {item['SKU']}, Count: {item['count']}")
            
            print("\nSelect option:")
            print("1- Add item(s)")
            print("2- Remove item(s)")
            print("0- Cancel")
            sub_choice = int(input("Enter choice: "))
            
            if sub_choice == 0:
                break
            elif sub_choice == 1:
                # Show current inventory
                print("\nCurrent Inventory (Name, SKU):")
                for item in inventory:
                    print(f"{item['name']}, SKU: {item['SKU']}")

                sku = input("Enter item SKU to add to the order: ")
                item = next((item for item in inventory if item['SKU'] == sku), None)
                if not item:
                    print("Item not found in inventory.")
                    continue
                
                if item['count'] > 1:
                    count = int(input(f"There are {item['count']} of this item. How many do you want to add? "))
                else:
                    count = 1
                
                if count > item['count']:
                    print(f"Cannot add {count} items. Only {item['count']} available.")
                    continue
                
                order_item = next((i for i in order['items'] if i['SKU'] == sku), None)
                if order_item:
                    order_item['count'] += count
                else:
                    order['items'].append({'SKU': sku, 'name': item['name'], 'price': item['price'], 'count': count})
                
                item['count'] -= count
                if item['count'] == 0:
                    inventory.remove(item)
            
            elif sub_choice == 2:
                print("\nCurrent items in order (Name, SKU):")
                for item in order['items']:
                    print(f"{item['name']}, SKU: {item['SKU']}, Count: {item['count']}")

                sku = input("Enter item SKU to remove from the order: ")
                order_item = next((item for item in order['items'] if item['SKU'] == sku), None)
                if not order_item:
                    print("Item not found in the order.")
                    continue
                
                if order_item['count'] > 1:
                    count = int(input(f"There are {order_item['count']} of this item in the order. How many do you want to remove? "))
                else:
                    count = 1
                
                if count > order_item['count']:
                    print(f"Cannot remove {count} items. Only {order_item['count']} available.")
                    continue
                
                order_item['count'] -= count
                if order_item['count'] == 0:
                    order['items'].remove(order_item)
                
                # Add removed items back to inventory
                inventory_item = next((item for item in inventory if item['SKU'] == sku), None)
                if inventory_item:
                    inventory_item['count'] += count
                else:
                    inventory.append({'name': order_item['name'], 'SKU': sku, 'price': order_item['price'], 'count': count})
                sort_inventory()
        
        # Recalculate the total price
        order['total_price'] = sum(item['price'] * item['count'] for item in order['items'])
    
    sort_orders()
    print("Order edited successfully.")

# View an order
def view_order():
    order_number = int(input("Enter the order number to view: "))
    order = next((order for order in orders if order['order_number'] == order_number), None)
    if not order:
        print("Order not found.")
        return
    
    print(f"\nOrder #: {order['order_number']:04d}")
    print(f"Name: {order['name']}")
    print(f"Phone #: {order['phone']}")
    print("Items:")
    for item in order['items']:
        total_price = item['price'] * item['count']
        print(f"{item['count']} {item['name']}(s), SKU: {item['SKU']}, Price: ${item['price']:.2f}, Total: ${total_price:.2f}")
    print(f"Total Price: ${order['total_price']:.2f}")
    
    input("\nPress Enter to return to the menu...")

# View all orders
def view_all_orders():
    if not orders:
        print("No orders found.")
        input("\nPress Enter to return to the menu...")
        return
    
    print("\nAll Orders:")
    for order in orders:
        print(f"Order #: {order['order_number']:04d}, Name: {order['name']}, Phone #: {order['phone']}, Total Price: ${order['total_price']:.2f}")
    
    input("\nPress Enter to return to the menu...")

# Function to display the manifest menu
def manifest_menu():
    while True:
        print("\nManifest Menu:")
        print("1- Generate Manifest")
        print("2- Receive Manifest")
        print("3- Delete Manifest")
        print("4- Update Item Pool")
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
            update_item_pool(item_pool)
        else:
            print("Invalid choice.")

# Function to sort inventory by SKU
def sort_inventory(inventory):
    inventory.sort(key=lambda x: x['SKU'])

# Initialize data structures
inventory = load_data('save_Inventory.json')
orders = load_data('save_Orders.json')
manifests = load_data('save_Manifests.json')
item_pool = load_data('save_Items.json')

# Main execution
if __name__ == "__main__":
    main_menu()
