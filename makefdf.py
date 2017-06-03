from fdfgen import forge_fdf


def build_fdf(fields, filename):
    if fields != [] and filename != 'none':
        fdf = forge_fdf("", fields, [], [], [])
        fdf_file = open(filename, "wb")
        fdf_file.write(fdf)
        fdf_file.close()
    else:
        print("error in buildfdf - fields were empty and filename was none")

if __name__ == '__main__':
    build_fdf([], 'none')
