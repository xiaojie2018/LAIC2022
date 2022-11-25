# -*- conding: utf-8 -*-
# @Time    : 2022/11/25  11:18
# @Author  : psi

import re
import json
from tqdm import trange, tqdm


def cut_text(text):
    flag1 = ' '
    flag2 = '\u2003'
    flag3 = '\u3000'
    res = re.split('[" ", "。", "\u2003", "\u3000"]', text)
    res1 = re.split('[" ", "。"]', text)
    res2 = re.split('["。"]', text)

    result = [x + '。' for x in res2]
    return result


def clean_text(text):
    flags = ['\u2003', '\u3000']
    for flag in flags:
        text.replace(flag, '')

    return text


def clean_start_pos(text):

    while True:
        if text.startswith(' ') or text.startswith('\u2003') or text.startswith('\u3000'):
            text = text[1:]
        elif text.endswith(' ') or text.endswith('\u2003') or text.endswith('\u3000'):
            text = text[:-1]
        else:
            break
    return text


def clean_other_text(texts, labels):
    other_symbol = ['\xa0', '\u0020', '\u00A0', '\u200B', '\u2002', '\u2003', '\u3000', ' ']
    assert len(texts) == len(labels), 'error length 1'
    r_text = []
    r_label = []
    for t, l in zip(texts, labels):
        if t in other_symbol:
            continue
        else:
            r_text.append(t)
            r_label.append(l)
    assert len(r_text) == len(r_label), 'error length 2'
    return r_text, r_label


def cut_text_by_period(text, label):
    res = []
    t_res = []
    t_label = []
    for t, l in zip(text, label):
        t_res.append(t)
        t_label.append(l)
        if t == '。':
            t_res, t_label = clean_other_text(t_res, t_label)
            if len(t_res) > 0:
                res.append((t_res, t_label))
            t_res = []
            t_label = []
    if len(t_res) > 0:
        t_res, t_label = clean_other_text(t_res, t_label)
        if len(t_res) > 0:
            res.append((t_res, t_label))
        t_res = []
        t_label = []
    return res


def read_(file):
    data = []
    text_length = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            line = json.loads(line)
            org_answer = line['org_answer']
            answer_list = line['answer_list']
            doc_text = line['doc_text']

            # for x in answer_list:
            #     x = clean_start_pos(x)
            #     if x not in org_answer:
            #         print(1)
            #     if x not in doc_text:
            #         print(2)

            # doc_text = cut_text(doc_text)
            # for x in answer_list:
            #     x = clean_start_pos(x)
            #     if x not in doc_text:
            #         print(1)

            assert len(answer_list) == len(line['answer_start_list']), 'error'

            doc_text_list = list(doc_text)
            doc_text_label = [0]*len(doc_text_list)

            for x, start_pos in zip(answer_list, line['answer_start_list']):
                end_pos = len(x) + start_pos
                assert x == doc_text[start_pos: end_pos], 'error'
                doc_text_label[start_pos: end_pos] = [1]*len(x)

            res = cut_text_by_period(doc_text_list, doc_text_label)
            for r in res:
                # if len(r[0]) > 10000:
                #     print(1)
                text_length.append(len(r[0]))
            line["result"] = res
            data.append(line)
    return data, text_length


def wee(data, file):
    f = open(file, 'w', encoding='utf-8')
    for d in data:
        json.dump(d, f, ensure_ascii=False)
        f.write('\n')
    f.close()
    print('save success {} of length ...'.format(len(data)))


if __name__ == '__main__':
    train_file = "../o_data/train_data/train.json"
    train_data, train_text_length = read_(train_file)
    dev_file = "../o_data/dev_data/dev.json"
    dev_data, dev_text_length = read_(dev_file)

    wee(train_data, 'train.json')
    wee(dev_data, 'dev.json')
