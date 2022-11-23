# -*- conding: utf-8 -*-
# @Time    : 2022/11/15  14:43
# @Author  : psi

import json


def read_cls(file):
    labels = {}
    data = []
    text_len = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = json.loads(line)
            if len(line['label']) == 1:

                if line['label'][0] not in labels:
                    labels[line['label'][0]] = 0
                labels[line['label'][0]] += 1
            else:

                print(1)

            text_len.append(len(line['data']))
            data.append({
                "id": line['id'],
                "text": line['data'],
                "label": line['label']
            })
    return {"labels": labels, "data": data, "text_len": text_len}


def read_ner(file):
    data = []
    text_len = []
    label_numbers = {}
    label_words_nums = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = json.loads(line)
            text = line['text']
            text_len.append(len(text))
            entities = []
            for e in line['entities']:
                if e['label'] not in label_numbers:
                    label_numbers[e['label']] = 0
                    label_words_nums[e['label']] = {}
                label_numbers[e['label']] += 1
                word = text[e['start_offset']: e['end_offset']]
                if word not in label_words_nums[e['label']]:
                    label_words_nums[e['label']][word] = 0
                label_words_nums[e['label']][word] += 1
                entities.append({
                    "word": word,
                    "start_pos": e['start_offset'],
                    "end_pos": e['end_offset'],
                    "entity_type": e['label']
                })
            data.append({
                "id": line['id'],
                "text": text,
                "entities": entities
            })
    print(1)


anjian = ['中型客车交通肇事', '交通肇事后逃逸', '全部责任', '肇事车辆超速行驶', '肇事车辆逆行', '被害人为本车人员', '被害人被后车撞击',
          '被害人闯红灯']

file_path = "../o_data/训练集/案件要素/"

result = {}
for n in anjian:
    result[n] = read_cls(file_path + n)

result['刑档'] = read_cls('../o_data/训练集/刑档')

read_ner('../o_data/训练集/ner')

print(1)
