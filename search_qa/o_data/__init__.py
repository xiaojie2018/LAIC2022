# -*- conding: utf-8 -*-
# @Time    : 2022/11/23  18:36
# @Author  : psi

import json
import re


def cut_text(text):
    flag1 = ' '
    flag2 = '\u2003'
    flag3 = '\u3000'
    res = re.split('[" ", "。"]', text)
    print(1)


def read_json(file):
    data = []
    no_answer = {0: 0, 1: 0}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = json.loads(line)
            org_answer = line['org_answer'].split(' ')
            if org_answer == ["NoAnswer"] or org_answer[0] == 'NoAnswer':
                no_answer[1] += 1
                continue
            else:
                no_answer[0] += 1
            for x in org_answer:
                if x not in line['doc_text']:
                    print(1)
                for x in line['answer_list']:
                    if x.replace(' ', '').replace('\u2003', '').replace('\u3000', '') not in line['org_answer'].replace(' ', '').replace('\u2003', '').replace('\u3000', ''):
                        print(1)
                # if len(line['answer_list']) != len(line['org_answer'].split(' ')):
                #     print(1)

            data.append(line)

    print(1)


if __name__ == '__main__':
    train_file = "./train_data/train.json"
    # read_json(train_file)
    t = "xxs。xxs xxxxsafv。xxssss xxxaaa"
    cut_text(t)
