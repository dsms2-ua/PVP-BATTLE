from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item


#Crear magia de ataque
fire = Spell("Fire", 25, 600, "Black")
thunder = Spell("Thunder", 25, 600, "Black")
blizzard = Spell("Blizzard", 25, 600, "Black")
meteor = Spell("Meteor", 40, 1200, "Black")
quake = Spell("Quake", 14, 1400, "Black")

#Crear magia de cura
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

#Crear algunos objetos
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Superpotion", "potion", "Heals 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores MP/HP of one of party member", 9999)
hielixer = Item("Mega-Elixer", "elixer", "Fully restores party´s HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

#Definir una lista con los diferentes elementos

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

#Crear diferentes jugadores
player1 = Person("Player1:", 4600, 132, 300, 34, player_magic, player_items)
player2 = Person("Player2:", 4200, 188, 310, 34, player_magic, player_items)
player3 = Person("Player3:", 5200, 174, 290, 34, player_magic, player_items)
enemy = Person("Enemy", 3000, 65, 525, 25, [], [])

players = [player1, player2, player3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=================================")
    print("\n\n")
    print("NAME                      HP                                     MP")

    for player in players:
        player.get_stats()

    print("\n")

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)

            print("You attacked for ", dmg, "points of damage.")

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic:")) - 1

            if magic_choice == -1:   #Nos permite volver atrás al menú pulsando el 0
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":

                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "Black":       
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose an item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixer":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage."+ bcolors.ENDC)
        enemy_dmg = enemy.generate_damage()
        player1.take_damage(enemy_dmg) 
        print("Enemy attacks for", str(enemy_dmg))

    enemy_choice = 1  

    print("_________________________________")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you" + bcolors.ENDC)
        running = False