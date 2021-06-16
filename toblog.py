# -*-coding:utf-8-*-

import re
import sys


def replace(file_name, output_file_name):
    p1 = r'_(?=[^\n\$]*\$)'
    p2 = r"_(?=[^\$]*\$\$)"
    np1 = r'\\_'
    p_nl = r'\\\\'
    p_cr = r'\\cr'
    f = open(file_name, 'r')
    f_output = open(output_file_name, 'w')
    all_lines = f.read()
    new_lines = re.sub(p1, np1, all_lines)
    new_lines = re.sub(p2, np1, new_lines)
    new_lines = re.sub(p_nl, p_cr, new_lines)
    f_output.write(new_lines)
    f.close()
    f_output.close()
    #except Exception, e:
    #    print(e)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need file name")
        sys.exit(1)
    file_name = sys.argv[1]
    # file_name = "极大似然小结.md".decode('utf-8')
    # default end with '.md'
    suffix = file_name.split('.')[-1]
    output_file_name = file_name.split('.')[0] + "_blog." + suffix
    replace(file_name, output_file_name)
