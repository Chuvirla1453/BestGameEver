from Classes.Secondary_functions import load_image, load_music
from Classes.Characters import Armor, Weapon

"""В этом файле лежат все константы, чтобы потом их можно было удобно менять"""

'''___________HERO_______________'''
HERO_HP = 100
HERO_SIGN = 'C'
HERO_SPRITE = load_image('Sprites', 'Animations', 'Hero', 'hero.png')  # +Characters
'''______________________________'''

''' ___________RAT________________'''
RAT_HP = 2
RAT_DAMAGE = 2
RAT_ARMOR = 0
RAT_SIGN = 'R'
RAT_SPRITE = load_image('Sprites', 'Animations', 'Rat', 'rat.png')
'''______________________________'''

'''__________WEAPONS______________'''
DAGGER = Weapon(1, load_image('Sprites', 'Weapons', 'dagger.png'), 'dagger')
AXE = Weapon(3, load_image('Sprites', 'Weapons', 'axe.png'), 'axe')
'''______________________________'''

'''_________ARMORS________________'''
LEATHER = Armor(1, load_image('Sprites', 'Armor', 'leather.png'), 'leather armor')
CHAIN = Armor(2, load_image('Sprites', 'Armor', 'chain.png'), 'chain armor')
'''______________________________'''

'''________TILES__________________'''
WALL_SIGN = '#'
WALL_SPRITES = [load_image('Sprites', 'Wall', '1.png'), load_image('Sprites', 'Wall', '2.png'),
                load_image('Sprites', 'Wall', '3.png'), load_image('Sprites', 'Wall', '4.png')]

FLOOR_SIGN = '_'
FLOOR_SPRITES = [load_image('Sprites', 'Floor', '1.png'), load_image('Sprites', 'Floor', '2.png'),
                 load_image('Sprites', 'Floor', '3.png'), load_image('Sprites', 'Floor', '4.png'),
                 load_image('Sprites', 'Floor', '5.png')]

STONE_SIGN = 's'
STONE_SPRITE = [load_image('Sprites', 'Stone', '1.png'), load_image('Sprites', 'Stone', '2.png'),
                load_image('Sprites', 'Stone', '3.png')]

NONE_SIGN = '.'
NONE_SPRITE = load_image('Sprites', 'none.png')

LADDER_SIGN = 'H'
LADDER_SPRITE = load_image('Sprites', 'Ladder', '1.png')
'''______________________________'''

'''________OTHER__________________'''
ENEMIES = ['rat']
'''______________________________'''


'''_____ELEMENTS_SIZE_____________'''
BASE_FONT = 'Times New Roman'
BASE_FONT_SIZE = 30

MENU_WIN_SIZE = (MENU_WIN_WIDTH, MENU_WIN_HEIGHT) = (600, 400)

MENU_WIN_BTN_SIZE = (MENU_WIN_BTN_WIDTH, MENU_WIN_BTN_HEIGHT) = (140, 70)
MENU_WIN_BTN_COLOR = (0, 255, 0)
MENU_WIN_BTN_BACK_COLOR = (0, 0, 0)

START_WIN_BTN_COUNT = 3

DEATH_MENU_BTN_COUNT = 1

TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT) = (64, 64)  # +Characters, Secondary_functions
'''______________________________'''

'''________MUSIC_________________'''
BREAK_STONE_SND = load_music('Sounds', 'break_stone.mp3')
WALK_SND = load_music('Sounds', 'walk.mp3')
GETTING_HIT_SND = load_music('Sounds', 'getting_hit.mp3')
HIT_SND = load_music('Sounds', 'hit.mp3')
WALK_IN_WALL_SND = load_music('Sounds', 'walk_in_wall.mp3')
LADDER_SND = load_music('Sounds', 'ladder.mp3')
PICK_SND = load_music('Sounds', 'pick.mp3')
GAZ = load_music('Sounds', 'Gaz.mp3')  # И ещё раз спасибо
# GAZ.play(-1)
'''______________________________'''
