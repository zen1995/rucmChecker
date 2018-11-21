import base
import typing
import abc
import rucmElement
class SampleRule:
    def __init__(self,subject:base.RuleSubject,op:str,val:list):
        self.subject=None
        self.op = None
        self.val = []

    def check(self)->bool:
        pass


class RuleLoader(base.Loader):

    def __init__(self,filepath:str):
        super(RuleLoader,self).__init__(filepath)
        self.json = dict()
        self.rules = []
    def load(self)->bool:
        #load to ruleDB
        pass

    def checkFileFormat(self)->bool:
        pass


    def parseDefaultRule(self)->bool:
        pass

    def parseComplexRule(self,rule:dict)->bool:
        pass

    def parseSampleRule(self,rule:dict)->bool:
        pass


class ErrorInfo:
    def __init__(self):
        self.rulename:str=None
        self.usecasename:str=None
        self.sentence:str=None

class Reporter():
    errors:typing.List[ErrorInfo]=[]
    @staticmethod
    def generateReport(filePath:str)->None:
        pass

class Rule():

    def __init__(self):
        self.id:int=-1
        self.description:str = None
        self.status:bool=True
        self.rtype:str=None#rtype in ["user","system"]
    @abc.abstractmethod
    def check(self)->typing.List[ErrorInfo]:
        pass

class SimpleRule():

    def __init__(self):
        self.target:base.RuleSubject=None
        self.op = base.SimpleOp=None
        self.val:typing.List[str]=[]
        self.description:str=""

    def check(self,sentece:rucmElement.Sentence)->bool:
        pass


class ComplexRule(Rule):

    def __init__(self,ruleDict:dict):
        super(ComplexRule,self).__init__()
        self.applyScope:base.ApplyScope=None
        self.op:typing.List[base.LogicOp]=None
        self.sampleRule:typing.List[SampleRule]=None

    def check(self)->typing.List[ErrorInfo]:
        #
        pass


class RuleDB():
    defaultRules:typing.List[Rule]=[]
    userRules:typing.List[Rule]=[]