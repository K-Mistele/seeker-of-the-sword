custom_map = open("custom_map.txt")
tile = []
for line in custom_map:
    tile.append(list(line.strip("\n")))
print(tile)
for row in tile:
    print(" ".join(row))
print("\n")
print(len(tile))
print(len(tile[0]))