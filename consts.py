from main import *

#___________HERO_______________
HERO_HP = 6
#______________________________

#___________RAT________________
RAT_HP = 2
RAT_DAMAGE = 2
RAT_ARMOR = 0
#______________________________

#__________WEAPONS______________
DAGGER = Weapon(1, load_image('Sprites', 'Weapons', 'dagger.png'), 'dagger')
AXE = Weapon(3, load_image('Sprites', 'Weapons', 'axe.png'), 'axe')
#_______________________________

#_________ARMORS________________
LEATHER = Armor(1, load_image('Sprites', 'Armor', 'leather.png'), 'leather armor')
CHAIN = Armor(2, load_image('Sprites', 'Armor', 'chain.png'), 'chain armor')
#_______________________________

