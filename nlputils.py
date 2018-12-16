from nltk.parse.corenlp import CoreNLPParser
import functools
import string
import jieba.posseg as pseg
import jieba
import logging

jieba.setLogLevel(logging.INFO) # 关闭结巴分词的log信息

'''
中文词性对应表:
https://gist.github.com/luw2007/6016931#ictclas-%E6%B1%89%E8%AF%AD%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8%E9%9B%86

Stanford parser server 相关
https://stanfordnlp.github.io/CoreNLP/corenlp-server.html
'''

url = 'http://10.133.6.180:9000/'
url_En = 'http://10.133.6.180:9000/'
url_Han = 'http://10.133.6.180:9001/'


def containHan(s):
    '''包含汉字的返回TRUE'''
    for c in s:
        if '\u4e00' <= c <= '\u9fa5':
            return True
    
    return False


def parse_sentense(sentence):
    return choose_function(sentence, parse_sentence_Han, parse_sentence_En)(sentence)

def choose_function(sentence, func_Han, func_En):
    global url
    if containHan(sentence):
        url = url_Han
        return func_Han
    else:
        url = url_En
        return func_En

def parse_sentence_En(sentence):
    sentence = sentence.strip()
    if not sentence:
        return [], [], []

    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(sentence))
    
    return parse_S_or_IP(parse[0])

parse_sentence_Han = parse_sentence_En

def parse_S_or_IP(S):
    subjects = []
    verbs = []
    objects = []
    for i in S:
        if i.label() == 'NP':
            subjects = parse_np(i)
        if i.label() == 'VP':
            v, o = parse_vp(i)
            verbs += v
            objects += o
        if i.label() in ['S', 'IP']:
            s, v, o = parse_S_or_IP(i)
            subjects += s
            verbs += v
            objects += o
        if i.label() in string.punctuation:
            break

    return subjects, verbs, objects


def get_verbs_count_of_sentense(sentence):
    return choose_function(sentence, get_verbs_count_of_sentense_Han, get_verbs_count_of_sentense_En)(sentence)

def get_verbs_count_of_sentense_Han(sentence):
    sentence = sentence.strip()
    if not sentence:
        return [], [], [], []
    
    pronoun = []
    adverb = []
    modal_verb = []
    participle = []
    words = pseg.cut(sentence)
    for word, flag in words:
        if flag == 'r':
            pronoun.append(word)
        elif flag == 'd':
            adverb.append(word)
        elif flag == 'u':
            modal_verb.append(word)
        else:
            continue
            # 中文没有 过去分词/现在分词

    return pronoun, adverb, modal_verb, participle

def get_verbs_count_of_sentense_En(sentence):
    pronoun = []
    adverb = []
    modal_verb = []
    participle = []
    sentence = sentence.strip()
    if not sentence:
        return [], [], [], []

    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(sentence))

    quene = [parse[0]]
    while len(quene) > 0:
        s = quene.pop(0)
        for i in s:
            if not isinstance(i, str):
                quene.append(i)

        if s.label() in ['PRP', 'PRP$', 'WP', 'WP$']:
            pronoun.append(s[0])
        if s.label() in ['RB', 'RBR', 'RBS', 'WRB'] and s[0] != 'not':
            adverb.append(s[0])
        if s.label() in ['MD']:
            modal_verb.append(s[0])
        if s.label() in ['VBG', 'VBN']:
            participle.append(s[0])

    return pronoun, adverb, modal_verb, participle


def parse_np(np):
    ret = []
    last_label = ''
    for i in np:
        if i.label() in ['PRP', 'EX', 'DT', 'PN', 'NR'] or i.label().startswith('NN'):
            if i.label().startswith('NN') and (last_label in ['DT'] or last_label.startswith('NN')):
                ret[-1] += ' ' + i[0]
            elif (i.label().startswith('NN') or i.label() == 'NR') and last_label == 'NR':
                ret[-1] += i[0]
            else:
                ret.append(i[0])
        if i.label() == 'NP':
            ret += parse_np(i)
        last_label = i.label()

    return ret


def parse_vp(vp):
    verbs = []
    objects = []
    for i in vp:
        if i.label() == 'VP':
            v, o = parse_vp(i)
            verbs += v
            objects += o
        elif i.label() == 'NP':
            objects += parse_np(i)
        elif i.label().startswith('VB'):
            verbs.append(i[0])
        elif i.label() == 'VV':
            verbs.append(i[0])
        elif i.label() == 'VRD':
            for j in i:
                if j.label() == 'VV':
                    verbs.append(j[0])
        elif i.label() in string.punctuation:
            break
        else:
            pass
    return verbs, objects


vb_tense_map = {
    'VB': 'present',
    'VBD': 'past',
    'VBG': 'none',  # 'ing',
    'VBN': 'past',
    'VBP': 'present',
    'VBZ': 'present'
}


def parse_sentense_tense(sentence):
    return choose_function(sentence, parse_sentense_tense_Han, parse_sentense_tense_En)(sentence)

def parse_sentense_tense_Han(sentence):
    '''
    中文没时态
    '''
    return 'present'

def parse_sentense_tense_En(sentence):
    sentence = sentence.strip()
    if not sentence:
        return 'none'

    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(sentence))

    quene = [parse[0]]
    while len(quene) > 0:
        s = quene.pop(0)
        for i in s:
            if not isinstance(i, str):
                quene.append(i)
        tag = s.label()

        if tag in ('VBD', 'VBN'):
            return vb_tense_map[tag]
        if tag == 'MD':
            return 'future'
        if tag.startswith('VB'):
            return vb_tense_map[tag]

    return 'none'


def parse_word_tense(word):
    return choose_function(word, parse_word_tense_Han, parse_word_tense_En)(word)

def parse_word_tense_Han(word):
    '''
    中文没时态
    '''
    return 'present'


def parse_word_tense_En(word):
    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(word))

    while not isinstance(parse, str):
        pre = parse.label()
        parse = parse[0]

    if pre.startswith('VB') and pre in vb_tense_map:
        return vb_tense_map[pre]

    return 'none'


def parse_word_type(word):
    return choose_function(word, parse_word_type_Han, parse_word_type_En)(word)


def parse_word_type_Han(word):
    words = pseg.cut(word)
    for _, flag in words:
        if flag.startswith('v'):
            return 'verb'
        elif flag.startswith('n'):
            return 'noun'
        elif flag.startswith('a'):
            return 'adj'
        else:
            continue

    return 'none'

def parse_word_type_En(word):
    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(word))

    while not isinstance(parse, str):
        if parse.label().startswith('VB'):
            return 'verb'
        if parse.label().startswith('NN'):
            return 'noun'
        if parse.label().startswith('JJ'):
            return 'adj'
        parse = parse[0]

    return 'none'


if __name__ == "__main__":
    test_Han = [
        'I want to sleep.',
        '妈妈你睡了吗？',
        '∂∑´® ƒß∂f I don\'t know what I write',
        ''
    ]

    for t in test_Han:
        print(t, containHan(t))

    url_En = 'http://localhost:9000'
    url_Han = 'http://localhost:9001'
    test = [
        'I want a girl.',
        'A girl shot an elephant.',
        'You and I are a couple.',
        'You and I have and see money',
        'I shot an girl',
        'You and I will have a baby!',
        'This system ejects the ATM card',
        'This is a boy',
        'ATM is idle, displaying a Welcome message',
        'This is a Welcome message'
    ]

    for t in test:
        print(t, parse_sentense(t), 'tense: ', parse_sentense_tense(t))

    print('-'*80)
    test_words = functools.reduce(lambda x, y: x + y, map(lambda x: x.split(), [
        'I want a girl.',
        'A girl shot an elephant.',
        'You and I are a couple.',
        'You and I have and see money',
        'I shot an girl',
        'You and I will have a baby!'
    ]))

    for t in test_words:
        print(t, f"type: {parse_word_type(t)}",
              'tense: %s' % parse_word_tense(t))

    print('-'*80)
    test_count = [
        'I can do this, however you cannot.',
        'Happily, I have an A finally.',
        'This gril is not that girl.',
        'To be or not to be, it is question.',
        'I would like to swimming rather than running.',
        'ATM is idle, displaying a Welcome message',
        'I wanted to sleep!'
    ]
    for t in test_count:
        print(t, get_verbs_count_of_sentense(t))

    test_Han = [
        '他来到了网易杭研大厦.',
        '我是小明，她是小红.',
        '芷若，这件事我在心中已想了很久。.',
        '我爱你',
        '我今天去上学',
        '我打篮球',
        '汽车在高速上奔驰',
        '然而，芷若，我不能瞒你，要是我这一生再不能见到赵姑娘，我是宁可死了的好。',
        '那日在大都，我见你到那小酒店去和她相会，便知你内心真正情爱之所系。'
    ]
    for t in test_Han:
        print(t, parse_sentense(t))
