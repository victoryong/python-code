# coding: utf-8
"""
Created on Dec 23, Sat, 2017

@author: Victor Y, Xie

The script is used to convert md from youdao to typora and vis versa.
What it can do is bellow:
1. Transform formulas.
2. Transform img url forms between "file:///" and the real absolute path
"""

__author__ = "Victor Y, Xie"

import os
import re
import sys

from log_print import get_or_create_logger

logger = get_or_create_logger('convert_md')

LINE_BREAK_FLAG = '{\n}'
# The first element is youdao form and seconde one is typora form for all patterns below.
INLINE_FORMULA = [re.compile(r'`(?P<inline_formula>\$[^\u4e00-\u9fa5$`]+\$)`'),
                  re.compile(r'[^$][\s]+(?P<inline_formula>\$[^\u4e00-\u9fa5$`]+\$)[\s]+[^$]')]
BLOCK_FORMULA = [re.compile(r'```math(?P<block_formula>[^`]+)```'),
                 re.compile(r'\$\$(?P<block_formula>[^$]+)\$\$')]
IMG_URL = [re.compile(r'!\[(?P<img_description>.+)\]\((?P<hdisk_name>[A-Za-z]:/)/(?P<img_path>[^)]+)\)'),
           re.compile(r'!\[(?P<img_description>.+)\]\(file:///(?P<hdisk_name>[A-Za-z]:/)(?P<img_path>[^)]+)\)')]


def youdao2typora(file_abs_path, img_path='default'):
    logger.info(f'start converting file "{file_abs_path}" from youdao2typora...')

    with open(file_abs_path, encoding='utf-8') as fp:
        content = LINE_BREAK_FLAG.join([re.sub(r'\n|\r|\r\n', '', i) for i in fp.readlines()])

    # Convert inline and block formulas to typora form.
    content = re.sub(INLINE_FORMULA[0], lambda x: x.group('inline_formula'), content)
    content = re.sub(BLOCK_FORMULA[0], lambda x: '$$' + x.group('block_formula') + '$$', content)
    if img_path == 'default':
        content = re.sub(IMG_URL[0],
                         lambda x: '![' + x.group('img_description') + '](file:///' + x.group('hdisk_name') +
                                   x.group('img_path') + ')', content)
    else:
        content = re.sub(IMG_URL[0],
                         lambda x: '![' + x.group('img_description') + '](./images/' + x.group('img_path').split('/')[
                             -1] + ')', content)

    # Save to file with postfix "-typora.md"
    with open(file_abs_path.split('-youdao')[0] + '-typora.md', 'w', newline='\n', encoding='utf-8') as fp:
        fp.writelines(re.sub(LINE_BREAK_FLAG, '\n', content))

    logger.info('ok')
    return content


def typora2youdao(file_abs_path):
    logger.info(f'start converting file "{file_abs_path}" from typora2youdao...')

    with open(file_abs_path, encoding='utf-8') as fp:
        content = LINE_BREAK_FLAG.join([re.sub(r'\n|\r|\r\n', '', i) for i in fp.readlines()])

    # Convert inline and block formulas to youdao form.
    content = re.sub(INLINE_FORMULA[1], lambda x: '`' + x.group('inline_formula') + '`', content)
    content = re.sub(BLOCK_FORMULA[1], lambda x: '```math\n' + x.group('block_formula') + '\n```', content)
    content = re.sub(IMG_URL[1], lambda x: '![' + x.group('img_description') + '](' + x.group('hdisk_name') + '/' +
                                           x.group('img_path') + ')', content)

    # Save to file with postfix "-youdao.md"
    with open(file_abs_path.split('-typora')[0] + '-youdao.md', 'w', newline='\n', encoding='utf-8') as fp:
        fp.writelines(re.sub(LINE_BREAK_FLAG, '\n', content))

    logger.info('ok')
    return content


def typora2mdhere(file_abs_path):
    logger.info(f'start converting file "{file_abs_path}" from typora2mdhere...')

    with open(file_abs_path, encoding='utf-8') as fp:
        try:
            lines = fp.readlines()
            lines_list = [re.sub(r'\n|\r|\r\n', '', i) for i in lines]
            content = LINE_BREAK_FLAG.join(lines_list)
        except Exception as e:
            print(e)

    content = re.sub(BLOCK_FORMULA[1], lambda x: '$' + re.sub(r'^{\n}|{\n}$', '', x.group('block_formula')) + '$',
                     content)
    with open(file_abs_path.split('-typora')[0] + '-mdhere.md', 'w', newline='\n', encoding='utf-8') as fp:
        fp.writelines(re.sub(LINE_BREAK_FLAG, '\n', content))

    logger.info('ok')
    return content


def main(filename='./test-youdao.md', method_type='t2y', img_path='default'):
    if not os.path.exists(filename):
        logger.error('File is not exists. ')
        exit(-1)

    if filename.endswith('-youdao.md'):
        youdao2typora(os.path.abspath(filename), img_path=img_path)
    elif filename.endswith('-typora.md'):
        if method_type == 't2y':
            typora2youdao(os.path.abspath(filename))
        elif method_type == 't2m':
            typora2mdhere(os.path.abspath(filename))
    else:
        logger.error('Filename error: either postfix "-youdao.md" or "-typora.md" is needed. ')
        exit(-1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python convert_md.py {filename} [<optional>t2m] [<optional>img_path]')
        sys.exit(-1)
    if len(sys.argv) == 2:
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[2] == 'img_path':
            main(filename=sys.argv[1], img_path=sys.argv[2])
        else:
            main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    # main('./test-typora.md')
