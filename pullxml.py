try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import loaddata
import xmlfuncs


def pull_xml(file):
    players = []
    data = []
    score_mods = [0, 0, 0, 0, 0, 0, 0]
    features = []
    lang_prof = ''
    weapons = []
    loaddata.load_name_data('charname.txt', players)
    xml = ET.parse(file)
    root = xml.getroot()
    tree = root[0]
    for children in tree:
        # print(children.tag, children.attrib)
        if children.tag == 'abilities':
            proc_abilities(children, data, score_mods)
        elif children.tag == 'appearance':
            items = [i.strip() for i in children.text.split('*')]
            for item in items:
                it = [i.strip() for i in item.split(':')]
                if it[0] == 'Hair':
                    data.append(('Hair', it[1]))
                elif it[0] == 'Eyes':
                    data.append(('Eyes', it[1]))
                elif it[0] == 'Skin':
                    data.append(('Skin', it[1]))
        elif children.tag == 'classes':
            proc_classes(children, data)
        elif children.tag == 'coins':
            proc_coins(children, data)
        elif children.tag == 'defenses':
            data.append(('AC', get_listed_items(children[0], 'total')))
        elif children.tag == 'featurelist':
            proc_features(children, features)
        elif children.tag == 'hp':
            data.append(('HPMax', get_listed_items(children, 'total')))
        elif children.tag == 'initiative':
            data.append(('Initiative', '+' + get_listed_items(children, 'total')))
        elif children.tag == 'inventorylist':
            proc_inventory(children, data, weapons)
        elif children.tag == 'languagelist':
            lang_prof += proc_languages_proficiencies(children)
        elif children.tag == 'name':
            data.append(('CharacterName', children.text))
            data.append(('CharacterName 2', children.text))
            data.append(('PlayerName', proc_playername(players, children.text)))
        elif children.tag == 'profbonus':
            data.append(('ProfBonus', '+' + children.text))
            score_mods[0] = int(children.text)
        elif children.tag == 'proficiencylist':
            lang_prof += proc_languages_proficiencies(children)
        elif children.tag == 'senses':
            features.append(children.text + '\n')
        elif children.tag == 'skilllist':
            proc_skills(children, data)
        elif children.tag == 'traitlist':
            proc_features(children, features)
        elif children.tag == 'weaponlist':
            proc_weapons(children, data, weapons, score_mods)
        else:
            xmlfuncs.process_normal_node(children.tag, children.text, data)

    data.append(('Features and Traits', '\n'.join(features)))
    data.append(('ProficienciesLang', lang_prof))
    print(*weapons)
    return list(data)


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


def proc_abilities(children, func_data, scores):
    for child in children:
        if child.tag == 'charisma':
            scores[6] = int(child[0].text)
            func_data.append(('CHA', child[4].text))
            func_data.append(('CHamod', '+' + child[0].text))
            func_data.append(('ST Charisma', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 22', 'Yes'))
        elif child.tag == 'constitution':
            scores[3] = int(child[0].text)
            func_data.append(('CON', child[4].text))
            func_data.append(('CONmod', '+' + child[0].text))
            func_data.append(('ST Constitution', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 19', 'Yes'))
        elif child.tag == 'dexterity':
            scores[2] = int(child[0].text)
            func_data.append(('DEX', child[4].text))
            func_data.append(('DEXmod ', '+' + child[0].text))
            func_data.append(('ST Dexterity', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 18', 'Yes'))
        elif child.tag == 'intelligence':
            scores[4] = int(child[0].text)
            func_data.append(('INT', child[4].text))
            func_data.append(('INTmod', '+' + child[0].text))
            func_data.append(('ST Intelligence', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 20', 'Yes'))
        elif child.tag == 'strength':
            scores[1] = int(child[0].text)
            func_data.append(('STR', child[4].text))
            func_data.append(('STRmod', '+' + child[0].text))
            func_data.append(('ST Strength', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 11', 'Yes'))
        elif child.tag == 'wisdom':
            scores[5] = int(child[0].text)
            func_data.append(('WIS', child[4].text))
            func_data.append(('WISmod', '+' + child[0].text))
            func_data.append(('ST Wisdom', '+' + child[1].text))
            if child[3].text == '1':
                func_data.append(('Check Box 21', 'Yes'))


def proc_classes(children, func_data):
    if len(children) > 1:
        print('Error: cannot handle multiclassing right now')
        exit()
    else:
        level = get_listed_items(children[0], 'level')
        class_level = get_listed_items(children[0], 'name')
        class_level += " " + level
        hdtot = level + get_listed_items(children[0], 'hddie')
        func_data.append(('ClassLevel', class_level))
        func_data.append(('HDTotal', hdtot))


def proc_coins(children, func_data):
    coins = [0, 0, 0, 0, 0]
    for child in children:
        proc_coin_name(child, coins)
    func_data.append(('CP', str(coins[0])))
    func_data.append(('SP', str(coins[1])))
    func_data.append(('EP', str(coins[2])))
    func_data.append(('GP', str(coins[3])))
    func_data.append(('PP', str(coins[4])))


def proc_coin_name(child, coins):
    if len(child) > 1:
        name = child[1].text
        if name == 'Copper' or name == 'CP':
            coins[0] = int(child[0].text)
        if name == 'Silver' or name == 'SP':
            coins[1] = int(child[0].text)
        if name == 'Electrum' or name == 'EP':
            coins[2] = int(child[0].text)
        if name == 'Gold' or name == 'GP':
            coins[3] = int(child[0].text)
        if name == 'Platinum' or name == 'PP':
            coins[4] = int(child[0].text)


def proc_features(children, feat):
    for child in children:
        for kid in child:
            if kid.tag == 'name':
                feat.append(kid.text)
    feat[-1] = feat[-1] + '\n'


def proc_playername(players, char):
    for c, p in players:
        if char.lower() == c:
            return p


if __name__ == '__main__':
    pull_xml()