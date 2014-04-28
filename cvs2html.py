#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

__version__ = "1.0"
program_name = os.path.basename(__file__)
authors = "Maciej Sypień"


def main():
    if len(sys.argv) > 1:
        try:
            process_questions()
            options = process_options()
            maxwidth = 100

            if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
                path_to_file = sys.argv[1]
                array = get_linelist_from_file(path_to_file)
                print_start()
                count = 0
                for line in array:
                    try:
                        if count == 0:
                            color = "lightgreen"
                        elif count % 2:
                            count = "white"
                        else:
                            count = "lightyellow"
                        print_line(line, color, maxwidth)
                        count += 1
                    except EOFError:
                        break
                print_end()
            elif len(sys.argv) == 3 and sys.argv[2] == ">":
                print("not done yet")
            else:
                s = ("Wrong usage.\n"
                     "Use '{0} --help' for help").format(program_name)
                print(s)
        except ValueError as err:
            print(err)
    else:
        s = ("Nothing happen.\n"
             "Use '{0} --help' for help.").format(program_name)
        print(s)


def process_options():
    pass


def process_questions():
    if sys.argv[1] in ("-h", "--help"):
        s = ("{0:-^50}\n"
             "Example usage:\n"
             "$ {2} [PATH]\n"
             "{1:-<50}".format(" Help ", "", program_name))
        print(s)
        sys.exit()
    elif sys.argv[1] in ("-V", "--__version__"):
        s = ("{0}  v{1}\n"
             "License GPLv3+: GNU GPL __version__ 3 or later "
             "http://gnu.org/licenses/gpl.html\n"
             "\n"
             "Author: {2}").format(program_name, __version__, authors)
        print(s)
        sys.exit()


def print_start():
    print('<table border="1">')


def print_end():
    print('</table>')


def print_line(line, color, maxwidth=100):
    print('\t<tr style="background: {0}">'.format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("\t\t<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print('\t\t<td align="right">{0:d}</td>'.format(round(x)))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = escape_html(field)
                else:
                    field = "{0} ...".format(escape_html(field[:maxwidth]))
                print("\t\t<td>{0}</td>".format(field))
    print("\t</tr>")


def extract_fields(line):
    fields = []
    field = ""
    quote = None
    for c in line:
        if c in "\"'":
            if quote is None:  # start of quoted string
                quote = c
            elif quote == c:  # end of quoted string
                quote = None
            else:
                field += c  # other quote inside quoted string
            continue
        if quote is None and c == ",":  # end of a field
            fields.append(field)
            field = ""
        else:
            field += c  # accumulating a field
    if field:
        fields.append(field)  # adding the last field
    return fields


def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def get_linelist_from_file(path_to_file):
    try:
        ins = open(path_to_file, "r")
    except IOError:
        print('File does\'t exsist.')
    array = []
    for line in ins:
        array.append(line)
    ins.close()
    return array


def is_cvs_file(path_to_file):
    fileName, fileExtension = os.path.splitext(path_to_file)
    if fileExtension == '.cvs':
        return True
    else:
        return False


# Begin of program
# print(sys.version)
main()
