try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from loaddata import load_name_data
from collections import defaultdict


def process_xml_file(file, dataloc):
    character = design_blank_character()

    xml = ET.parse(file)
    root = xml.getroot()
    tree = root[0]
    for node in tree:
        #load character info
        if node.tag == 'age' or node.tag == 'level' or node.tag == 'exp' or node.tag == 'expneeded':
            character['info'][node.tag] = int(node.text)
        elif node.tag == 'alignment' or node.tag == 'background' or node.tag == 'bonds' or node.tag == 'flaws' or \
        node.tag == 'height' or node.tag == 'ideals' or node.tag == 'weight' or node.tag == 'personalitytraits' or \
        node.tag == 'name' or node.tag == 'deity':
            character['info'][node.tag] = node.text
        elif node.tag == 'race':
            if '(' in node.text:
                temp = node.text.split('(')
                character['info']['race'] = temp[0].strip()
                character['info']['subrace'] = temp[1].strip(')')
            else:       #no subrace
                character['info']['race'] = node.text
        elif node.tag == 'classes':
            get_class_information(node, character)
        elif node.tag == 'abilities':
            populate_abilities(node, character)
        elif node.tag == 'coins':
            populate_monies(node, character['monies'])
        elif node.tag == 'defenses':
            populate_defense(node[0], character['defense'])
        elif node.tag == 'encumbrance':
            populate_limits(node, character)
        elif node.tag == 'featlist':
            populate_feats(node, character)
        elif node.tag == 'featurelist':
            populate_features(node, character['features'])
        elif node.tag == 'hp':
            character['health']['max_hp'] = int(get_listed_items(node, 'total'))
        elif node.tag == 'initiative':
            character['combat']['init'] = int(get_listed_items(node, 'total')) + character['combat']['init_mod']
        elif node.tag == 'inventorylist':
            populate_inventory(node, character)
        elif node.tag == 'languagelist':
            populate_languages(node, character['languages'])
        elif node.tag == 'powergroup':
            populate_spellpower(node, character['spells'])
        elif node.tag == 'powermeta':
            populate_spellslots(node, character['spells'])
        elif node.tag == 'powers':
            populate_spells(node, character['spells'])
        elif node.tag == 'profbonus':
            character['abilities']['prof'] = int(node.text)
        elif node.tag == 'proficiencylist':
            populate_proficiencies(node, character)
        elif node.tag == 'senses':
            character['features'].append(node.text)
        elif node.tag == 'skilllist':
            populate_skills(node, character['skills'])
        elif node.tag == 'speed':
            populate_speed(node, character)
        elif node.tag == 'traitlist':
            populate_traits(node, character['features'])

    character['info']['p_name'] = get_player_name(dataloc, character['info']['name'])
    populate_weapon_modifiers(character)
    populate_spell_info(character)
    return character


def populate_spell_info(char):
    stat = char['spells']['stat']
    mod = char['abilities'][stat+'mod']
    mod += char['abilities']['prof']
    char['spells']['atk'] = mod
    char['spells']['dc'] = 8 + mod


def populate_armor(tree, char):
    if get_listed_items(tree, 'subtype') == 'Shield':
        char['defense']['shield'] = get_listed_items(tree, 'name')
    else:
        char['defense']['armor'] = get_listed_items(tree, 'name')


def populate_weapon_modifiers(char):
    for _ in range(1, 7):
        ref = 'weapon' + str(_)
        if char['weapons'][ref]['name'] != '':
            if char['weapons'][ref]['range'] != '' or 'Finesse' in char['weapons'][ref]['prop']:
                modifier = char['abilities']['dexmod']
            else:
                modifier = char['abilities']['strmod']
            if modifier > 0:
                char['weapons'][ref]['dmg'] += '+' + str(modifier)
            char['weapons'][ref]['hit'] += modifier + char['abilities']['prof']


def populate_weapons(node, char):
    if char['weapons']['weapon1']['name'] == '':
        wpn = char['weapons']['weapon1']
    elif char['weapons']['weapon2']['name'] == '':
        wpn = char['weapons']['weapon2']
    elif char['weapons']['weapon3']['name'] == '':
        wpn = char['weapons']['weapon3']
    elif char['weapons']['weapon4']['name'] == '':
        wpn = char['weapons']['weapon4']
    elif char['weapons']['weapon5']['name'] == '':
        wpn = char['weapons']['weapon5']
    elif char['weapons']['weapon6']['name'] == '':
        wpn = char['weapons']['weapon6']
    if wpn is not None:
        for item in node:
            if item.tag == 'name':
                wpn['name'] = item.text
            elif item.tag == 'properties':
                if 'range' in item.text:
                    x = item.text.index('range')
                    wpn['range'] = item.text[x+5:].strip().strip(')')
                    wpn['prop'] = item.text[:x].strip().strip('(')
                elif 'Finesse' in item.text:
                    wpn['prop'] = item.text
            elif item.tag == 'bonus':
                wpn['hit'] += int(item.text)
            elif item.tag == 'damage':
                temp = item.text.split(' ')
                wpn['dmg'] = temp[0]
                wpn['type'] = temp[1][0].upper()


def populate_traits(tree, feat):
    for node in tree:             # id
        feat.append(get_listed_items(node, 'name'))


def populate_speed(tree, char):
    for node in tree:               # id
        if node.tag == 'base':
            char['combat']['speed'] = int(node.text)


def populate_skills(tree, skill):
    for node in tree:               # id
        for item in node:           # skill
            if item.tag == 'name':
                name = item.text.replace(' ', '').lower()
            elif item.tag == 'prof':
                prof = item.text
            elif item.tag == 'total':
                mod = int(item.text)
        skill[name]['mod'] = mod
        skill[name]['prof'] = True if prof == '1' else False
        if name == 'investigation' or name == 'perception':
            skill[name]['pass'] = 10 + mod


def populate_proficiencies(tree, char):
    for node in tree:               # id
        profs = node[0].text.split(':')
        char[profs[0].lower() + '_prof'] = [p.strip().title() for p in profs[1].split(',')]


def populate_spells(tree, spells):
    for node in tree:               # id
        name = get_listed_items(node, 'name')
        level = 'level' + get_listed_items(node, 'level')
        spells[level].append(name)


def populate_spellslots(tree, spells):
    for node in tree:
        if node.tag[-6:] == 'slots1':
            spells['l1'] += int(node[0].text)
        if node.tag[-6:] == 'slots2':
            spells['l2'] += int(node[0].text)
        if node.tag[-6:] == 'slots3':
            spells['l3'] += int(node[0].text)
        if node.tag[-6:] == 'slots4':
            spells['l4'] += int(node[0].text)
        if node.tag[-6:] == 'slots5':
            spells['l5'] += int(node[0].text)
        if node.tag[-6:] == 'slots6':
            spells['l6'] += int(node[0].text)
        if node.tag[-6:] == 'slots7':
            spells['l7'] += int(node[0].text)
        if node.tag[-6:] == 'slots8':
            spells['l8'] += int(node[0].text)
        if node.tag[-6:] == 'slots9':
            spells['l9'] += int(node[0].text)


def populate_spellpower(tree, spells):
    for node in tree:               #id
        power = get_listed_items(node, 'name')
        if power == 'Spells':
            spells['prep'] = int(get_listed_items(node, 'prepared'))
            spells['stat'] = get_listed_items(node, 'stat')[0:3]


def populate_languages(tree, langs):
    for node in tree:               #id
        for item in node:           #name
            langs.append(item.text)


def populate_inventory(tree, char):
    for node in tree:       #id
        qty = int(get_listed_items(node, 'count'))
        item = get_listed_items(node, 'name')
        type = get_listed_items(node, 'type')
        if item is not None:
            if qty > 1:
                char['inventory']['items'].append(str(qty) + ' ' + item)
            else:
                char['inventory']['items'].append(item)
        if type == 'Weapon':
            populate_weapons(node, char)
        elif type == 'Armor':
            populate_armor(node, char)


def populate_features(tree, feat):
    for node in tree:
        for item in node:
            if item.tag == 'name':
                feat.append(item.text)


def populate_feats(tree, char):
    for node in tree:
        name = ''
        desc = ''
        for feat in node:
            if feat.tag == 'name':
                name = feat.text
                if name == 'Alert':
                    char['combat']['init_mod'] += 5
            # elif feat.tag == 'text':
            #     for text in feat:
            #         if text.tag == 'p':
            #             desc = text.text
            #         elif text.tag == 'list':
            #             for list in text:
            #                 desc += '\n  ' + list.text
        char['features'].append(name)


def populate_limits(tree, char):
    for node in tree:
        if node.tag == 'max':
            char['limits']['carry_max'] = int(node.text)
        elif node.tag == 'liftpushdrag':
            char['limits']['lift_max'] = int(node.text)
        elif node.tag == 'load':
            char['inventory']['tot_weight'] = float(node.text)


def populate_defense(tree, char):
    for node in tree:
        if node.tag == 'total':
            char['ac'] = int(node.text)
        elif node.tag == 'shield':
            if node.text != '0':
                char['use_shield'] = True
        elif node.tag == 'disstealth':
            if node.text == '1':
                char['stealth_dis'] = True


def populate_monies(coins, money):
    for slot in coins:
        for node in slot:
            if node.tag == 'name':
                coin = node.text
            else:
                amt = int(node.text)
        if coin != '':
            money[coin] = amt
            coin = '';


def populate_abilities(tree, char):
    for ability in tree:
        score = ability.tag[0:3]
        mod = score + 'mod'
        save = score + '_save'
        for node in ability:
            if node.tag == 'score':
                char['abilities'][score] = int(node.text)
            elif node.tag == 'bonus':
                char['abilities'][mod] = int(node.text)
            elif node.tag == 'save':
                char['defense'][save]['mod'] = int(node.text)
            elif node.tag == 'saveprof':
                if node.text == '1':
                    char['defense'][save]['prof'] = True


def get_player_name(loc, name):
    players = load_name_data(loc)
    for c, p in players:
        if name.lower() == c:
            return p
    return 'NPC'


def get_abbreviated_classes(classlist):
    class_ = []
    spell_class = []
    for c in classlist:
        if c == 'Barbarian':
            class_.append('Barb')
        elif c == 'Cleric':
            class_.append('Clrc')
            spell_class.append('Clrc')
        elif c == 'Druid':
            class_.append('Drd')
            spell_class.append('Drd')
        elif c == 'Fighter':
            class_.append('Ftr')
        elif c == 'Paladin':
            class_.append('Pal')
            spell_class.append('Pal')
        elif c == 'Ranger':
            class_.append('Rng')
            spell_class.append('Rng')
        elif c == 'Rogue':
            class_.append('Rog')
        elif c == 'Sorcerer':
            class_.append('Sorc')
            spell_class.append('Sorc')
        elif c == 'Warlock':
            class_.append('Wrlk')
            spell_class.append('Wrlk')
        elif c == 'Wizard':
            class_.append('Wiz')
            spell_class.append('Wiz')
        else:
            class_.append(c)
            if c == 'Bard':
                spell_class.append('Bard')
    return '/'.join(class_)


def get_class_information(tree, char):
    #class info affects info and health (hit die)
    dtype = ''
    hdnum = 0
    classes = []
    for branch in tree:         #should take us to id# in classes
        for node in branch:     #should take us to the individual class detail
            if node.tag == 'hddie':
                dtype = node.text
            elif node.tag == 'level':
                hdnum = int(node.text)
            elif node.tag == 'name':
                classes.append(node.text)
        char['health'][dtype] += hdnum
        if len(classes) > 1:
            char['info']['class'] = get_abbreviated_classes(classes)
        else:
            char['info']['class'] = classes[0]
            char['spells']['class'] = classes[0]


def get_listed_items(tree, item):
    for node in tree:
        if node.tag == item:
            return node.text


def design_blank_character():
    c = defaultdict(dict)
    # build character info section
    c['info'] = {'name': '', 'p_name': '', 'race': '', 'class': '', 'background': '', 'subrace': '', 'alignment': '',
                 'weight': '', 'height': '', 'age': 0, 'level': 0, 'exp': 0, 'expneeded': 0, 'personalitytraits': '',
                 'ideals': '', 'bonds': '', 'flaws': '', 'eyes': '', 'skin': '', 'hair': '', 'deity': '',
                 'backstory': '', 'allies': ''}
    c['abilities'] = {'str': 0, 'dex': 0, 'con': 0, 'int': 0, 'wis': 0, 'cha': 0, 'prof': 0, 'strmod': 0, 'dexmod': 0,
                      'conmod': 0, 'intmod': 0, 'wismod': 0, 'chamod': 0}
    c['skills'] = {'acrobatics': {'mod': 0, 'prof': False}, 'animalhandling': {'mod': 0, 'prof': False},
                   'arcana': {'mod': 0, 'prof': False}, 'athletics': {'mod': 0, 'prof': False},
                   'deception': {'mod': 0, 'prof': False}, 'history': {'mod': 0, 'prof': False},
                   'insight': {'mod': 0, 'prof': False}, 'intimidation': {'mod': 0, 'prof': False},
                   'investigation': {'mod': 0, 'prof': False, 'pass': 10}, 'medicine': {'mod': 0, 'prof': False},
                   'nature': {'mod': 0, 'prof': False}, 'perception': {'mod': 0, 'prof': False, 'pass': 10},
                   'performance': {'mod': 0, 'prof': False}, 'persuasion': {'mod': 0, 'prof': False},
                   'religion': {'mod': 0, 'prof': False}, 'sleightofhand': {'mod': 0, 'prof': False},
                   'stealth': {'mod': 0, 'prof': False}, 'survival': {'mod': 0, 'prof': False}}
    c['limits'] = {'hold_breath': 0, 'suffocate': 0, 'starve': 0, 'carry_max': 0, 'lift_max': 0, 'high_jump': 0,
                   'long_jump': 0, 'crawl_swim': 0, 'daily_travel': 0}
    c['health'] = {'max_hp': 0, 'd6': 0, 'd8': 0, 'd10': 0, 'd12': 0, 'condition1': '', 'condition2': '',
                   'condition3': ''}
    c['defense'] = {'ac': 0, 'use_shield': False, 'stealth_dis': False, 'armor': '', 'shield': '',
                    'str_save': {'mod': 0, 'prof': False}, 'dex_save': {'mod': 0, 'prof': False},
                    'con_save': {'mod': 0, 'prof': False}, 'int_save': {'mod': 0, 'prof': False},
                    'wis_save': {'mod': 0, 'prof': False}, 'cha_save': {'mod': 0, 'prof': False},
                    'resistance1': '', 'resistance2': '', 'resistance3': ''}
    c['combat'] = {'init': 0, 'speed': 0, 'num_atks': 0, 'init_mod': 0}
    c['class_features'] = {'feature1': {'name': '', 'uses': 0, 'rest': ''},
                           'feature2': {'name': '', 'uses': 0, 'rest': ''},
                           'feature3': {'name': '', 'uses': 0, 'rest': ''},
                           'feature4': {'name': '', 'uses': 0, 'rest': ''},
                           'feature5': {'name': '', 'uses': 0, 'rest': ''},
                           'feature6': {'name': '', 'uses': 0, 'rest': ''}}
    c['weapons'] = {'weapon1': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''},
                    'weapon2': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''},
                    'weapon3': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''},
                    'weapon4': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''},
                    'weapon5': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''},
                    'weapon6': {'name': '', 'hit': 0, 'dmg': '', 'type': '', 'range': '', 'prop': ''}}
    c['features'] = []
    c['inventory'] = {'tot_weight': 0, 'items': []}
    c['monies'] = {'PP': 0, 'GP': 0, 'EP': 0, 'SP': 0, 'CP': 0}
    c['armor_prof'] = []
    c['weapon_prof'] = []
    c['tool_prof'] = []
    c['languages'] = []
    c['spells'] = {'cantrips': [], 'level1': [], 'level2': [], 'level3': [], 'level4': [], 'level5': [], 'level6': [],
                   'level7': [], 'level8': [], 'level9': [], 'atk': 0, 'dc': 0, 'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0,
                   'l4': 0, 'l5': 0, 'l6': 0, 'l7': 0, 'l8': 0, 'l9': 0, 'stat': '', 'prep': 0, 'class': ''}
    return c


if __name__ == '__main__':
    process_xml_file()
