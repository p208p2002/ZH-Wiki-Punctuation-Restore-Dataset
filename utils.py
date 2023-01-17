import unicodedata
from typing import List

USE_ZH_PUNCTUATION = [
    '，',
    '、',
    '。',
    '？',
    '！',
    '；',
]

def isFull(c:str)->bool:
    # 全形字元的 unicode 編碼是從 65281 到 65374
    return ord(c) in range(65281,65374+1)

def isHalf(c:str)->bool:
    # 半形字元的 unicode 編碼是從 33 到 126
    return ord(c) in range(33,126+1)

def full2half(c: str) -> str:
    if isFull(c):
        return chr(ord(c)-65248)
    return c


def half2full(c: str) -> str:
    if isHalf(c):
        return chr(ord(c)+65248)
    return c

def ch_text_norm(text):
    # 將所有符號轉換至全形
    # 英文或是數字轉換成半形
    # 符號空白等移除
    # https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)
    text = list(text)
    for t_id,c in enumerate(text):
        if unicodedata.category(c)[0] == 'P':
            new_char = half2full(c)
            text[t_id] = new_char
        if unicodedata.category(c)[0] == 'N' or unicodedata.category(c) in ['Lu','Ll']:
            new_char = full2half(c)
            text[t_id] = new_char
        if unicodedata.category(c)[0] in ['Z','O']:
            text[t_id] = "" # soft del
        if unicodedata.category(c) in ['So']:
            text[t_id] = "" # soft del
    
    return ''.join(text)

def clean_punct(text,keep_use_punct=False):
    text = list(text)
    for t_id,c in enumerate(text):
        if keep_use_punct == True:
            if unicodedata.category(c)[0] == 'P' and c not in USE_ZH_PUNCTUATION:
                text[t_id] = ""
        elif keep_use_punct == False:
            if unicodedata.category(c)[0] == 'P':
                text[t_id] = ""
    return ''.join(text)

def gen_input_and_bio(text: str) -> List[str]:
    tokens = list(text)
    bio = []
    tokens_wo_punct = []
    for t_id, token in enumerate(tokens):
        if token in USE_ZH_PUNCTUATION:
            if len(bio) > 0 and bio[-1] == 'O':
                bio.pop(-1)
            bio.append(f"S-{token}")
        else:
            bio.append('O')
            tokens_wo_punct.append(token)
    return tokens_wo_punct,bio
        
# text = "}』(（)）我🙂今  /天,去買飯，.。０Ａ|0A‘’“”''""「」『』？?"
# text = "我今天，去買范。"
# print(text,len(text))
# print(text:=clean_punct(ch_text_norm(text),keep_use_punct=True),len(text))
# print(bio_tag:=gen_bio_tag(text),len(bio_tag[0]),len(bio_tag[-1]))


