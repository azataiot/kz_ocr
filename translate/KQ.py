import json
def kzlatin(src):
    with open('../dict/dict.json','r') as f:
        KQ=json.load(f)
    with open(src) as pt:
        p = pt.read()
    for key,value in KQ.items():
        p = p.replace(key,value)
    return p

# returnesss = kzlatin('../../test/kz.txt')

def print_result(fsrc):
    print(kzlatin(fsrc))

# test_file = '../../test/kz.txt'


def kzlatinstr(string):
    with open('dict.json', 'r') as f:
        KQ=json.load(f)
    p = string
    for key, value in KQ.items():
        p = p.replace(key, value)
    return p

#
#print(kzlatinstr("QazKaz - жасанды интеллект технологиясына негізделген көпфункционалды қазақ интеграцияланған өңдеу жүйесі."))
