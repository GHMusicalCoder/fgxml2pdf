from fdfgen import forge_fdf


def build_fdf(fields, filename):
    if fields != [] and filename != 'none':
        fdf = forge_fdf("", fields, [], [], [])
        fdf_file = open(filename, "wb")
        fdf_file.write(fdf)
        fdf_file.close()
    else:
        print("error in buildfdf - fields were empty and filename was none")


def build_perkins_fieldset(char):
    data = []
    # section 1 - character name and info
    data.append(('CHARACTER NAME', char['info']['name']))
    data.append(('PLAYER NAME', char['info']['p_name']))
    data.append(('CLASS', char['info']['class']))
    data.append(('BACKGROUND', char['info']['background']))
    data.append(('RACE', char['info']['race']))
    data.append(('SUBRACE', char['info']['subrace']))
    data.append(('ALIGNMENT', char['info']['alignment']))
    data.append(('WEIGHT', char['info']['weight']))
    data.append(('HEIGHT', char['info']['height']))
    data.append(('AGE', char['info']['age']))
    data.append(('LEVEL', char['info']['level']))
    data.append(('CURRENT EXP', char['info']['exp']))
    data.append(('EXP FOR NEXT LEVEL', char['info']['expneeded']))
    data.append(('Personality Traits', '\n'.join(char['info']['personalitytraits'])))
    data.append(('Ideals', char['info']['ideals']))
    data.append(('Bonds', char['info']['bonds']))
    data.append(('Flaws', char['info']['flaws']))

    # section 2 - ability scores
    data.append(('STR MOD', '+' + str(char['abilities']['strmod'])))
    data.append(('DEX MOD', '+' + str(char['abilities']['dexmod'])))
    data.append(('CON MOD', '+' + str(char['abilities']['conmod'])))
    data.append(('INT MOD', '+' + str(char['abilities']['intmod'])))
    data.append(('WIS MOD', '+' + str(char['abilities']['wismod'])))
    data.append(('CHA MOD', '+' + str(char['abilities']['chamod'])))
    data.append(('STR SCORE', str(char['abilities']['str'])))
    data.append(('DEX SCORE', str(char['abilities']['dex'])))
    data.append(('CON SCORE', str(char['abilities']['con'])))
    data.append(('INT SCORE', str(char['abilities']['int'])))
    data.append(('WIS SCORE', str(char['abilities']['wis'])))
    data.append(('CHA SCORE', str(char['abilities']['cha'])))
    data.append(('Proficiency Bonus', '+' + str(char['abilities']['prof'])))

    # section 3 - health
    data.append(('Max HP', str(char['health']['max_hp'])))
    if char['health']['d6'] > 0:
        data.append(('Max HD 1', str(char['health']['d6'])))
    if char['health']['d8'] > 0:
        data.append(('Max HD 2', str(char['health']['d8'])))
    if char['health']['d10'] > 0:
        data.append(('Max HD 3', str(char['health']['d10'])))
    if char['health']['d12'] > 0:
        data.append(('Max HD 4', str(char['health']['d12'])))
    if char['health']['condition1'] != '':
        data.append(('Conditions 1', char['health']['condition1']))
    if char['health']['condition2'] != '':
        data.append(('Conditions 2', char['health']['condition2']))
    if char['health']['condition3'] != '':
        data.append(('Conditions 3', char['health']['condition3']))

    # section 4 - defense
    data.append(('Armour Class', str(char['defense']['ac'])))
    if char['defense']['use_shield']:
        data.append(('95', 'Yes'))
    if char['defense']['stealth_dis']:
        data.append(('96', 'Yes'))
    if char['defense']['armor'] != '':
        data.append(('Armour Type', char['defense']['armor']))
    data.append(('STR Save', '+' + str(char['defense']['str_save']['mod'])))
    if char['defense']['str_save']['prof']:
        data.append(('37', 'Yes'))
    data.append(('DEX Save', '+' + str(char['defense']['dex_save']['mod'])))
    if char['defense']['dex_save']['prof']:
        data.append(('38', 'Yes'))
    data.append(('CON Save', '+' + str(char['defense']['con_save']['mod'])))
    if char['defense']['con_save']['prof']:
        data.append(('39', 'Yes'))
    data.append(('INT Save', '+' + str(char['defense']['int_save']['mod'])))
    if char['defense']['int_save']['prof']:
        data.append(('41', 'Yes'))
    data.append(('WIS Save', '+' + str(char['defense']['wis_save']['mod'])))
    if char['defense']['wis_save']['prof']:
        data.append(('40', 'Yes'))
    data.append(('CHA Save', '+' + str(char['defense']['cha_save']['mod'])))
    if char['defense']['cha_save']['prof']:
        data.append(('42', 'Yes'))
    if char['defense']['resistance1'] != '':
        data.append(('Resist 1', char['defense']['resistance1']))
    if char['defense']['resistance2'] != '':
        data.append(('Resist 2', char['defense']['resistance2']))
    if char['defense']['resistance3'] != '':
        data.append(('Resist 3', char['defense']['resistance3']))

    # section 5 - combat
    data.append(('Initiative Bonus', '+' + str(char['combat']['init'])))
    data.append(('Speed', str(char['combat']['speed']) + ' ft.'))

    # section 6 - class resources
    if char['class_features']['feature1']['name'] != '':
        data.append(('Class Name 1', char['class_features']['feature1']['name']))
        data.append(('Class Max 1', str(char['class_features']['feature1']['uses'])))
        if char['class_features']['feature1']['rest'] == 'long':
            data.append(('43', 'Yes'))
        elif char['class_features']['feature1']['rest'] == 'short':
            data.append(('44', 'Yes'))
    if char['class_features']['feature2']['name'] != '':
        data.append(('Class Name 2', char['class_features']['feature2']['name']))
        data.append(('Class Max 2', str(char['class_features']['feature2']['uses'])))
        if char['class_features']['feature2']['rest'] == 'long':
            data.append(('45', 'Yes'))
        elif char['class_features']['feature2']['rest'] == 'short':
            data.append(('46', 'Yes'))
    if char['class_features']['feature3']['name'] != '':
        data.append(('Class Name 3', char['class_features']['feature3']['name']))
        data.append(('Class Max 3', str(char['class_features']['feature3']['uses'])))
        if char['class_features']['feature3']['rest'] == 'long':
            data.append(('47', 'Yes'))
        elif char['class_features']['feature3']['rest'] == 'short':
            data.append(('48', 'Yes'))
    if char['class_features']['feature4']['name'] != '':
        data.append(('Class Name 4', char['class_features']['feature4']['name']))
        data.append(('Class Max 4', str(char['class_features']['feature4']['uses'])))
        if char['class_features']['feature4']['rest'] == 'long':
            data.append(('49', 'Yes'))
        elif char['class_features']['feature4']['rest'] == 'short':
            data.append(('50', 'Yes'))
    if char['class_features']['feature5']['name'] != '':
        data.append(('Class Name 5', char['class_features']['feature5']['name']))
        data.append(('Class Max 5', str(char['class_features']['feature5']['uses'])))
        if char['class_features']['feature5']['rest'] == 'long':
            data.append(('51', 'Yes'))
        elif char['class_features']['feature5']['rest'] == 'short':
            data.append(('52', 'Yes'))
    if char['class_features']['feature6']['name'] != '':
        data.append(('Class Name 6', char['class_features']['feature6']['name']))
        data.append(('Class Max 6', str(char['class_features']['feature6']['uses'])))
        if char['class_features']['feature6']['rest'] == 'long':
            data.append(('53', 'Yes'))
        elif char['class_features']['feature6']['rest'] == 'short':
            data.append(('54', 'Yes'))

    # section 7 - skills
    data.append(('Acrobatics', '+' + str(char['skills']['acrobatics']['mod'])))
    if char['skills']['acrobatics']['prof']:
        data.append(('11', 'Yes'))
    data.append(('Animal Handling', '+' + str(char['skills']['animalhandling']['mod'])))
    if char['skills']['animalhandling']['prof']:
        data.append(('13', 'Yes'))
    data.append(('Arcana', '+' + str(char['skills']['arcana']['mod'])))
    if char['skills']['arcana']['prof']:
        data.append(('15', 'Yes'))
    data.append(('Athletics', '+' + str(char['skills']['athletics']['mod'])))
    if char['skills']['athletics']['prof']:
        data.append(('17', 'Yes'))
    data.append(('Deception', '+' + str(char['skills']['deception']['mod'])))
    if char['skills']['deception']['prof']:
        data.append(('19', 'Yes'))
    data.append(('History', '+' + str(char['skills']['history']['mod'])))
    if char['skills']['history']['prof']:
        data.append(('21', 'Yes'))
    data.append(('Insight', '+' + str(char['skills']['insight']['mod'])))
    if char['skills']['insight']['prof']:
        data.append(('23', 'Yes'))
    data.append(('Intimidation', '+' + str(char['skills']['intimidation']['mod'])))
    if char['skills']['intimidation']['prof']:
        data.append(('25', 'Yes'))
    data.append(('Investigation', '+' + str(char['skills']['investigation']['mod'])))
    if char['skills']['investigation']['prof']:
        data.append(('27', 'Yes'))
    data.append(('Medicine', '+' + str(char['skills']['medicine']['mod'])))
    if char['skills']['medicine']['prof']:
        data.append(('29', 'Yes'))
    data.append(('Nature', '+' + str(char['skills']['nature']['mod'])))
    if char['skills']['nature']['prof']:
        data.append(('31', 'Yes'))
    data.append(('Perception', '+' + str(char['skills']['perception']['mod'])))
    if char['skills']['perception']['prof']:
        data.append(('33', 'Yes'))
    data.append(('Performance', '+' + str(char['skills']['performance']['mod'])))
    if char['skills']['performance']['prof']:
        data.append(('35', 'Yes'))
    data.append(('Persuasion', '+' + str(char['skills']['persuasion']['mod'])))
    if char['skills']['persuasion']['prof']:
        data.append(('81', 'Yes'))
    data.append(('Religion', '+' + str(char['skills']['religion']['mod'])))
    if char['skills']['religion']['prof']:
        data.append(('85', 'Yes'))
    data.append(('Sleight of Hand', '+' + str(char['skills']['sleightofhand']['mod'])))
    if char['skills']['sleightofhand']['prof']:
        data.append(('40', 'Yes'))      # this is a bug and probably needs to be fixed - its also the Wis Save Prof flag
    data.append(('Stealth', '+' + str(char['skills']['stealth']['mod'])))
    if char['skills']['stealth']['prof']:
        data.append(('84', 'Yes'))
    data.append(('Survival', '+' + str(char['skills']['survival']['mod'])))
    if char['skills']['survival']['prof']:
        data.append(('89', 'Yes'))

    # section 8 - weapons
    if char['weapons']['weapon1']['name'] != '':
        data.append(('Weapon 1', char['weapons']['weapon1']['name']))
        data.append(('To Hit 1', '+' + str(char['weapons']['weapon1']['hit'])))
        data.append(('Damage 1', char['weapons']['weapon1']['dmg']))
        data.append(('Type 1', char['weapons']['weapon1']['type']))
        data.append(('Range 1', char['weapons']['weapon1']['range']))
        data.append(('Properties 1', char['weapons']['weapon1']['prop']))
    if char['weapons']['weapon2']['name'] != '':
        data.append(('Weapon 2', char['weapons']['weapon2']['name']))
        data.append(('To Hit 2', '+' + str(char['weapons']['weapon2']['hit'])))
        data.append(('Damage 2', char['weapons']['weapon2']['dmg']))
        data.append(('Type 2', char['weapons']['weapon2']['type']))
        data.append(('Range 2', char['weapons']['weapon2']['range']))
        data.append(('Properties 2', char['weapons']['weapon2']['prop']))
    if char['weapons']['weapon3']['name'] != '':
        data.append(('Weapon 3', char['weapons']['weapon3']['name']))
        data.append(('To Hit 3', '+' + str(char['weapons']['weapon3']['hit'])))
        data.append(('Damage 3', char['weapons']['weapon3']['dmg']))
        data.append(('Type 3', char['weapons']['weapon3']['type']))
        data.append(('Range 3', char['weapons']['weapon3']['range']))
        data.append(('Properties 3', char['weapons']['weapon3']['prop']))
    if char['weapons']['weapon4']['name'] != '':
        data.append(('Weapon 4', char['weapons']['weapon4']['name']))
        data.append(('To Hit 4', '+' + str(char['weapons']['weapon4']['hit'])))
        data.append(('Damage 4', char['weapons']['weapon4']['dmg']))
        data.append(('Type 4', char['weapons']['weapon4']['type']))
        data.append(('Range 4', char['weapons']['weapon4']['range']))
        data.append(('Properties 4', char['weapons']['weapon4']['prop']))
    if char['weapons']['weapon5']['name'] != '':
        data.append(('Weapon 5', char['weapons']['weapon5']['name']))
        data.append(('To Hit 5', '+' + str(char['weapons']['weapon5']['hit'])))
        data.append(('Damage 5', char['weapons']['weapon5']['dmg']))
        data.append(('Type 5', char['weapons']['weapon5']['type']))
        data.append(('Range 5', char['weapons']['weapon5']['range']))
        data.append(('Properties 5', char['weapons']['weapon5']['prop']))

    # section 9 - physical limits
    data.append(('Physical 1', str(1 + char['abilities']['conmod'] if char['abilities']['conmod'] >= 0 else .5)))
    data.append(('Physical 2', str(char['abilities']['conmod'] if char['abilities']['conmod'] > 1 else 1)))
    data.append(('Physical 3', str(3 + char['abilities']['conmod'] if char['abilities']['conmod'] >= -2 else 1)))
    data.append(('Physical 4', str(char['limits']['carry_max'])))
    data.append(('Physical 5', str(char['limits']['lift_max'])))
    data.append(('Physical 6', str((3 + char['abilities']['strmod']) // 2) + ' / ' + str(3+char['abilities']['strmod'])))
    data.append(('Physical 7', str(char['abilities']['str'] // 2) + ' / ' + str(char['abilities']['str'])))
    data.append(('Physical 8', str(char['combat']['speed'] // 2)))
    data.append(('physical 9', '18/24/30'))

    # page 2
    # section 10 - feats & traits
    left, right = '', ''
    x = 0
    for feat in char['features']:
        if x % 2 == 0:
            left += feat + '\n\n'
        else:
            right += feat + '\n\n'
        x += 1
    data.append(('Feats 1', left))
    data.append(('Feats 2', right))

    # section 11 - inventory
    left, center, right = '', '', ''
    x = 0
    for inv in char['inventory']['items']:
        if x % 3 == 0:
            left += inv + '\n'
        elif x % 3 == 1:
            center += inv + '\n'
        else:
            right += inv + '\n'
        x += 1

    data.append(('Inventory 1', left))
    data.append(('Inventory 2', center))
    data.append(('Inventory 3', right))

    # section 12 - armor profs
    data.append(('Armour Proficiency', '\n'.join(char['armor_prof'])))

    # section 13 - weapon prof
    data.append(('Weapon  Proficiency', '\n'.join(char['weapon_prof'])))

    # section 14 - tool prof
    data.append(('Tool Proficiency', '\n'.join(char['tool_prof'])))

    # section 15 - languages
    data.append(('Language Proficiency', '\n'.join(char['languages'])))

    # section 16 - coins
    data.append(('PP', str(char['monies']['PP'])))
    data.append(('GP', str(char['monies']['GP'])))
    data.append(('EP', str(char['monies']['EP'])))
    data.append(('SP', str(char['monies']['SP'])))
    data.append(('CP', str(char['monies']['CP'])))

    # page 3
    # section 17 - spellcasting
    data.append(('Spells Knows', str(char['spells']['prep'])))
    data.append(('SpellBonus', '+' + str(char['spells']['atk'])))
    data.append(('Spell Save DC', str(char['spells']['dc'])))
    data.append(('l0', str(char['spells']['l0'])))
    data.append(('l1', str(char['spells']['l1'])))
    data.append(('l2', str(char['spells']['l2'])))
    data.append(('l3', str(char['spells']['l3'])))
    data.append(('l4', str(char['spells']['l4'])))
    data.append(('l5', str(char['spells']['l5'])))
    data.append(('l6', str(char['spells']['l6'])))
    data.append(('l7', str(char['spells']['l7'])))
    data.append(('l8', str(char['spells']['l8'])))
    data.append(('l9', str(char['spells']['l9'])))

    # cantrips
    if len(char['spells']['level0']) > 0:
        placard = 1
        for spell in char['spells']['level0']:
            data.append((str(placard), spell))
            placard += 1

    # level 1
    if len(char['spells']['level1']) > 0:
        placard = 1
        for spell in char['spells']['level1']:
            data.append((str(placard)+'_2', spell))
            placard += 1

    # level 2
    if len(char['spells']['level2']) > 0:
        placard = 1
        for spell in char['spells']['level2']:
            data.append((str(placard)+'_3', spell))
            placard += 1

    # level 3
    if len(char['spells']['level3']) > 0:
        placard = 1
        for spell in char['spells']['level3']:
            data.append((str(placard)+'_4', spell))
            placard += 1

    # level 4
    if len(char['spells']['level4']) > 0:
        placard = 1
        for spell in char['spells']['level4']:
            data.append((str(placard)+'_5', spell))
            placard += 1

    # level 5
    if len(char['spells']['level5']) > 0:
        placard = 1
        for spell in char['spells']['level5']:
            data.append((str(placard)+'_6', spell))
            placard += 1

    # level 6
    if len(char['spells']['level6']) > 0:
        placard = 1
        for spell in char['spells']['level6']:
            data.append((str(placard)+'_7', spell))
            placard += 1

    # level 7
    if len(char['spells']['level7']) > 0:
        placard = 1
        for spell in char['spells']['level7']:
            data.append((str(placard)+'_8', spell))
            placard += 1

    # level 8
    if len(char['spells']['level8']) > 0:
        placard = 1
        for spell in char['spells']['level8']:
            data.append((str(placard)+'_9', spell))
            placard += 1

    # level 9
    if len(char['spells']['level9']) > 0:
        placard = 1
        for spell in char['spells']['level9']:
            data.append((str(placard)+'_10', spell))
            placard += 1

    return list(data)


def build_wotc_fieldset(char):
    data = []

    # info section
    data.append(('CharacterName', char['info']['name']))
    data.append(('CharacterName 2', char['info']['name']))
    data.append(('PlayerName', char['info']['p_name']))
    if char['info']['subrace'] != '':
        data.append(('Race ', char['info']['race'] + ' (' + char['info']['subrace'] + ')'))
    else:
        data.append(('Race ', char['info']['race']))
    data.append(('ClassLevel', char['info']['class'] + ' ' + str(char['info']['level'])))
    data.append(('Background', char['info']['background']))
    data.append(('Bonds', char['info']['bonds']))
    data.append(('Age', str(char['info']['age'])))
    data.append(('Height', char['info']['height']))
    data.append(('Weight', char['info']['height']))
    data.append(('Eyes', char['info']['eyes']))
    data.append(('Skin', char['info']['skin']))
    data.append(('Hair', char['info']['hair']))
    data.append(('Backstory', char['info']['backstory']))
    data.append(('Flaws', char['info']['flaws']))
    data.append(('Ideals', char['info']['ideals']))
    data.append(('PersonalityTraits ', '\n'.join(char['info']['personalitytraits'])))
    data.append(('Alignment', char['info']['alignment']))
    data.append(('FactionName', char['info']['deity']))
    data.append(('Allies', char['info']['allies']))
    data.append(('XP', str(char['info']['exp']) + '/' + str(char['info']['expneeded'])))

    # abilities section
    data.append(('STR', str(char['abilities']['str'])))
    data.append(('STRmod', '+' + str(char['abilities']['strmod'])))
    data.append(('DEX', str(char['abilities']['dex'])))
    data.append(('DEXmod ', '+' + str(char['abilities']['dexmod'])))
    data.append(('CON', str(char['abilities']['con'])))
    data.append(('CONmod', '+' + str(char['abilities']['conmod'])))
    data.append(('INT', str(char['abilities']['int'])))
    data.append(('INTmod', '+' + str(char['abilities']['intmod'])))
    data.append(('WIS', str(char['abilities']['wis'])))
    data.append(('WISmod', '+' + str(char['abilities']['wismod'])))
    data.append(('CHA', str(char['abilities']['cha'])))
    data.append(('CHamod', '+' + str(char['abilities']['chamod'])))
    data.append(('ProfBonus', '+' + str(char['abilities']['prof'])))

    # skills section
    data.append(('Acrobatics', '+' + str(char['skills']['acrobatics']['mod'])))
    if char['skills']['acrobatics']['prof']:
        data.append(('Check Box 23', 'Yes'))
    data.append(('Animal', '+' + str(char['skills']['animalhandling']['mod'])))
    if char['skills']['animalhandling']['prof']:
        data.append(('Check Box 24', 'Yes'))
    data.append(('Arcana', '+' + str(char['skills']['arcana']['mod'])))
    if char['skills']['arcana']['prof']:
        data.append(('Check Box 25', 'Yes'))
    data.append(('Athletics', '+' + str(char['skills']['athletics']['mod'])))
    if char['skills']['athletics']['prof']:
        data.append(('Check Box 26', 'Yes'))
    data.append(('Deception ', '+' + str(char['skills']['deception']['mod'])))
    if char['skills']['deception']['prof']:
        data.append(('Check Box 27', 'Yes'))
    data.append(('History ', '+' + str(char['skills']['history']['mod'])))
    if char['skills']['history']['prof']:
        data.append(('Check Box 28', 'Yes'))
    data.append(('Insight', '+' + str(char['skills']['insight']['mod'])))
    if char['skills']['insight']['prof']:
        data.append(('Check Box 29', 'Yes'))
    data.append(('Intimidation', '+' + str(char['skills']['intimidation']['mod'])))
    if char['skills']['intimidation']['prof']:
        data.append(('Check Box 30', 'Yes'))
    data.append(('Investigation ', '+' + str(char['skills']['investigation']['mod'])))
    if char['skills']['investigation']['prof']:
        data.append(('Check Box 31', 'Yes'))
    data.append(('Medicine', '+' + str(char['skills']['medicine']['mod'])))
    if char['skills']['medicine']['prof']:
        data.append(('Check Box 32', 'Yes'))
    data.append(('Nature', '+' + str(char['skills']['nature']['mod'])))
    if char['skills']['nature']['prof']:
        data.append(('Check Box 33', 'Yes'))
    data.append(('Perception ', '+' + str(char['skills']['perception']['mod'])))
    if char['skills']['perception']['prof']:
        data.append(('Check Box 34', 'Yes'))
    data.append(('Performance', '+' + str(char['skills']['performance']['mod'])))
    if char['skills']['performance']['prof']:
        data.append(('Check Box 35', 'Yes'))
    data.append(('Persuasion', '+' + str(char['skills']['persuasion']['mod'])))
    if char['skills']['persuasion']['prof']:
        data.append(('Check Box 36', 'Yes'))
    data.append(('Religion', '+' + str(char['skills']['religion']['mod'])))
    if char['skills']['religion']['prof']:
        data.append(('Check Box 37', 'Yes'))
    data.append(('SleightofHand', '+' + str(char['skills']['sleightofhand']['mod'])))
    if char['skills']['sleightofhand']['prof']:
        data.append(('Check Box 38', 'Yes'))
    data.append(('Stealth ', '+' + str(char['skills']['stealth']['mod'])))
    if char['skills']['stealth']['prof']:
        data.append(('Check Box 39', 'Yes'))
    data.append(('Survival', '+' + str(char['skills']['survival']['mod'])))
    if char['skills']['survival']['prof']:
        data.append(('Check Box 40', 'Yes'))
    data.append(('Passive', str(char['skills']['perception']['pass'])))

    # health section
    data.append(('HPMax', str(char['health']['max_hp'])))
    temp = ''
    if char['health']['d6'] > 0:
        temp += str(char['health']['d6']) + 'd6'
    if char['health']['d8'] > 0:
        if temp != '':
            temp += '/'
        temp += str(char['health']['d8']) + 'd8'
    if char['health']['d10'] > 0:
        if temp != '':
            temp += '/'
        temp += str(char['health']['d10']) + 'd10'
    if char['health']['d12'] > 0:
        if temp != '':
            temp += '/'
        temp += str(char['health']['d12']) + 'd12'
    data.append(('HDTotal', temp))

    # defense section
    data.append(('AC', str(char['defense']['ac'])))
    data.append(('ST Strength', '+' + str(char['defense']['str_save']['mod'])))
    if char['defense']['str_save']['prof']:
        data.append(('Check Box 11', 'Yes'))
    data.append(('ST Dexterity', '+' + str(char['defense']['dex_save']['mod'])))
    if char['defense']['dex_save']['prof']:
        data.append(('Check Box 18', 'Yes'))
    data.append(('ST Constitution', '+' + str(char['defense']['con_save']['mod'])))
    if char['defense']['con_save']['prof']:
        data.append(('Check Box 19', 'Yes'))
    data.append(('ST Intelligence', '+' + str(char['defense']['int_save']['mod'])))
    if char['defense']['int_save']['prof']:
        data.append(('Check Box 20', 'Yes'))
    data.append(('ST Wisdom', '+' + str(char['defense']['wis_save']['mod'])))
    if char['defense']['wis_save']['prof']:
        data.append(('Check Box 21', 'Yes'))
    data.append(('ST Charisma', '+' + str(char['defense']['cha_save']['mod'])))
    if char['defense']['cha_save']['prof']:
        data.append(('Check Box 22', 'Yes'))

    # combat section
    data.append(('Initiative', '+' + str(char['combat']['init'])))
    data.append(('Speed', str(char['combat']['speed'])))

    # weapons section
    temp, attkextra = '', ''
    data.append(('Wpn Name', char['weapons']['weapon1']['name']))
    data.append(('Wpn1 AtkBonus', '+' + str(char['weapons']['weapon1']['hit'])))
    if char['weapons']['weapon1']['range'] != '':
        temp = ' *'
        attkextra += '* ' + char['weapons']['weapon1']['range'] + ' - ' + char['weapons']['weapon1']['prop'] + '\n'
    data.append(('Wpn1 Damage', char['weapons']['weapon1']['dmg'] + ' ' + char['weapons']['weapon1']['type'] + temp))

    data.append(('Wpn Name 2', char['weapons']['weapon2']['name']))
    data.append(('Wpn2 AtkBonus ', '+' + str(char['weapons']['weapon2']['hit'])))
    if char['weapons']['weapon2']['range'] != '':
        temp = ' ^'
        attkextra += '^ ' + char['weapons']['weapon2']['range'] + ' - ' + char['weapons']['weapon2']['prop'] + '\n'
    data.append(('Wpn2 Damage ', char['weapons']['weapon2']['dmg'] + ' ' + char['weapons']['weapon2']['type'] + temp))

    data.append(('Wpn Name 3', char['weapons']['weapon3']['name']))
    data.append(('Wpn3 AtkBonus  ', '+' + str(char['weapons']['weapon3']['hit'])))
    if char['weapons']['weapon3']['range'] != '':
        temp = ' #'
        attkextra += '# ' + char['weapons']['weapon3']['range'] + ' - ' + char['weapons']['weapon3']['prop'] + '\n'
    data.append(('Wpn3 Damage ', char['weapons']['weapon3']['dmg'] + ' ' + char['weapons']['weapon3']['type'] + temp))
    data.append(('AttacksSpellcasting', attkextra))

    # features section
    data.append(('Features and Traits', '\n'.join(char['features'])))

    # inventory section
    inv = []
    line = char['inventory']['items'][0] if len(char['inventory']['items']) > 0 else ""
    for i in range(1, len(char['inventory']['items'])):
        if (3 + len(line) + len(char['inventory']['items'][i])) < 26:
            line += ' / ' + char['inventory']['items'][i]
        else:
            inv.append(line)
            line = char['inventory']['items'][i]
    data.append(('Equipment', '\n'.join(inv)))

    # money
    data.append(('CP', str(char['monies']['CP'])))
    data.append(('SP', str(char['monies']['SP'])))
    data.append(('EP', str(char['monies']['EP'])))
    data.append(('GP', str(char['monies']['GP'])))
    data.append(('PP', str(char['monies']['PP'])))

    # profs
    temp = ''
    temp += 'Armor Proficiencies:\n'
    temp += ' * '.join(char['armor_prof'])
    temp += '\n\nWeapon Proficiencies:\n'
    temp += ' * '.join(char['weapon_prof'])
    temp += '\n\nTool Proficiencies\n'
    temp += ' * '.join(char['tool_prof'])
    temp += '\n\nLanguages:\n'
    temp += ' * '.join(char['languages'])
    data.append(('ProficienciesLang', temp))

    # spells
    if char['spells']['stat'] != '':
        data.append(('Spellcasting Class 2', char['spells']['class']))
        data.append(('SpellcastingAbility 2', char['spells']['stat'].upper()))
        data.append(('SpellSaveDC  2', str(char['spells']['dc'])))
        data.append(('SpellAtkBonus 2', '+' + str(char['spells']['atk'])))
        if char['spells']['l0'] > 0:
            slot = 1016
            for spell in char['spells']['level0']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l1'] > 0:
            data.append(('SlotsTotal 19', str(char['spells']['l1'])))
            slot = 1023
            for spell in char['spells']['level1']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l2'] > 0:
            data.append(('SlotsTotal 20', str(char['spells']['l2'])))
            slot = 1034
            for spell in char['spells']['level2']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l3'] > 0:
            data.append(('SlotsTotal 21', str(char['spells']['l3'])))
            slot = 1047
            for spell in char['spells']['level3']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l4'] > 0:
            data.append(('SlotsTotal 22', str(char['spells']['l4'])))
            slot = 1060
            for spell in char['spells']['level4']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l5'] > 0:
            data.append(('SlotsTotal 23', str(char['spells']['l5'])))
            slot = 1073
            for spell in char['spells']['level5']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l6'] > 0:
            data.append(('SlotsTotal 24', str(char['spells']['l6'])))
            slot = 1082
            for spell in char['spells']['level6']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l7'] > 0:
            data.append(('SlotsTotal 25', str(char['spells']['l7'])))
            slot = 1091
            for spell in char['spells']['level7']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l8'] > 0:
            data.append(('SlotsTotal 26', str(char['spells']['l8'])))
            slot = 10100
            for spell in char['spells']['level8']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1
        if char['spells']['l9'] > 0:
            data.append(('SlotsTotal 27', str(char['spells']['l9'])))
            slot = 10107
            for spell in char['spells']['level9']:
                data.append(('Spells ' + str(slot), spell))
                slot += 1

    return data


if __name__ == '__main__':
    build_fdf([], 'none')
