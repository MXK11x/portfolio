d = {'o': '👨', 0: ' ', 1: '🧱', 2: "", 3: "🚪", '.': '💰'}
p = {"char": "o", "x": 0, "y": 0, "score": 0}
size_map = (7, 20)
proportion_wall = 0.1

def display_map_char_and_objects(m, d, p, objects):
    # Calcul de la largeur de la carte en prenant en compte les bordures
    map_width = len(m[0]) + 2

    # Affichage d'une bordure supérieure
    print('═' * map_width)

    # Affichage de la carte avec des emojis
    for y, row in enumerate(m):
        print('║', end='')  # Bordure latérale gauche
        for x, cell in enumerate(row):
            if x == p['x'] and y == p['y']:
                print(d['o'], end='')  # Affichage du personnage
            elif (x, y) in objects:
                print('💰', end='')  # Affichage des objets
            else:
                print(d[cell], end='')  # Affichage de la carte
        print('║')  # Bordure latérale droite

    # Affichage d'une bordure inférieure
    print('═' * map_width)
    print("Score du joueur : %d" % (p['score']))
    
def delete_all_walls(m, pos): 
    x, y = pos 

    autour_p = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y),(x+1, y),(x-1, y+1), (x, y+1), (x+1, y+1)]

    for coord in autour_p: 
        x, y = coord 
        if 0 <= x < len(m[0]) and 0 <= y < len(m): 
            m[y][x] = 0  

def update_p(letter, p, m):
    maximum_x, maximum_y = len(m[0]) - 1, len(m) - 1
    if letter == "z" and p["y"] > 0 and m[p["y"] - 1][p["x"]] != 1:
        p["y"] -= 1  
    elif letter == "q" and p["x"] > 0 and m[p["y"]][p["x"] - 1] != 1:
        p["x"] -= 1  
    elif letter == "s" and p["y"] < maximum_y  and m[p["y"] + 1][p["x"]] != 1:
        p["y"] += 1  
    elif letter == "d" and p["x"] < maximum_x and m[p["y"]][p["x"] + 1] != 1:
        p["x"] += 1  
    elif letter == 'e':
        delete_all_walls(m, (p["x"], p["y"]))
    else:
        print("Le déplacement suggéré est impossible. Veuillez recommencer svp.")


import random
m = [[0,0,0,1,1],[0,0,0,0,1],[1,1,0,0,0],[0,0,0,0,0]]
def create_objects(nb_objects, m):
    maximum_x, maximum_y = len(m[0]) - 1, len(m) - 1
    objects = set()
    while len(objects) < nb_objects:
        objet_x, objet_y = random.randint(1, maximum_x), random.randint(1, maximum_y)
        if m[objet_y][objet_x] == 0:
            objects.add((objet_x, objet_y))
    return objects
objects = create_objects(random.randint(0, 10),m)


def update_objects(p, objects):
    position_joueur = (p["x"], p["y"])
    if position_joueur in objects:
        objects.remove(position_joueur)
        p["score"] += 1
        print("L’objet est ramassé ! Score actuel : %d" % p["score"])
        
import random
def generate_random_map(size_map, proportion_wall):
    l, L = size_map
    nouvelle_m = [[0] * L for i in range(l)]
    entrée_x, entrée_y = random.randint(0, L - 1), random.randint(0, l - 1)
    sortie_x, sortie_y = random.randint(0, L - 1), random.randint(0, l - 1)
    nouvelle_m[entrée_y][entrée_x] = 2
    nouvelle_m[sortie_y][sortie_x] = 3
    for i in range(l):
        for j in range(L):
            if nouvelle_m[i][j] == 0 and random.random() < proportion_wall:
                nouvelle_m[i][j] = 1  
    return nouvelle_m


random_map= generate_random_map(size_map, proportion_wall)

def create_new_level(p, m, obj, size_map, proportion_wall, nouvelle_position_sortie=None):
    nouvelle_m = generate_random_map(size_map, proportion_wall)

    if nouvelle_position_sortie is None:
        entrée_coords = None
        for j, j_list in enumerate(nouvelle_m):
            for i, value in enumerate(j_list):
                if value == ' ':
                    entrée_coords = (i, j)
                    break
            if entrée_coords:
                break
    else:
        entrée_coords = nouvelle_position_sortie

    p['x'], p['y'] = entrée_coords

    m[:] = nouvelle_m

    obj.clear()
    obj.update(create_objects(3, m))

    nouvelle_position_sortie = None
    for row, row_list in enumerate(nouvelle_m):
        for col, value in enumerate(row_list):
            if value == 3:
                nouvelle_position_sortie = (col, row)
                break
        if nouvelle_position_sortie:
            break

    return nouvelle_position_sortie

nouvelle_position_sortie = None

while True:
    letter = input("Veuillez entrer une lettre (z, q, s, d) pour déplacer le joueur : ")
    if letter == 'fin':
        break  
    update_p(letter, p, random_map)
    update_objects(p, objects)
    display_map_char_and_objects(random_map, d, p, objects)
    if random_map[p['y']][p['x']] == 3:
        print("Félicitations! Vous avez atteint la sortie du niveau!")
        nouvelle_position_sortie = p['x'], p['y']
        nouvelle_position_sortie = create_new_level(p, random_map, objects, size_map, proportion_wall, nouvelle_position_sortie)

print("Merci d'avoir joué!")