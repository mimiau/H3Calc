# %%
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sqlite3
from sqlite3.dbapi2 import IntegrityError
from collections import namedtuple
import itertools
# %%


class unit():

    def __init__(self, scrapped_info):
        cells = []
        for element in scrapped_info.find_all('td'):
            cells.append(element)
        self.name = cells[0].text.strip()
        self.type = cells[1].a['title']
        self.level = cells[2].text.strip()
        self.attack = cells[3].text.strip()
        self.defense = cells[4].text.strip()
        self.min_dmg = cells[5].text.strip()
        self.max_dmg = cells[6].text.strip()
        self.health = cells[7].text.strip()
        self.speed = cells[8].text.strip()
        self.growth = cells[9].text.strip()
        self.ai_value = cells[10].text.strip()

    def __str__(self):
        to_print = ""
        to_print += 'Name: ' + self.name + '\n'
        to_print += 'Type: ' + self.type + '\n'
        to_print += 'Level: ' + self.level + '\n'
        to_print += 'Attack: ' + self.attack + '\n'
        to_print += 'Defense: ' + self.defense + '\n'
        to_print += 'Min. Damage: ' + self.min_dmg + '\n'
        to_print += 'Max. Damage: ' + self.max_dmg + '\n'
        to_print += 'Health: ' + self.health + '\n'
        to_print += 'Speed: ' + self.speed + '\n'
        to_print += 'Growth: ' + self.growth + '\n'
        to_print += 'AI Value: ' + self.ai_value
        return to_print


class map_object():

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        to_print = ""
        to_print += 'Name: ' + self.name + '\n'
        to_print += 'Value: ' + self.value + '\n'
        return to_print

    def __repr__(self):
        to_print = ""
        to_print += 'Name: ' + self.name + '\n'
        to_print += 'Value: ' + self.value + '\n'
        return to_print


# %%
html = urlopen("https://heroes.thelazy.net/index.php/List_of_creatures_(HotA)")
bs = BeautifulSoup(html.read(), 'lxml')

# %%
units = []
for data in bs.tr.next_siblings:
    if data != '\n':
        units.append(unit(data))

# %%
html = urlopen("https://heroes.thelazy.net//index.php/Template_Editor")
bs = BeautifulSoup(html.read(), 'lxml')

map_objects = []
pattern = re.compile(
    r'''<li>[\w \d.\/_=\"';&%$#<>()]{1,}\n<ul><li>Value: [0-9]{1,}.</li>''',
    flags=re.MULTILINE)
map_objects_to_parse = pattern.findall(str(bs.contents[1]))

pattern_value = re.compile(r'''Value: [0-9]{3,}''', flags=re.MULTILINE)
pattern_name = re.compile(r'''>[a-zA-z0-9() \n']{1,}<''', flags=re.MULTILINE)
for object in map_objects_to_parse:

    value = pattern_value.findall(object)[0].split(' ')[-1]
    name = pattern_name.findall(object)[0][1:-1].strip()
    map_objects.append(map_object(name, value))

# %%
html = urlopen("https://heroes.thelazy.net/index.php/List_of_artifacts_(HotA)")
bs = BeautifulSoup(html.read(), 'lxml')

Artifact = namedtuple('Artifact', ['Name', 'Class'])
artifacts = []

for data in bs.tr.next_siblings:
    if data != '\n':
        art_name = data.find_all('td')[0].find_all('a')[1].text.strip()
        art_class = data.find_all('td')[2].text.strip()
        art = Artifact(art_name, art_class)
        artifacts.append(art)

# %%
html = urlopen(
    "https://heroes.thelazy.net/index.php/External_dwellings_table_(HotA)")
bs = BeautifulSoup(html.read(), 'lxml')

Dwelling = namedtuple(
    'Dwelling', [
        'Name', 'Creature', 'Level', 'Growth', 'Type'])
dwellings = []
for data in itertools.islice(bs.tr.next_siblings, 2, None):
    if data != '\n':
        type = data.contents[1].a['title']
        name = data.contents[3].text
        creature = data.contents[7].a.attrs['title']
        level = data.contents[9].text
        growth = data.contents[11].text[1:]
        dwelling = Dwelling(name, creature, level, growth, type)
        dwellings.append(dwelling)

# %%
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# %%
cursor.execute(
    '''CREATE TABLE objects (name VARCHAR(20) PRIMARY KEY, value INT)''')

cursor.execute('''CREATE TABLE units (
    name VARCHAR(20) PRIMARY KEY, type VARCHAR(20),
    level INT,
    Attack INT,
    Defense INT,
    minDamage INT,
    maxDamage INT,
    Health INT,
    Speed INT,
    Growth INT,
    Value INT)''')

cursor.execute(
    '''CREATE TABLE artifacts (
    name VARCHAR(20) PRIMARY KEY,
    class VARCHAR(20),
    Value INT)''')

cursor.execute(
    '''CREATE TABLE dwellings (
    name VARCHAR(20),
    creature VARCHAR(20),
    level INT,
    growth INT,
    type VARCHAR(20))''')
# %%
query = 'INSERT INTO objects VALUES (?,?)'
for object in map_objects:
    name = object.name
    value = int(object.value)
    try:
        cursor.execute(query, (name, value))
        print(object.name + " added")
    except IntegrityError:
        print(object.name + " already in database")
connection.commit()
# %%
query = 'INSERT INTO units VALUES (?,?,?,?,?,?,?,?,?,?,?)'
for unit in units:
    name = unit.name
    type = unit.type
    level = unit.level
    attack = unit.attack
    defense = unit.defense
    mindmg = unit.min_dmg
    maxdmg = unit.max_dmg
    health = unit.health
    speed = unit.speed
    growth = unit.growth
    value = unit.ai_value
    cursor.execute(
        query,
        (name,
         type,
         level,
         attack,
         defense,
         mindmg,
         maxdmg,
         health,
         speed,
         growth,
         value))
connection.commit()

# %%
query = 'INSERT INTO artifacts VALUES (?,?,?)'
values = {'Treasure': 2000, 'Minor': 5000, 'Major': 10000, 'Relic': 20000}

for art in artifacts:
    cursor.execute(query, (art.Name, art.Class, values[art.Class]))
connection.commit()

# %%
query = 'INSERT INTO dwellings VALUES (?,?,?,?,?)'

for dwelling in dwellings:
    try:
        cursor.execute(
            query,
            (dwelling.Name,
             dwelling.Creature,
             dwelling.Level,
             dwelling.Growth,
             dwelling.Type))
    except IntegrityError:
        print(dwelling)
connection.commit()
# %%
cursor.execute(
    '''SELECT name,value
         FROM objects
         WHERE name
         LIKE ? or name LIKE ? or name LIKE ?''', [
        'Pandora%', 'Spell%', 'Prison%'])
rows = cursor.fetchall()
print([name[0] for name in rows])
# %%
cursor.close()
connection.close()
