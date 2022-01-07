from main import *
"""
В этом файле лежат все константы, чтобы потом их можно было удобно менять
"""
#___________HERO_______________
HERO_HP = 6
HERO_SPRITE = load_image('Sprites', 'Animations', 'Hero', 'hero.png')
#______________________________

#___________RAT________________
RAT_HP = 2
RAT_DAMAGE = 2
RAT_ARMOR = 0
RAT_SPRITE = load_image('Sprites', 'Animations', 'Rat', 'rat.png')
#______________________________

#__________WEAPONS______________
DAGGER = Weapon(1, load_image('Sprites', 'Weapons', 'dagger.png'), 'dagger')
AXE = Weapon(3, load_image('Sprites', 'Weapons', 'axe.png'), 'axe')
#_______________________________

#_________ARMORS________________
LEATHER = Armor(1, load_image('Sprites', 'Armor', 'leather.png'), 'leather armor')
CHAIN = Armor(2, load_image('Sprites', 'Armor', 'chain.png'), 'chain armor')
#_______________________________

#________OTHER__________________
ENEMIES = ['rat']
#_______________________________