# %%
import xml.etree.ElementTree as ET 

# %%
dir = '../../data/special/country_data.xml'
tree = ET.parse(dir)
print(tree)
root = tree.getroot()
print(root)
# %%
# root = ET.fromstring(country='Panama')
# %%
root.tag
# %%
root.attrib
# %%
for child in root:
    print(child.tag, child.attrib)
# %%
root[0][1].text
# %%
parser = ET.XMLPullParser(['start', 'end'])
parser.feed('<mytag>sometext')
# list(parser.read_events())
for event, elem in parser.read_events():
    print(event)
    print(elem.tag, 'text=', elem.text)
# %%
for neighbor in root.iter('neighbor'):
    print(neighbor['name'].attrib)
# %% Read
for country in root.findall('country'):
    rank = country.find('rank').text
    name = country.get('name')
    print(name, rank)
# %% Modify 
for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'yes')
# %% write
tree.write('output.xml')
# %% Remove
for country in root.findall('country'):
    # using root.findall() to avoid removal during traversal
    rank = int(country.find('rank').text)
    if rank > 50:
        root.remove(country)

# %% Build
a = ET.Element('a')
b = ET.SubElement(a, 'b')
c = ET.SubElement(a, 'c')
d = ET.SubElement(c, 'd')
ET.dump(a)
# %% Parsing XML with namespaces
    # form prefix:sometag
    # {uri}sometag

#%%
xmltext = \
'''<?xml version="1.0"?>
<actors xmlns:fictional="http://characters.example.com"
        xmlns="http://people.example.com">
    <actor>
        <name>John Cleese</name>
        <fictional:character>Lancelot</fictional:character>
        <fictional:character>Archie Leach</fictional:character>
    </actor>
    <actor>
        <name>Eric Idle</name>
        <fictional:character>Sir Robin</fictional:character>
        <fictional:character>Gunther</fictional:character>
        <fictional:character>Commander Clement</fictional:character>
    </actor>
</actors>'''
# %%
root = fromstring(xmltext)
for actor in root.findall('{http://people.example.com}actor'):
    name = actor.find('{http://people.example.com}name')
    print(name.text)
    for char in actor.findall('{http://characters.example.com}character'):
        print(' |-->', char.text)
# %%
