import json

# Data structures for inventory and orders
inventory = []
orders = []

# Load inventory from file
def load_inventory(filename='inventory.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save inventory to file
def save_inventory(filename='inventory.json'):
    with open(filename, 'w') as file:
        json.dump(inventory, file)
    print("Inventory saved.")

# Load orders from file
def load_orders(filename='orders.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save orders to file
def save_orders(filename='orders.json'):
    with open(filename, 'w') as file:
        json.dump(orders, file)
    print("Orders saved.")

# Sort inventory by SKU
def sort_inventory():
    global inventory
    inventory.sort(key=lambda item: item['SKU'])

# Sort orders by Order #
def sort_orders():
    global orders
    orders.sort(key=lambda order: order['order_number'])

# Add item to inventory
def add_item():
    name = input("Enter item name: ")
    sku = input("Enter item SKU: ")
    price = float(input("Enter item price: "))
    count = int(input("Enter item count: "))

    for item in inventory:
        if item['SKU'] == sku:
            item['count'] += count
            break
    else:
        inventory.append({'name': name, 'SKU': sku, 'price': price, 'count': count})

    sort_inventory()

# Remove item from inventory
def remove_item():
    global inventory  # Declare global inventory

    if not inventory:
        print("Inventory is empty.")
        input("\nPress Enter to return to the items menu...")
        return

    print("\nCurrent Inventory (Name and SKU):")
    for item in inventory:
        print(f"{item['name']}, SKU: {item['SKU']}")

    sku = input("\nEnter SKU of the item to remove: ")
    items = [item for item in inventory if item['SKU'] == sku]

    if not items:
        print("No items found with that SKU.")
        return

    count = items[0]['count']
    print(f"There are {count} item(s) with SKU: {sku}")

    to_remove = int(input(f"How many items with SKU {sku} do you want to remove? "))
    if to_remove > count:
        print(f"Cannot remove {to_remove} items. Only {count} item(s) available.")
        return

    for item in inventory:
        if item['SKU'] == sku:
            if to_remove >= item['count']:
                inventory.remove(item)
            else:
                item['count'] -= to_remove
            break

    print(f"Removed {to_remove} item(s) with SKU: {sku}")

    sort_inventory()

# Edit item in inventory
def edit_item():
    if not inventory:
        print("Inventory is empty.")
        return
    
    print("\nCurrent Inventory (Name and SKU):")
    for item in inventory:
        print(f"Name: {item['name']}, SKU: {item['SKU']}")
    
    sku = input("\nEnter SKU of the item to edit: ")
    items = [item for item in inventory if item['SKU'] == sku]
    
    if not items:
        print("No items found with that SKU.")
        return

    # Show details of the items with the given SKU
    for item in items:
        print(f"\nCurrent details of the item:\nName: {item['name']}\nSKU: {item['SKU']}\nPrice: {item['price']}\nCount: {item['count']}")
    
    print("\nSelect field to edit:")
    print("1- Name")
    print("2- SKU")
    print("3- Price")
    print("0- Cancel")
    choice = int(input("Enter choice: "))
    
    if choice == 0:
        return
    elif choice == 1:
        new_name = input("Enter new name: ")
        for item in items:
            item['name'] = new_name
    elif choice == 2:
        new_sku = input("Enter new SKU: ")
        for item in items:
            item['SKU'] = new_sku
    elif choice == 3:
        new_price = float(input("Enter new price: "))
        for item in items:
            item['price'] = new_price
    else:
        print("Invalid choice.")

    sort_inventory()

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

# Clear Inventory
def clear_inventory():
    print('You are about to clear the inventory')
    response = input('Type \'Clear\' to clear the inventory. Anything else will cancel. ')
    if response == 'Clear':
        inventory.clear()
        print('The inventory was cleared.')
    else:
        print('The inventory was not cleared.')
        return

# Main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1- Items Menu")
        print("2- Inventory Menu")
        print("3- Orders Menu")
        print("0- Quit")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            items_menu()
        elif choice == 2:
            inventory_menu()
        elif choice == 3:
            orders_menu()
        elif choice == 0:
            save_inventory()
            save_orders()
            print("Thank you for using the inventory system.")
            break
        else:
            print("Invalid choice. Please try again.")

# Items menu
def items_menu():
    while True:
        print("\nItems Menu:")
        print("1- Add Item")
        print("2- Remove Item")
        print("3- Edit Item")
        print("0- Main Menu")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            add_item()
        elif choice == 2:
            remove_item()
        elif choice == 3:
            edit_item()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

# Inventory menu
def inventory_menu():
    while True:
        print("\nInventory Menu:")
        print("1- Show Inventory")
        print("2- Save Inventory")
        print('3- Clear Inventory')
        print("0- Main Menu")
        choice = int(input("Enter choice: "))
        
        if choice == 1:
            view_inventory()
        elif choice == 2:
            save_inventory()
        elif choice == 3:
            clear_inventory()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

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
        elif choice == 6:
            save_orders()
        elif choice == 0:
            break
        else:
            print("Invalid choice. Please try again.")

# Load inventory and orders and start the main menu
inventory = load_inventory()
orders = load_orders()
sort_inventory()  # Sort inventory after loading
sort_orders()     # Sort orders after loading
main_menu()
