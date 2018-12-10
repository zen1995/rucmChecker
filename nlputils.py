from nltk.parse.corenlp import CoreNLPParser
import functools
import string

# https://stanfordnlp.github.io/CoreNLP/corenlp-server.html
url = 'http://10.133.6.180:9000/'


def parse_sentense(sentence):
    sentence = sentence.strip()
    if not sentence:
        return [], [], []

    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(sentence))
    S = parse[0]
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
        if i.label() in string.punctuation:
            break

    return subjects, verbs, objects


def get_verbs_count_of_sentense(sentence):
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
        if i.label() in ['PRP', 'EX', 'DT'] or i.label().startswith('NN'):
            if i.label().startswith('NN') and (last_label == 'DT' or last_label.startswith('NN')):
                ret[-1] += ' ' + i[0]
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
        if i.label() == 'NP':
            objects += parse_np(i)
        if i.label().startswith('VB'):
            verbs.append(i[0])
        if i.label() in string.punctuation:
            break
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
    parser = CoreNLPParser(url=url)
    parse = next(parser.raw_parse(word))

    while not isinstance(parse, str):
        pre = parse.label()
        parse = parse[0]

    if pre.startswith('VB') and pre in vb_tense_map:
        return vb_tense_map[pre]

    return 'none'


def parse_word_type(word):
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
    url = 'http://localhost:9000'
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
        print(t, parse_sentense(t), 'tense: %s' % parse_sentense_tense(t))

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
