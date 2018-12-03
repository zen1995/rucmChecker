from nltk.parse.corenlp import CoreNLPParser


def parse_sentense(sentence):
    parser = CoreNLPParser()
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

    return subjects, verbs, objects

def parse_np(np):
    ret = []
    for i in np:
        if i.label() in ['PRP', 'NN']:
            ret.append(i[0])

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
    return verbs, objects

def parse_sentense_tense(sentence):
    parser = CoreNLPParser()
    parse = next(parser.raw_parse(sentence))
    vb_tense_map = {
        'VB': 'present',
        'VBD': 'past',
        'VBG': 'none', #'ing',
        'VBN': 'past',
        'VBP': 'present',
        'VBZ': 'present'
    }
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

if __name__ == "__main__":
    test = [
        'I want a girl.',
        'A girl shot an elephant.',
        'You and I are a couple.',
        'You and I have and see money',
        'I shot an girl',
        'You and I will have a baby!'
    ]

    for t in test:
        print(t, parse_sentense(t), 'tense: %s' % parse_sentense_tense(t))
