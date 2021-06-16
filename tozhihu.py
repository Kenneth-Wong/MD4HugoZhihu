# -*-coding:utf-8-*-

import re
import sys


def replace(file_name, output_file_name):
    pattern1 = r"\$\$\n*([\s\S]*?)\n*\$\$"
    new_pattern1 = r'\n<img src="https://www.zhihu.com/equation?tex=\1" alt="\1" class="ee_img tr_noresize" eeimg="1">\n'
    pattern2 = r"\$\n*(.*?)\n*\$"
    new_pattern2 = r'\n<img src="https://www.zhihu.com/equation?tex=\1" alt="\1" class="ee_img tr_noresize" eeimg="1">\n'
    f = open(file_name, 'r')
    f_output = open(output_file_name, 'w')
    all_lines = f.read()
    new_lines1 = re.sub(pattern1, new_pattern1, all_lines)
    new_lines2 = re.sub(pattern2, new_pattern2, new_lines1)
    f_output.write(new_lines2)
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
    output_file_name = file_name.split('.')[0] + "_zhihu." + suffix
    replace(file_name, output_file_name)
