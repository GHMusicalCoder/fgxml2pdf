def process_normal_node(tag, text, fdf_data):
    if tag == 'age':
        fdf_data.append(('Age', text))
    elif tag == 'alignment':
        fdf_data.append(('Alignment', text))
    elif tag == 'background':
        fdf_data.append(('Background', text))
    elif tag == 'bonds':
        fdf_data.append(('Bonds', text))
    elif tag == 'deity':
        fdf_data.append(('FactionName', text))
    elif tag == 'flaws':
        fdf_data.append(('Flaws', text))
    elif tag == 'height':
        fdf_data.append(('Height', text))
    elif tag == 'ideals':
        fdf_data.append(('Ideals', text))
    elif tag == 'perception':
        fdf_data.append(('Passive', text))
    elif tag == 'personalitytraits':
        fdf_data.append(('PersonalityTraits ', text))
    elif tag == 'race':
        fdf_data.append(('Race ', text))


if __name__ == '__main__':
    process_normal_node('', '', [])