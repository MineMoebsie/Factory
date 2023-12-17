import json

with open("Data/storage_menu_layout.json") as f:
    storage_menu_layout = json.load(f)

items_used = []
for category in storage_menu_layout:
    print(category)
    for item in storage_menu_layout[category]:
        print(item)
        items_used.append(item)

items_used = sorted(items_used)
prev_item = 0
for item in items_used:
    if prev_item != item - 1:
        
        print("unincluded", item-1)

    prev_item = item