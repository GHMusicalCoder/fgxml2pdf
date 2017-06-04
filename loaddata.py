import os


def load_name_data(file, players):
    filename = get_full_pathname(file)
    if os.path.exists(filename):
        with open(filename) as fin:
            for entry in fin.readlines():
                names = entry.split('|')
                players.append((names[0], names[1].strip()))


def get_full_pathname(name):
    return os.path.abspath(os.path.join('.', name))


if __name__ == '__main__':
    load_name_data()