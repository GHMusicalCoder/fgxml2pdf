import makefdf
import os
from shutil import copyfile
from pullxml import process_xml_file


def main():
    # set our paths
    xml_file_location = os.path.join('/home', 'chris', '.cxoffice', 'Fantasy_Grounds', 'drive_c', 'Program Files',
                                     'Fantasy Grounds')
    xmlpath = os.path.join('/home', 'chris', 'Temp', 'xmlfiles')
    pdfpath = os.path.join('/home', 'chris', 'Documents', 'DnDCharSheets')
    datapath = os.path.join('/home', 'chris', 'Documents', 'DnDCharSheets', 'charData')

    # copy xmlfiles from fantasy grounds to temp/xmlfiles
    for file in os.listdir(xml_file_location):
        if file[-4:] == ".xml" and file != "patchnotes.xml":
            copyfile(xml_file_location + '/' + file, xmlpath + '/' + file)

    # move to our main directory
    os.chdir(pdfpath)

    # loop thru the xml files
    for file in os.listdir(xmlpath):
        filename = os.path.join(xmlpath, file)
        fdf_name = file[:-3] + 'fdf'
        wotc_pdf = file[:-4] + '_wotc.pdf'
        perkins_pdf = file[:-4] + '_perkins.pdf'
        data = process_xml_file(filename, datapath)

        # wotc sheet
        fieldset = makefdf.build_wotc_fieldset(data)
        makefdf.build_fdf(fieldset, fdf_name)
        pdf_command = "pdftk ./blankSheets/wotc_blank_sheet.pdf fill_form " + fdf_name + \
                      " output " + wotc_pdf + " flatten"
        os.system(pdf_command)

        # perkins sheet
        fieldset = makefdf.build_perkins_fieldset(data)
        makefdf.build_fdf(fieldset, fdf_name)
        pdf_command = "pdftk ./blankSheets/perkins_blank_sheet.pdf fill_form " + fdf_name + \
                      " output " + perkins_pdf + " flatten"
        os.system(pdf_command)


if __name__ == '__main__':
    main()
