import base
import typing

class Word():
    def __init__(self,val:str):
        self.val:str = val
        self.type:base.WordType =None
        self.tense :base.WordTense=None
        #parseWord

    def parseWord(self):
        pass

class Sentence():
    def __init__(self,sentense:str,useCaseName:str):
        self.val = sentense
        self.subjects:typing.List[Word] =[]
        self.objects:typing.List[Word] = []
        self.verbs:typing.List[Word] = []
        self.tense:base.WordTense = None
        self.words:typing.List[Word] = []
        self.useCaseName = useCaseName



    def parseSentense(self)->bool:
        pass


class Step():
    def __init__(self,index:int,step:dict):
        self.index = index
        self.val:str = None
        self.sentences:typing.List[Sentence] = []
        self.natureType:base.NatureType = None
        self.natureContent = []#啥玩意？？？

    def parseStep(self)->bool:
        pass

class Flow():
    def __init__(self,flow:dict,usecaseNmae:str):
        self.type:str=None
        self.title:str = None
        self.postCondition:Sentence = None#
        self.useCaseName:str = usecaseNmae
        self.introduction:str = None
        self.steps:typing.List[Step] =  None

    def parseFlow(self)->bool:
        pass

class Usecase():
    def __init__(self,rucm:dict):
        self.name:str = None
        self.briefDescription:str = None
        self.postCondition:Sentence = None
        self.include:typing.List[str] = None
        self.extend:typing.List[str] = None
        self.generalization:typing.List[str] = None
        self.basicFlow:Flow = None
        self.specificFlows:typing.List[Flow] = None
        self.id = -1#???

    def findRfs(self,flowName:str,index:int)->bool:
        pass

class RUCMRRoot:
    useCases: typing.List[Usecase] = []
    actors: typing.List[str] = []



    # @classmethod
    # def instance(cls, *args, **kwargs):
    #     if not hasattr(RUCMRRoot, "_instance"):
    #         RUCMRRoot._instance = RUCMRRoot(*args, **kwargs)
    #     return RUCMRRoot._instance

    @staticmethod
    def getActors()->typing.List[str]:
        pass

    @staticmethod
    def getAllSteps()->typing.List[Step]:
        pass

    @staticmethod
    def getAllFLows()->typing.List[Flow]:#啥时候用来着？？？
        pass

    @staticmethod
    def getUsecase(usecaseName:str)->Usecase:
        pass


