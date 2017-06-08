import makefdf
import pullxml
import os


def main():
    path = os.path.join('/home', 'chris', 'Documents')
    os.chdir(path)
    # xml_filename = get_xml_filename() + ".xml"
    xml_filename = 'romulus.xml'
    field_values = pullxml.process_xml_file(xml_filename)
    # pullxml.pull_xml(xml_filename)
    # print(*field_values)
    fdf_filename = 'fgoutput.fdf'
    makefdf.build_fdf(field_values, fdf_filename)
    pdftk = "pdftk sample.pdf fill_form fgoutput.fdf output romulus.pdf flatten"
    os.system(pdftk)


def get_xml_filename():
    print('Enter the name of your xml file -- just the file name - we will handle the .xml portion')
    print()
    file = input()
    return file


if __name__ == '__main__':
    main()
