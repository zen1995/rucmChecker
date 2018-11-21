from abc import abstractclassmethod,ABCMeta,abstractmethod
import enum
import os
import typing


class Loader():

    def __init__(self,filepath:str):
        self.filepath = filepath

    @abstractmethod
    def load(self)->bool:
        pass

    def fileExist(self)->bool:
        return os.path.exists(self.filepath)

    @abstractmethod
    def checkFileFormat(self)->bool:
        pass


class RuleSubject(enum.Enum):
    subject_Val='subject_Val'
    object_Val='object_Val'
    verb_count='verb_count'
    verb_tense='verb_tense'
    str_="str_"
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

class WordType(enum.Enum):
    noun="noun"
    adj="adj"
    verb="verb"
    #add more?

class NatureType(enum.Enum):
    pass
    #to add
    #!!

