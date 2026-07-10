#!/usr/bin/env python3
import sys
import requests

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n" + "="*50)
    print("      INVENTORY MANAGEMENT SYSTEM PORTAL")
    print("="*50)
    print("1. View Full Stock Inventory")
    print("2. Search Specific Item ID")
    print("3. Register New Manual Stock Entry")
    print("4. Modify Stock Quantity or Unit Valuation Price")
    print("5. Purge Inventory Record (Delete)")
    print("6. Query & Import via OpenFoodFacts Barcode")
    print("7. Terminate Interface")
    print("="*50)

def view_all():
    res = requests.get(f"{BASE_URL}/inventory")
    if res.status_code == 200:
        items = res.json()
        print(f"\n{'ID':<5} | {'Product Name':<25} | {'Brand':<15} | {'Stock':<6} | {'Price':<8}")
        print("-" * 70)
        for i in items:
            print(f"{i['id']:<5} | {i['product_name'][:25]:<25} | {i['brands'][:15]:<15} | {i['quantity']:<6} | ${i['price']:<8.2f}")
    else:
        print("Failed to retrieve inventory records.")

def view_one():
    item_id = input("Enter Item Target Database ID: ")
    res = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if res.status_code == 200:
        i = res.json()
        print(f"\n[ID {i['id']}] {i['product_name']} - Brand: {i['brands']}")
        print(f"Ingredients: {i['ingredients_text']}")
        print(f"Current Available Stock Count: {i['quantity']} items")
        print(f"Individual Base Valuation: ${i['price']:.2f}")
    else:
        print(f"Error: {res.json().get('error', 'Item could not be extracted')}")

def add_manual():
    print("\n--- Manual Record Profiling Input ---")
    name = input("Product Label Name (Required): ")
    if not name:
        print("Operation Aborted: Label cannot be null.")
        return
    brand = input("Manufacturer Brand Label Name: ") or "Unknown"
    ing = input("Ingredients Description Text Block: ") or "N/A"
    qty = int(input("Starting Warehouse Unit Count: ") or 0)
    price = float(input("Target Sales Unit Evaluation Price: ") or 0.0)
    
    payload = {"product_name": name, "brands": brand, "ingredients_text": ing, "quantity": qty, "price": price}
    res = requests.post(f"{BASE_URL}/inventory", json=payload)
    if res.status_code == 201:
        print(f"Success! Item allocated database index: {res.json()['id']}")
    else:
        print("Failed to push inventory modification record.")

def patch_record():
    item_id = input("Enter target item database reference ID to modify: ")
    print("Leave field empty to retain existing state settings.")
    qty = input("New Target Stock Quantity Count: ")
    price = input("Updated Unit Market Valuation Price: ")
    
    payload = {}
    if qty: payload["quantity"] = int(qty)
    if price: payload["price"] = float(price)
    
    res = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
    if res.status_code == 200:
        print("Database record state updated successfully.")
    else:
        print(f"Error executing update operation: {res.json().get('error')}")

def delete_record():
    item_id = input("Enter index profile ID targeted for permanent destruction: ")
    res = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if res.status_code == 200:
        print("Record cleared from persistent infrastructure layers.")
    else:
        print(f"Error: {res.json().get('error')}")

def import_external():
    barcode = input("Scan or Input Target Product Barcode Number: ")
    if not barcode: return
    
    print("Contacting external network API registry points...")
    res = requests.get(f"{BASE_URL}/api/external/fetch?barcode={barcode}")
    if res.status_code == 200:
        ext_data = res.json()
        print(f"\nLocated: {ext_data['product_name']} [{ext_data['brands']}]")
        confirm = input("Import this asset configuration directly into inventory tracking array? (y/n): ")
        if confirm.lower() == 'y':
            qty = int(input("Assign initial stock count size: ") or 0)
            price = float(input("Assign standard floor valuation sales price: ") or 0.0)
            ext_data["quantity"] = qty
            ext_data["price"] = price
            
            save_res = requests.post(f"{BASE_URL}/inventory", json=ext_data)
            if save_res.status_code == 201:
                print(f"Asset successfully tracking inside database layout under ID: {save_res.json()['id']}")
    else:
        print("Resource not found in external lookup databases.")

def main():
    while True:
        show_menu()
        choice = input("Enter operating instruction code (1-7): ")
        if choice == '1': view_all()
        elif choice == '2': view_one()
        elif choice == '3': add_manual()
        elif choice == '4': patch_record()
        elif choice == '5': delete_record()
        elif choice == '6': import_external()
        elif choice == '7':
            print("Shutting down administrative operations portal link...")
            sys.exit(0)
        else:
            print("Invalid code matrix parameter path chosen.")

if __name__ == "__main__":
    main()
