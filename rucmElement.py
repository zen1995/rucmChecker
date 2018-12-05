import base
import typing
import json
import re
from enum import Enum, unique
from nlputils import parse_sentense, parse_sentense_tense, parse_word_tense, parse_word_type


@unique
class NatureType(Enum):
    validates_that_ = 'VALIDATES THAT'
    do_ = 'DO'
    until_ = 'UNTIL'
    resume_step_ = 'RESUME STEP'
    rfs_ = 'RFS'
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
        self.useCaseName: str = use_case_name
        self.parent: RUCMBase = parent


class Word(RUCMBase):
    def __init__(self, val: str, use_case_name, parent):
        super(Word,self).__init__(use_case_name, parent)
        self.val: str = val
        self.type: base.WordType = None
        self.tense: base.WordTense = None
       # self.__parse_word()
    
    def __parse_word(self):
        self.type = base.WordTense(parse_word_tense(self.val))
        self.tense = base.WordType(parse_word_type(self.val))
    
    def __repr__(self):
        return self.val
    
    def __str__(self):
        return self.val


class Sentence(RUCMBase):

    def __init__(self, sentence: str, nature, use_case_name, parent):
        super(Sentence,self).__init__(use_case_name, parent)
        self.val = sentence
        self.subjects: typing.List[Word] = []
        self.objects: typing.List[Word] = []
        self.verbs: typing.List[Word] = []
        self.tense: base.WordTense = None
        self.words: typing.List[Word] = []
        #self.__parse_sentense()
        self.nature: str = nature
    
    def __parse_sentense(self):
        assert isinstance(self.val, str)
        self.subjects, self.verbs, self.objects = list(map(
            lambda x: list(map(
                lambda y: Word(y, self.useCaseName, self),
                x
            )),
            parse_sentense(self.val)
        ))
        self.tense = base.WordTense.factory(parse_sentense_tense(self.val))
        self.words = map(lambda x: Word(
            x, self.useCaseName, self), self.val.split())
    
    def __str__(self):
        return str({
            'subjects': self.subjects,
            'verbs': self.verbs,
            'objects': self.objects,
            'tense': self.tense
        })


class Step(RUCMBase):
    def __init__(self, step: dict, index: int, use_case_name, parent):
        super(Step,self).__init__(use_case_name, parent)
        self.index = index                                      # step的序号
        # step中的字符串，未划分之前的字符串
        self.val: str = step['content']['content']['content']
        # step中出现的句子集，包含了关键字，划分之后的结果
        self.sentences: typing.List[Sentence] = []
        # 分割step，形成sentences, keywords
        self.__parse_step()

    # 分割step成sentences，按照关键字进行划分，关键字也作为sentence存入其中，按照顺序排列
    # 例如：IF this is if THEN，   划分为['IF', 'this is if', 'THEN']
    # 对于这种情况： IFFFF AAA THEn IFB，该方法会将其划分为['IFFFF AAA THEn IFB']，
    # 只有确实是关键字以独立的方式出现的时候，才会进行划分。
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
            assert isinstance(sentence, str)
            a = keywords_dict.keys()
            if start in keywords_dict.keys():
                self.sentences.append(
                    Sentence(sentence, keywords_dict[start], self.useCaseName, self))
            else:
                self.sentences.append(
                    Sentence(sentence, None, self.useCaseName, self))
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
        super(Flow,self).__init__(use_case_name,parent)
        self.title = None
        self.introduction = None
        # 类型是'BasicFlow'或者'Specific Flow', 'Specific Flow'包含了另外三种分支流的类型
        self.type = 'BasicFlow'
        if flow['type'] != 'BasicFlow':
            self.type: str = 'Specific Flow'
        if flow['content']['name']['content'] != '':
            # 名字如果存在，则取原本的名字，如果不存在，则取type作为名字
            self.name = flow['content']['name']['content']
        else:
            self.name = self.type
        flow_content = flow['content']
        # 后置条件，是一个sentence
        self.postCondition = None
        if 'postCondition' in flow_content:
            self.postCondition: Sentence = Sentence(flow_content['postCondition']['content']
                                                ['sentences'][0]['content']['content']['content'], None, self.useCaseName, self)
        self.steps: typing.List[Step] = []
        # 建立steps
        for i in range(len(flow_content['steps'])):
            self.steps.append(
                Step(flow_content['steps'][i], i, self.useCaseName, self))
        self.RfsSentence = None                 # RFS句子
        # 如果flow是分支流的话，如果flow是specifix，代表他是来自哪个流的那个steps。例如：RFS Basic 4。
        # 在这里作为句子而存在。如果flow是 基本流 或者是 全局分支流 ，那么这一项为None。
        if self.type != 'BasicFlow' and 'rfsSentence' in flow_content:
            self.RfsSentence = Sentence(flow_content['rfsSentence']['content']['content']['content'], None, self.useCaseName, self)
        self.id = index
        # 未实现的部分
        self.include = []
        self.extend = []
        self.generalization = []

    # 获得flow中所有包含MEANWHILE关键字的step的sentences 和 不包含关键字的step的sentences
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
        self.name: str = use_case_content['name']['content']    # 名字
        super(Usecase,self).__init__(self.name, parent)
        self.id = index                                         # 设置Use Case的ID
        # 设置Use Case下的流，流的类型只分为Basic Flow和Alternative Flow。以及前置条件、简述
        self.basicFlow: Flow = None                             # Basic Flow，可能为None
        # 分支流，可能为[],实际上这里指的是alternative flow，但是由于历史原因不更改了
        self.specificFlows: typing.List[Flow] = []              # 分支流，可能为[]
        self.precondition = None                                # 前置条件，可能为None
        self.briefDescription = None                            # 简要描述，可能为None
        # specification'有可能不出现
        if 'specification' in use_case_content:
            specification_content = use_case_content['specification']['content']
            self.basicFlow = Flow(
                specification_content['basicFlow'], 0, self.name, self)
            if 'alternativeFlows' in specification_content:
                alt_content = specification_content['alternativeFlows']
                for i in range(len(alt_content)):
                    for f in specification_content['alternativeFlows']:
                        self.specificFlows.append(Flow(f, i, self.name, self))
            # 设置precondition和briefDescription
            if 'preCondition' in specification_content:
                self.preCondition = Sentence(specification_content['preCondition']['content']['sentences'][0]
                                             ['content']['content']['content'], None, self.name, self)
            if 'briefDescription' in specification_content:
                self.briefDescription = Sentence(specification_content['briefDescription']['content']['sentences'][0]
                                                 ['content']['content']['content'], None, self.name, self)

        # use case在初始化的时候会将下面这些初始化，之后，由上一级的root将这些提取出的id替换为usecase对应的name
        self.include = []
        self.extend = []
        self.generalization = None
        if 'extend' in use_case_content:
            for i, extend in enumerate(use_case_content['extend']):
                extend_use_case_id = int(re.findall('\d', extend['content']['extendedCase'])[i])
                self.extend.append(extend_use_case_id)
        if 'include' in use_case_content:
            for i, include in enumerate(use_case_content['include']):
                include_use_case_id = int(re.findall('\d', include['content']['addition'])[i])
                self.include.append(include_use_case_id)
        a = 1
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

    def __repr__(self):
        return self.name

    # 句子中不包含precondition和briefDescription
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

    def _get_all_flows(self)->typing.List[Flow]:
        flows = []
        if self.basicFlow != None:
            flows.append(self.basicFlow)
        for flow in self.specificFlows:
            flows.append(flow)
        return flows


    # 寻找名字为flowname的Flow中是否存在第index的step，这个可能用于RFS相关的规则
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
        index = 0
        model_elements = rucm_dict['root']['content']['modelElements']
        for me in model_elements:
            if me['type'] == 'UseCase':
                #将index替换为reference中的id,为了之后寻找relationship做基础
                ref_id = RUCMRoot.__get_reference_id(rucm_dict, index)
                RUCMRoot.useCases.append(Usecase(me, ref_id, None))
            elif me['type'] == 'Actor':
                RUCMRoot.actors.append(me['content']['name']['content'])
            elif me['type'] == 'Relationship':
                pass
            else:
                pass
            index = index + 1
        #设置include关系, extend关系
        for use_case in RUCMRoot.useCases:
            included_use_cases = []
            extended_use_cases = []
            for included_id in use_case.include:
                for u in RUCMRoot.useCases:
                    if u.id == included_id:
                        included_use_cases.append(u.name)
            for extende_id in use_case.extend:
                for u in RUCMRoot.useCases:
                    if u.id == extende_id:
                        extended_use_cases.append(u.name)
            #设置use_case的include、extend
            use_case.include = included_use_cases
            use_case.extend = extended_use_cases

    @staticmethod
    def getAllSentences()->typing.List[Sentence]:
        sentences = []
        for uc in RUCMRoot.useCases:
            sentences.extend(uc._get_all_sentences())
        return sentences

    #返回所有出现的流中的step
    @staticmethod
    def getAllSteps()->typing.List[Step]:
        steps = []
        for uc in RUCMRoot.useCases:
            steps.extend(uc._get_all_steps())
        return steps

    @staticmethod
    def getActors(Usecasename = None)->typing.List[str]:
        return RUCMRoot.actors

    # 根据usecaseName获得UseCase
    @staticmethod
    def getUseCase(usecaseName: str)->Usecase:
        for uc in RUCMRoot.useCases:
            if uc.name == usecaseName:
                return uc
        return None

    # 根据usecaseName获得UseCase
    @staticmethod
    def getAllFlow()->typing.List[Flow]:
        flows = []
        for uc in RUCMRoot.useCases:
            flows.extend(uc._get_all_flows())
        return flows

    # 根据模型元素中的id通过在 rucm['reference']中寻找，找到其对应的引用ID，用于判断include等
    @staticmethod
    def __get_reference_id(rucm:dict, model_element_id):
        pattern = '<root>\.modelElements\[\d\]'
        refs : dict = rucm['reference']
        for ref_id in range(len(refs)):
            ref_str = refs[ref_id]['path']
            if re.fullmatch(pattern, ref_str) != None:
                find_id = int(re.findall('\d+', ref_str)[0])
                if find_id == model_element_id:
                    return ref_id
        return None

    @staticmethod
    def __repr__():
        return str({
            'UserCases': RUCMRoot.useCases,
            'Actors': RUCMRoot.actors
        })
# #########################测试用代码
# load_dict = {}
# with open("D://java for RUCM//TEST FOR RUCM CHECKER//test1.rucm",'r') as load_f:
#     load_dict = json.load(load_f)
# RUCMRoot.init(load_dict)
# a = RUCMRoot.useCases
# s0 = RUCMRoot.getAllSentences()
# s1 = RUCMRoot.getAllSteps()


if __name__ == "__main__":
    # test cases
    # test = [
    #     'I want a girl.',
    #     'A girl shot an elephant.',
    #     'You and I are a couple.',
    #     'You and I have and see money',
    #     'I shot an girl'
    # ]
    # for t in test:
    #     print(t, Sentence(t, None, None, None))
    #########################测试用代码
    load_dict = {}
    with open(".//test1.rucm",'r') as load_f:
        load_dict = json.load(load_f)
    RUCMRoot.init(load_dict)
    a = RUCMRoot.useCases
    s0 = RUCMRoot.getAllSentences()
    s1 = RUCMRoot.getAllSteps()
    s3 = RUCMRoot.getAllFlow()
    s4 = a