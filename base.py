from abc import abstractclassmethod,ABCMeta,abstractmethod
import enum
import os
import typing
import errno
import json


class Loader():

    def __init__(self,filepath:str):
        self.filepath = filepath
        self.dict_content = json.load(open(self.filepath, 'r'))

    @abstractmethod
    def load(self)->bool:
        #所有的load结果均存到静态类中，返回值是是否解析成功
        try:
            self.dict_content = json.loads(self.filepath)
        except Exception as e:
            return False
        return True


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

    @staticmethod
    def factory(string):
        if string == "past":
            return WordTense.past
        if string == "present":
            return WordTense.present
        if string == "future":
            return WordTense.future
        return WordTense.none

class WordType(enum.Enum):
    noun="noun"
    adj="adj"
    verb="verb"
    none="none" # other type
    #add more?

from rucmElement import NatureType as NatureType

