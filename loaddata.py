import os


def load_name_data(location):
    players = []
    filename = get_full_pathname(location, 'player_names.txt')
    if os.path.exists(filename):
        with open(filename) as fin:
            for entry in fin.readlines():
                names = entry.split('|')
                players.append((names[0], names[1].strip()))
    return players


def get_full_pathname(loc, name):
    return os.path.abspath(os.path.join('.', loc, name))


if __name__ == '__main__':
    load_name_data()