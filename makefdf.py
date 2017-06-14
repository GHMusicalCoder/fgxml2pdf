from fdfgen import forge_fdf


def build_fdf(fields, filename):
    if fields != [] and filename != 'none':
        fdf = forge_fdf("", fields, [], [], [])
        fdf_file = open(filename, "wb")
        fdf_file.write(fdf)
        fdf_file.close()
    else:
        print("error in buildfdf - fields were empty and filename was none")


def build_type2_fields(char):
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

    return list(data)


if __name__ == '__main__':
    build_fdf([], 'none')
