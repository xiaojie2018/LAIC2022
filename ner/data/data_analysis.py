# -*- conding: utf-8 -*-
# @Time    : 2022/11/14  18:50
# @Author  : psi

import json


train_file = '../o_data/train.json'
test_file = '../o_data/test.json'
un_label_file1 = "../o_data/危险驾驶罪-样本标签集-8000"
un_label_file2 = "../o_data/危险驾驶罪-样本标签集-2000"


class DataAnalysis:

    def __init__(self, train_file_name, test_file_name=None, un_label_file_name1=None, un_label_file_name2=None):
        self.train_file = train_file_name
        self.test_file = test_file_name
        self.un_label_file1 = un_label_file_name1
        self.un_label_file2 = un_label_file_name2

    def read_txt(self, file):
        data = []
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = json.loads(line)
                data.append(line)
        return data

    def get_train_data(self):
        train_data = self.read_txt(self.train_file)
        data = []
        text_len = []
        label_nums = {}
        label_words = {}
        for line in train_data:
            assert len(line['entities']) == len(line['entities_text']), 'error length'
            text = line['context']
            text_len.append(len(text))
            entities_text = line['entities_text']
            r_entities = []
            for entities in line['entities']:
                label = entities['label']
                span = entities['span']
                words = entities_text[label]
                if label not in label_nums:
                    label_nums[label] = 0
                    label_words[label] = {}
                label_nums[label] += len(span)

                for s, w in zip(span, words):
                    start_pos, end_pos = s.split(';')
                    assert text[int(start_pos): int(end_pos)] == w, 'error'
                    r_entities.append({
                        "start_pos": int(start_pos),
                        "word": w,
                        "end_pos": int(end_pos),
                        "entity_type": label
                    })
                    if w not in label_words[label]:
                        label_words[label][w] = 0
                    label_words[label][w] += 1

            data.append({
                "id": line['id'],
                "text": text,
                "entities": r_entities
            })
        return data

    def get_test_data(self):
        data = []
        text_len = []
        test_data = self.read_txt(self.test_file)
        for line in test_data:
            text_len.append(len(line['context']))

    def get_un_label_data(self):
        data1 = self.read_txt(self.un_label_file1)
        data2 = self.read_txt(self.un_label_file2)
        un_label_data = list(set([x['fullText'] for x in data1+data2]))
        text_len = []
        for x in un_label_data:
            text_len.append(len(x))

    def pipline(self):
        # self.get_train_data()
        # self.get_test_data()
        self.get_un_label_data()


if __name__ == '__main__':
    da = DataAnalysis(train_file_name=train_file, test_file_name=test_file,
                      un_label_file_name1=un_label_file1, un_label_file_name2=un_label_file2)
    da.pipline()
