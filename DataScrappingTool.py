#%%
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import sqlite3
from sqlite3.dbapi2 import IntegrityError
from collections import namedtuple
#%%
class unit():

    def __init__(self, scrapped_info):
        data = []
        for element in scrapped_info.find_all('td'):
            if element.text != '':
                data.append(element.text.strip())
        self.name = data[0]
        self.level = data[1]
        self.attack = data[2]
        self.defense = data[3]
        self.min_dmg = data[4]
        self.max_dmg = data[5]
        self.health = data[6]
        self.speed = data[7]
        self.growth = data[8]
        self.ai_value = data[9]
    
    def __str__(self):
        to_print = ""
        to_print += 'Name: ' + self.name + '\n'
        to_print += 'Level: ' + self.level + '\n'
        to_print += 'Attack: ' + self.attack + '\n'
        to_print += 'Defense: '+ self.defense + '\n'
        to_print += 'Min. Damage: '+self.min_dmg + '\n'
        to_print += 'Max. Damage: '+self.max_dmg + '\n'
        to_print += 'Health: ' + self.health + '\n'
        to_print += 'Speed: '+self.speed + '\n'
        to_print += 'Growth: ' + self.growth + '\n'
        to_print += 'AI Value: '+self.ai_value 
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

#%%
html = urlopen("https://heroes.thelazy.net/index.php/List_of_creatures_(HotA)")
bs = BeautifulSoup(html.read(), 'lxml')

# %%
units = []
for data in bs.tr.next_siblings:
    if data != '\n':
        units.append(unit(data))

# %%
html = urlopen("https://heroes.thelazy.net//index.php/Template_Editor")
bs = BeautifulSoup(html.read(),'lxml')

map_objects = []
pattern = re.compile(r'''<li>[\w \d.\/_=\"';&%$#<>()]{1,}\n<ul><li>Value: [0-9]{1,}.</li>''', flags=re.MULTILINE)
map_objects_to_parse = pattern.findall(str(bs.contents[1]))

pattern_value = re.compile(r'''Value: [0-9]{3,}''', flags=re.MULTILINE)
pattern_name = re.compile(r'''>[a-zA-z0-9() \n']{1,}<''', flags=re.MULTILINE)
for object in map_objects_to_parse:

    value = pattern_value.findall(object)[0].split(' ')[-1]
    name = pattern_name.findall(object)[0][1:-1].strip()
    map_objects.append(map_object(name,value))

# %%
html = urlopen("https://heroes.thelazy.net/index.php/List_of_artifacts_(HotA)")
bs = BeautifulSoup(html.read(),'lxml')

Artifact = namedtuple('Artifact',['Name','Class'])
artifacts = []
   
for data in bs.tr.next_siblings:
    if data != '\n':
        art_name = data.find_all('td')[0].find_all('a')[1].text.strip()
        art_class = data.find_all('td')[2].text.strip()
        art = Artifact(art_name,art_class)
        artifacts.append(art) 


#%%
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#%%
#cursor.execute('''CREATE TABLE objects (name VARCHAR(20) PRIMARY KEY, value INT)''')
#cursor.execute('''CREATE TABLE units (name VARCHAR(20) PRIMARY KEY, level INT, Attack INT, Defense INT, minDamage INT, maxDamage INT, Health INT, Speed INT, Growth INT, Value INT)''')

cursor.execute('''CREATE TABLE artifacts (name VARCHAR(20) PRIMARY KEY, class VARCHAR(20), Value INT)''')
# %%
query = 'INSERT INTO objects VALUES (?,?)'
for object in map_objects:
    name = object.name
    value = int(object.value)
    #print(object)
    try:
        cursor.execute(query,(name,value))
        print(object.name + " added")
    except IntegrityError:
        print(object.name + " already in database")
connection.commit()
#%%
query = 'INSERT INTO units VALUES (?,?,?,?,?,?,?,?,?,?)'
for unit in units:
    name = unit.name
    level = unit.level
    attack = unit.attack
    defense = unit.defense
    mindmg = unit.min_dmg
    maxdmg = unit.max_dmg
    health = unit.health
    speed = unit.speed
    growth = unit.growth
    value = unit.ai_value
    cursor.execute(query,(name,level,attack,defense,mindmg,maxdmg,health,speed,growth,value))
connection.commit()

#%%
query = 'INSERT INTO artifacts VALUES (?,?,?)'
values = {'Treasure':2000,'Minor':5000,'Major':10000,'Relic':20000}

for art in artifacts:
    cursor.execute(query,(art.Name,art.Class,values[art.Class]))
connection.commit()
#%%
cursor.execute('SELECT name from units')
rows = cursor.fetchall()
print([name[0] for name in rows])
# %%
cursor.close()
connection.close()

# %%
