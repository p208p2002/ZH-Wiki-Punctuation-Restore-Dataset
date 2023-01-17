from glob import glob
import json
import opencc
from loguru import logger
import argparse
from copy import deepcopy
import json
import shutil
import random
import os
from utils import ch_text_norm,clean_punct,gen_input_and_bio

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--translate", default='s2tw',
                    choices=['s2t', 't2s', 's2tw', 'tw2s', 's2hk', 'hk2s'])
args = parser.parse_args()

GEN_TRAIN_DOCS = 30000 
GEN_TEST_DOCS = 3000 
GEN_DEV_DOCS = 3000

class OpenccObjectTranslater():
    def __init__(self, trans_target) -> None:
        self.converter = opencc.OpenCC(f'{trans_target}.json')

    def __call__(self, json_object):
        json_object = deepcopy(json_object)
        for k, v in json_object.items():
            if type(v) is str:
                json_object[k] = self.converter.convert(v)
            elif type(v) is dict:
                return self(v)
            else:
                raise NotImplementedError
        return json_object

def data_iterator(files, obj_translater):
    for file in files:
        with open(file, 'r') as f:
            lines = f.read().strip().split("\n")

        for line in lines:
            data = json.loads(line)
            if obj_translater is not None:
                data = obj_translater(data)
            out = clean_punct(ch_text_norm(data['text']),keep_use_punct=True)
            if len(out) <=100:
                continue
            yield out

def clean(dir):
    shutil.rmtree(dir,ignore_errors=True)

if __name__ == "__main__":
    clean('out')
    os.makedirs("out",exist_ok=True)
    out_writer = open(f"out/train.jsonl",'w')

    files = glob("text/*/wiki_*")
    random.shuffle(files)
    logger.info(f"{files}")
    obj_translater = None

    if args.translate is not None:
        obj_translater = OpenccObjectTranslater(args.translate)

    count = 0

    for document in data_iterator(files,obj_translater):
        document = document.split("\n")
        document = list(filter(lambda sent:len(sent)>5 and sent[-1]=='。',document)) # 移除段落標題或是結尾沒有符號的句子
        document = ''.join(document)
        tokens,bios =gen_input_and_bio(document)
        if len(tokens) != len(bios):
            # 轉換至BIO表示法可能會因為連續的符號導致轉換出來的長度不同
            # 這些資料無法使用
            continue
        
        out_writer.write(f"{json.dumps({'tokens':tokens,'bios':bios},ensure_ascii=False)}\n")

        count += 1

        print(count,end='\r')

        if count == GEN_TRAIN_DOCS:
            out_writer = open(f"out/test.jsonl",'w')
        elif count == GEN_TRAIN_DOCS + GEN_TEST_DOCS:
            out_writer = open(f"out/dev.jsonl",'w')
        elif count == GEN_TRAIN_DOCS + GEN_TEST_DOCS + GEN_DEV_DOCS:
            break