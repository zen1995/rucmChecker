from abc import abstractclassmethod,ABCMeta,abstractmethod
import enum
import os
import typing
import errno
import json


class Loader():

    def __init__(self,filepath:str):
        self.filepath = filepath

    @abstractmethod
    def load(self):
        self.dict_content = json.loads(self.filepath)


class RuleSubject(enum.Enum):
    # 判断句子主语
    subject_Val='subject_Val'
    # 判断句子宾语
    object_Val='object_Val'
    # 判断句子动词数量
    verb_count='verb_count'
    # 判断句子动词时态
    verb_tense='verb_tense'
    # 判断所有的词
    strs='strs'
    # 判断主语数量
    subject_count='subject_count'
    # 判断宾语数量
    object_count='object_count'
    # 判断分词短语的数量
    participlePhrases_count='participlePhrases_count'

class SimpleOp(enum.Enum):
    in_="in"
    notin_="notin"

class LogicOp(enum.Enum):
    skip_="skip"
    not_="not_"
    and_="and_"
    or_="or_"

class ApplyScope(enum.Enum):
    actionStep="actionStep"
    allSentence="allSentence"


class WordTense(enum.Enum):
    past="past"
    present="present"
    future="future"
    none="none"

class WordType(enum.Enum):
    noun="noun"
    adj="adj"
    verb="verb"
    #add more?

class NatureType(enum.Enum):
    pass
    #to add
    #!!

