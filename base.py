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
    def load(self)->bool:
        #所有的load结果均存到静态类中，返回值是是否解析成功
        self.dict_content = json.loads(self.filepath)


class RuleSubject(enum.Enum):
    subject_Val='subject_Val'
    object_Val='object_Val'
    verb_count='verb_count'
    verb_tense='verb_tense'
    #str_="str_"
    strs='strs'
    subject_count='subject_count'
    object_count='object_count'
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
    #add more?

class NatureType(enum.Enum):
    pass
    #to add
    #!!

