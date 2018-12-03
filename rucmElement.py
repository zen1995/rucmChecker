import base
import typing
import json
import re
from enum import Enum, unique
from nlputils import parse_sentense

@unique
class NatureType(Enum):
    validates_that_ = 'VALIDATES THAT'
    do_ = 'DO'
    until_ = 'UNTIL'
    resume_step_ = 'RESUME STEP'
    rfs_ =  'RFS'
    mean_while_ = 'MEANWHILE'
    if_ = 'IF'
    endif_ = 'ENDIF'
    then_ = 'THEN'
    include_use_case_ = 'INCLUDE USE CASE'
    extened_by_usecase_ = 'EXTENDED BY USE CASE'
    abort_ = 'ABORT'
    elseif_ = 'ELSEIF'

class RUCMBase:
    def __init__(self, use_case_name, parent):
        self.useCaseName:str = use_case_name
        self.parent:RUCMBase = parent


class Word(RUCMBase):
    def __init__(self, val:str, use_case_name, parent):
        RUCMBase.__init__(self, use_case_name, parent)
        self.val:str = val
        self.type:base.WordType =None
        self.tense :base.WordTense=None
        self.__parse_word()

    def __parse_word(self):
        pass

    def __repr__(self):
        return self.val

    def __str__(self):
        return self.val

class Sentence(RUCMBase):
    def __init__(self, sentence: str, nature, use_case_name, parent):
        RUCMBase.__init__(self, use_case_name, parent)
        self.val = sentence
        self.subjects: typing.List[Word] =[]
        self.objects: typing.List[Word] = []
        self.verbs: typing.List[Word] = []
        self.tense: base.WordTense = None
        self.words: typing.List[Word] = []
        self.__parse_sentense()
        self.nature: str = nature
    def __parse_sentense(self):
        self.subjects, self.verbs, self.objects = list(map(
            lambda x: list(map(
                lambda y: Word(y, self.useCaseName, self),
                x
            )),
            parse_sentense(self.val)
        ))

    def __str__(self):
        return str({
            'subjects': self.subjects,
            'verbs': self.verbs,
            'objects': self.objects
        })

# 使用loaction描述错误语句的位置
class  Step(RUCMBase):
    def __init__(self, step: dict, index:int, use_case_name, parent):
        RUCMBase.__init__(self, use_case_name, parent)
        self.index = index                                         # step的序号
        self.val: str = step['content']['content']['content']   # step中的字符串，包括关键字如VALIDATES THAT等
        self.sentences: typing.List[Sentence] = []              # step中出现的句子集，剔除了关键字，并进行了划分
        # 分割step，形成sentences, keywords
        self.__parse_step()

    def __parse_step(self):
        keywords = []
        # 生成keywords
        for keyword in NatureType:
            # 存在关键字，并且该关键字是独立的（前后有空格）
            loc = self.__find_key(keyword.value)[1]
            if loc != -1:
                keywords.append([loc, keyword])
        keywords.sort()
        # 生成分割点
        split_point = [0, len(self.val)]
        if len(keywords) != 0:
            if keywords[0][0] == 0:
                split_point = []
            else:
                split_point = [0]
            for [loc, keyword] in keywords:
                split_point.extend([loc, loc + len(keyword.value)])
            if keywords[len(keywords) - 1][0] + len(keyword.value) != len(self.val):
                split_point.append(len(self.val))
        # 删除关键字，生成句子集
        keywords_dict = dict(keywords)
        for i in range(len(split_point) - 1):
            start = split_point[i]
            end = split_point[i + 1]
            sentence = self.val[start: end]
            a = keywords_dict.keys()
            if start in keywords_dict.keys():
                self.sentences.append(Sentence(sentence, keywords_dict[start], self.useCaseName, self))
            else:
                self.sentences.append(Sentence(sentence, None, self.useCaseName, self))
        a = 1
    # 判断是否存在关键字并返回其头部位置
    def __find_key(self, key) -> (bool, int):
        i = -1
        # 边界条件：key长度 > s长度 和 两者长度相等时
        s = self.val
        if len(key) > len(s):
            return False, -1
        elif len(key) == len(s):
            if s == key:
                return True, 0
            else:
                return False, -1
        # 此时len(key) < len(s)成立
        # key顶到最左边的情况
        if s[0: len(key)] == key:
            if s[len(key)] == ' ':
                return True, 0
        i = 1
        # key在s当中的时候
        while i + len(key) < len(s):
            if s[i: i + len(key)] == key:
                # 两侧需要有空格
                if s[i - 1] == ' ' and s[i + len(key)] == ' ':
                    return True, i
            i = i + 1
        # key顶到最右边的情况
        if s[i: i + len(key)] == key:
            if s[i - 1] == ' ':
                return True, i
        return False, -1

class Flow(RUCMBase):
    def __init__(self, flow: dict, index: int, use_case_name, parent):
        RUCMBase.__init__(self, use_case_name, parent)
        self.title = None
        self.introduction = None
        self.type: str=flow['type']        # 是'BasicFlow'、Specific Flow、等
        if flow['content']['name']['content'] != '':
            self.name = flow['content']['name']['content']
        else:
            self.name = self.type
        flow_content = flow['content']
        #后置条件
        self.postCondition: Sentence = Sentence(flow_content['postCondition']['content']\
                                                ['sentences'][0]['content']['content']['content']
                                                , None, self.useCaseName, self)

        self.steps: typing.List[Step] = []
        for i in range(len(flow_content['steps'])):
            self.steps.append(Step(flow_content['steps'][i], i,self.useCaseName, self))
        self.RfsSentence = None
        if self.type!='BasicFlow':
            self.RfsSentence = Sentence(flow_content['rfsSentence']['content']['content']['content']
                                        , None, self.useCaseName, self)
        self.id = index
        # 未实现的部分
        self.include = None
        self.extend = None
        self.generalization = None

    def _get_all_sentences(self)->typing.List[Sentence]:
        sentences = []
        for step in self.steps:
            for sentence in step.sentences:
                if sentence.nature == None or sentence.nature == NatureType.mean_while_.value:
                    sentences.append(sentence)
        # sentences.append(self.postCondition)
        return sentences

    def _get_all_steps(self)->typing.List[Step]:
        return self.steps

class Usecase(RUCMBase):
    def __init__(self, use_case: dict, index: int, parent):
        use_case_content = use_case['content']
        self.name: str = use_case_content['name']['content']   #名字
        RUCMBase.__init__(self, self.name, parent)
        # 设置Use Case的ID
        self.id = index
        # 设置Use Case下的流，流的类型只分为Basic Flow和Alternative Flow。以及前置条件、简述
        self.basicFlow: Flow = None
        self.specificFlows: typing.List[Flow] = []
        self.precondition = None
        self.briefDescription = None
        # specification'有可能不出现
        if 'specification' in use_case_content :
            specification_content = use_case_content['specification']['content']
            self.basicFlow = Flow(specification_content['basicFlow'], 0, self.name, self)
            alt_content = specification_content['alternativeFlows']
            for i in range(len(alt_content)):
                for f in specification_content['alternativeFlows']:
                    self.specificFlows.append(Flow(f, i, self.name, self))
            # 设置precondition和briefDescription
            if 'preCondition' in specification_content :
                self.preCondition = Sentence(specification_content['preCondition']['content']['sentences'][0] \
                                                             ['content']['content'], None, self.name, self)
            if 'briefDescription' in specification_content:
                self.briefDescription = Sentence(specification_content['briefDescription']['content']['sentences'][0] \
                                                         ['content']['content'], None, self.name, self)
        # 这一部分没有完成#########################################
        # self.include:typing.List[str] = self.basicFlow.getInclude()
        # self.extend:typing.List[str] = self.basicFlow.getExtend()
        # self.generalization:typing.List[str] = self.basicFlow.getGeneralization()
        # 这一部分没有完成#########################################
        # for f in self.specificFlows:
        #     self.include += f.getInclude()
        #     self.extend += f.getExtend()
        #     self.generalization += f.getGeneralization()
        # 这一部分没有完成#########################################

    # 句子中尚未包含precondition和briefDescription
    def _get_all_sentences(self)->typing.List[Sentence]:
        sentences = []
        if self.basicFlow != None:
            sentences = self.basicFlow._get_all_sentences()
        for i in range(len(self.specificFlows)):
            sentences.extend(self.specificFlows[i]._get_all_sentences())
        return sentences

    def _get_all_steps(self)->typing.List[Step]:
        steps = []
        if self.basicFlow != None:
            steps = self.basicFlow._get_all_steps()
        for i in range(len(self.specificFlows)):
            steps.extend(self.specificFlows[i]._get_all_steps())
        return steps

    #寻找名字为flowname的Flow中是否存在第index的step，这个可能用于RFS相关的规则
    def findRFS(self, flow_name: str, index: int)->bool:
        steps = []
        flow: Flow = None
        if self.basicFlow != None:
            if self.basicFlow.name == flow_name:
                flow = self.basicFlow
                for step in flow.steps:
                    if step.index == index:
                        return True
                return False
        for i in range(len(self.specificFlows)):
            if self.specificFlows[i].name == flow_name:
                flow = self.specificFlows[i]
                for step in flow.steps:
                    if step.index == index:
                        return True
                return False
        return False
            # basic_steps:
            #     if('VALIDATES THAT' in step.keywords):
            #         return True

##########################
    # def getInclude(self)->typing.List[str]:
    #     return self.include
    #
    # def getExtend(self)->typing.List[str]:
    #     return self.extend
    #
    # def getGeneralization(self)->typing.List[str]:
    #     return self.generalization

class RUCMRoot:
    useCases: typing.List[Usecase] = []
    actors: typing.List[str] = []

    @staticmethod
    def init(rucm_dict: dict):
        model_elements = rucm_dict['root']['content']['modelElements']
        index = 0
        for me in model_elements:
            if me['type'] == 'UseCase':
                RUCMRoot.useCases.append(Usecase(me, index, None))
                index = index + 1
            elif me['type'] == 'Actor':
                RUCMRoot.actors.append(me['content']['name']['content'])
            elif me['type'] == 'Relationship':
                pass
            else:
                raise json.JSONDecodeError

    @staticmethod
    def getAllSentences()->typing.List[Sentence]:
        sentences = []
        for uc in RUCMRoot.useCases:
            sentences.extend(uc._get_all_sentences())
        return sentences

    @staticmethod
    def getAllSteps()->typing.List[Step]:
        steps = []
        for uc in RUCMRoot.useCases:
            steps.extend(uc._get_all_steps())
        return steps

    @staticmethod
    def getActors()->typing.List[str]:
        return RUCMRoot.actors

    #根据usecaseName获得UseCase
    @staticmethod
    def getUseCase(usecaseName:str)->Usecase:
        for uc in RUCMRoot.useCases:
            if uc.name == usecaseName:
                return uc
        return None


#########################测试用代码
load_dict = {}
with open("C://Python Projects//test1.rucm",'r') as load_f:
    load_dict = json.load(load_f)

r = RUCMRoot(load_dict)
s0 = RUCMRoot.getAllSentences(r)
s1 = RUCMRoot.getAllSteps(r)
u1 = r.useCases[0]
print(u1.findRFS('BB', 4))

if __name__ == "__main__":
    ## test cases
    test = [
        'I want a girl.',
        'A girl shot an elephant.',
        'You and I are a couple.',
        'You and I have and see money',
        'I shot an girl'
    ]

    for t in test:
        print(t, Sentence(t, None, None, None))
