#!/usr/bin/python3

import sys
import os

version = "1.0"
program_name = os.path.basename(__file__)
authors = "Maciej Sypień"


def main():
    maxwidth = 100
    print_start()
    count = 0
    while True:
        try:
            line = input()
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


def print_start():
    print('<table border="1">')


def print_end():
    print('</table>')


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


def print_line(line, color, maxwidth=100):
    print('<tr style="background: {0}">'.format(color))
    fields = extract_fields(line)
    for field in fields:
        if not field:
            print("<td></td>")
        else:
            number = field.replace(",", "")
            try:
                x = float(number)
                print('<td align="right"{0:d}</td>'.format(round(x)))
            except ValueError:
                field = field.title()
                field = field.replace(" And ", " and ")
                if len(field) <= maxwidth:
                    field = escape_html(field)
                else:
                    field = "{0} ...".format(escape_html(field[:maxwidth]))
                print("<td>{0}</td>".format(field))
    print("</tr>")


def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


# Begin of program
# print(sys.version)
if len(sys.argv) > 1:
    try:
        if sys.argv[1] in ("-h", "--help"):
            s = ("{0:-^50}\n"
                 "Example usage:\n"
                 "$ {2} [PATH]\n"
                 "{1:-<50}".format(" Help ", "", program_name))
            print(s)
        elif sys.argv[1] in ("-V", "--version"):
            s = ("{0}  v{1}\n"
                 "License GPLv3+: GNU GPL version 3 or later "
                 "http://gnu.org/licenses/gpl.html\n"
                 "\n"
                 "Author: {2}").format(program_name, version, authors)
            print(s)
        else:
            main()
    except ValueError as err:
        print(err)
else:
    print("Nothing happen. Use '{0} --help' for help".format(
        os.path.basename(__file__)))
