#%%
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
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
pattern = re.compile(r'''<li><a href="[a-z\/A-Z._]{1,}" title="[a-zA-Z ]{1,}">[a-zA-Z ]{1,}<\/a>\n<ul><li>Value: [0-9]{1,}.<\/li>\n''', flags=re.MULTILINE)
map_objects_to_parse = pattern.findall(str(bs.contents[1]))

pattern_value = re.compile(r'''[0-9]{2,5}''', flags=re.MULTILINE)
pattern_name = re.compile(r'''>[a-zA-z ]{1,}<''', flags=re.MULTILINE)
for object in map_objects_to_parse:

    value = pattern_value.findall(object)[0]
    name = pattern_name.findall(object)[0][1:-1]
    map_objects.append(map_object(name,value))

# %%
