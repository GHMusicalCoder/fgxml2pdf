try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from loaddata import load_name_data
from collections import defaultdict


def process_xml_file(file):
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
        node.tag == 'name':
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

    character['info']['p_name'] = get_player_name('charname.txt', character['info']['name'])
    #test
    print(character['info'])
    print(character['abilities'])
    print(character['monies'])
    print(character['defense'])
    print(character['skills'])
    print(character['limits'])
    print(character['health'])
    print(character['combat'])
    print(character['class_features'])
    print(character['weapons'])
    print(character['features'])
    print(character['inventory'])
    print(character['monies'])
    print(character['armor_prof'])
    print(character['wpn_prof'])
    print(character['tool_prof'])
    print(character['languages'])
    print(character['spells'])


def populate_feats(tree, char):
    for node in tree:
        name = ''
        desc = ''
        for feat in node:
            if feat.tag == 'name':
                name = feat.text
                if name == 'Alert':
                    char['combat']['init_mod'] += 5
            elif feat.tag == 'text':
                for text in feat:
                    if text.tag == 'p':
                        desc = text.text
                    elif text.tag == 'list':
                        for list in text:
                            desc += '\n  ' + list.text
        char['features'].append(name + ' : ' + desc)


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


def get_player_name(file, name):
    players = load_name_data(file)
    for c, p in players:
        if name.lower() == c:
            return p
    return 'NPC'


def get_abbreviated_classes(classlist):
    class_ = []
    for c in classlist:
        if c == 'Barbarian':
            class_.append('Barb')
        elif c == 'Cleric':
            class_.append('Clrc')
        elif c == 'Druid':
            class_.append('Drd')
        elif c == 'Fighter':
            class_.append('Ftr')
        elif c == 'Paladin':
            class_.append('Pal')
        elif c == 'Ranger':
            class_.append('Rng')
        elif c == 'Rogue':
            class_.append('Rog')
        elif c == 'Sorcerer':
            class_.append('Sorc')
        elif c == 'Warlock':
            class_.append('Wrlk')
        elif c == 'Wizard':
            class_.append('Wiz')
        else:
            class_.append(c)
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


def list_weapon(func_data, idx, name, atk, dmg):
    weapons = ['Wpn Name', 'Wpn Name 2', 'Wpn Name 3']
    atk_bonus = ['Wpn1 AtkBonus', 'Wpn2 AtkBonus', 'Wpn3 AtkBonus']
    dmg_bonus = ['Wpn1 Damage', 'Wpn2 Damage', 'Wpn3 Damage']
    func_data.append((weapons[idx], name))
    func_data.append((atk_bonus[idx], atk))
    func_data.append((dmg_bonus[idx], dmg))


def wpn_str_dex(data, adjs):
    if 'range' in data or 'Finesse' in data:
        return adjs[2]
    else:
        return adjs[1]


def proc_weapons(children, func_data, wpns, adjustments):
    c = 0
    wname, wattack, wdamage = '', '', ''

    for child in children:
        for kid in child:
            if kid.tag == 'attackbonus':
                atk_mod = int(kid.text)
            elif kid.tag == 'damagelist':
                for entry in kid:
                    dmg_mod = int(get_listed_items(entry, 'bonus'))
                    dmg_type = get_listed_items(entry, 'type')
            elif kid.tag == 'name':
                wname = kid.text
        for w in wpns:
            if w[0] == wname:
                wpn_data = w[2]
                dmg_die = w[1]

        atk_mod += adjustments[0] + wpn_str_dex(wpn_data, adjustments)
        dmg_mod += wpn_str_dex(wpn_data, adjustments)

        if dmg_mod > 0:
            temp = dmg_die.split(' ')

            # if dmg[0] == 'd':
            #     damage = '1' + dmg
            # else:
            #     damage = dmg
            # if dmod != '0':
            #     damage += '+' + dmod
            # damage += ' ' + dtype
            # if c == 1:
            #     func_data.append(('Wpn Name', wpn))
            #     func_data.append(('Wpn1 AtkBonus', '+' + str(atk)))
            #     func_data.append(('Wpn1 Damage', damage))


def proc_skills(children, func_data):
    for child in children:
        name = get_listed_items(child, 'name')
        prof = get_listed_items(child, 'prof')
        adj = get_listed_items(child, 'total')
        set_skill(func_data, name, prof, adj)


def set_skill(fdata, skill, isprof, mod):
    if skill == 'Acrobatics':
        fdata.append(('Acrobatics', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 23', 'Yes'))
    if skill == 'Animal Handling':
        fdata.append(('Animal', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 24', 'Yes'))
    if skill == 'Arcana':
        fdata.append(('Arcana', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 25', 'Yes'))
    if skill == 'Athletics':
        fdata.append(('Athletics', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 26', 'Yes'))
    if skill == 'Deception':
        fdata.append(('Deception ', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 27', 'Yes'))
    if skill == 'History':
        fdata.append(('History ', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 28', 'Yes'))
    if skill == 'Insight':
        fdata.append(('Insight', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 29', 'Yes'))
    if skill == 'Intimidation':
        fdata.append(('Intimidation', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 30', 'Yes'))
    if skill == 'Investigation':
        fdata.append(('Investigation ', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 31', 'Yes'))
    if skill == 'Medicine':
        fdata.append(('Medicine', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 32', 'Yes'))
    if skill == 'Nature':
        fdata.append(('Nature', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 33', 'Yes'))
    if skill == 'Perception':
        fdata.append(('Perception ', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 34', 'Yes'))
    if skill == 'Performance':
        fdata.append(('Performance', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 35', 'Yes'))
    if skill == 'Persuasion':
        fdata.append(('Persuasion', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 36', 'Yes'))
    if skill == 'Religion':
        fdata.append(('Religion', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 37', 'Yes'))
    if skill == 'Sleight of Hand':
        fdata.append(('SleightofHand', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 38', 'Yes'))
    if skill == 'Stealth':
        fdata.append(('Stealth ', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 39', 'Yes'))
    if skill == 'Survival':
        fdata.append(('Survival', '+' + mod))
        if isprof == '1':
            fdata.append(('Check Box 25', 'Yes'))


def proc_languages_proficiencies(children):
    line = ''
    for child in children:
        line += get_listed_items(child, 'name') + '\n'
    return line + '\n'


def proc_inventory(children, func_data, weapons):
    inv = []
    for child in children:
        qty = ''
        wpn = False
        for kid in child:
            if kid.tag == 'count':
                if int(kid.text) > 1:
                    qty = kid.text
            elif kid.tag == 'damage':
                dmg = kid.text
            elif kid.tag == 'name':
                item = kid.text
            elif kid.tag == 'properties':
                prop = kid.text
            elif kid.tag == 'type' and kid.text == 'Weapon':
                wpn = True
        if qty != '':
            inv.append(qty + ' ' + item)
        else:
            inv.append(item)
        if wpn:
            weapons.append([item, dmg, prop])

    # inv is our list of inventory
    inv.sort()
    l = []
    line = inv[0] if len(inv) > 0 else ""
    for i in range(1, len(inv)):
        if (len(line) + len(inv[i]) + 3) < 26:
            line += ' / ' + inv[i]
        else:
            l.append(line)
            line = inv[i]
    func_data.append(('Equipment', '\n'.join(l)))


def get_listed_items(children, name):
    for child in children:
        if child.tag == name:
            return child.text


def proc_features(children, feat):
    for child in children:
        for kid in child:
            if kid.tag == 'name':
                feat.append(kid.text)
    feat[-1] = feat[-1] + '\n'


def design_blank_character():
    c = defaultdict(dict)
    # build character info section
    c['info'] = {'name': '', 'p_name': '', 'race': '', 'class': '', 'background': '', 'subrace': '', 'alignment': '',
                 'weight': '', 'height': '', 'age': 0, 'level': 0, 'exp': 0, 'expneeded': 0, 'personalitytraits': '',
                 'ideals': '', 'bonds': '', 'flaws': ''}
    c['abilities'] = {'str': 0, 'dex': 0, 'con': 0, 'int': 0, 'wis': 0, 'cha': 0, 'prof': 0, 'strmod': 0, 'dexmod': 0,
                      'conmod': 0, 'intmod': 0, 'wismod': 0, 'charmod': 0}
    c['skills'] = {'acrobatics': {'mod': 0, 'prof': False}, 'animalhandling': {'mod': 0, 'prof': False},
                   'arcana': {'mod': 0, 'prof': False}, 'athletics': {'mod': 0, 'prof': False},
                   'deception': {'mod': 0, 'prof': False}, 'history': {'mod': 0, 'prof': False},
                   'insight': {'mod': 0, 'prof': False}, 'intimidation': {'mod': 0, 'prof': False},
                   'investigation': {'mod': 0, 'prof': False}, 'medicine': {'mod': 0, 'prof': False},
                   'nature': {'mod': 0, 'prof': False}, 'perception': {'mod': 0, 'prof': False},
                   'performance': {'mod': 0, 'prof': False}, 'persuasion': {'mod': 0, 'prof': False},
                   'religion': {'mod': 0, 'prof': False}, 'sleightofhand': {'mod': 0, 'prof': False},
                   'stealth': {'mod': 0, 'prof': False}, 'survival': {'mod': 0, 'prof': False}}
    c['limits'] = {'hold_breath': 0, 'suffocate': 0, 'starve': 0, 'carry_max': 0, 'lift_max': 0, 'high_jump': 0,
                   'long_jump': 0, 'crawl_swim': 0, 'daily_travel': 0}
    c['health'] = {'max_hp': 0, 'd6': 0, 'd8': 0, 'd10': 0, 'd12': 0, 'condition1': '', 'condition2': '',
                   'condition3': ''}
    c['defense'] = {'ac': 0, 'use_shield': False, 'stealth_dis': False, 'str_save': {'mod': 0, 'prof': False},
                    'dex_save': {'mod': 0, 'prof': False}, 'con_save': {'mod': 0, 'prof': False},
                    'int_save': {'mod': 0, 'prof': False}, 'wis_save': {'mod': 0, 'prof': False},
                    'cha_save': {'mod': 0, 'prof': False}, 'resistance1': '', 'resistance2': '', 'resistance3': ''}
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
    c['wpn_prof'] = []
    c['tool_prof'] = []
    c['languages'] = []
    c['spells'] = {'cantrips': [], 'level1': [], 'level2': [], 'level3': [], 'level4': [], 'level5': [], 'level6': [],
                   'level7': [], 'level8': [], 'level9': [], 'atk': 0, 'dc': 0, 'l0': 0, 'l1': 0, 'l2': 0, 'l3': 0,
                   'l4': 0, 'l5': 0, 'l6': 0, 'l7': 0, 'l8': 0, 'l9': 0}
    return c


if __name__ == '__main__':
    pull_xml()
