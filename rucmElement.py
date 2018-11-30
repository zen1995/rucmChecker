import base
import typing
import json


class RUCMBase():
    def __init__(self,useCaseName:str,parent):
        self.useCaseName:str=useCaseName
        self.parent=parent


class Word(RUCMBase):
    def __init__(self,val:str,useCaseName:str,parent,):
        super(Word,self).__init__(useCaseName,parent)
        self.val:str = val
        self.type:base.WordType =None
        self.tense :base.WordTense=None
        #parseWord

    def parseWord(self):
        pass

class Sentence(RUCMBase):
    def __init__(self,sentense:str,useCaseName:str,parent):
        super(Sentence,self).__init__(useCaseName,parent)
        self.val = sentense
        self.subjects:typing.List[Word] =[]
        self.objects:typing.List[Word] = []
        self.verbs:typing.List[Word] = []
        self.tense:base.WordTense = None
        self.words:typing.List[Word] = []



    def parseSentense(self)->bool:
        pass


class Step(RUCMBase):
    def __init__(self,index:int,step:dict,useCaseName:str,parent):
        super(Step,self).__init__(useCaseName,parent)

        self.index = index
        self.val:str = None
        self.sentences:typing.List[Sentence] = []
        self.natureType:base.NatureType = None
        self.natureContent = []#啥玩意？？？

    def parseStep(self)->bool:
        pass

class Flow(RUCMBase):
    def __init__(self,flow:dict,useCaseName:str,parent):
        super(Flow,self).__init__(useCaseName,parent)

        self.type:str=None
        self.title:str = None
        self.postCondition:Sentence = None#
        self.introduction:str = None
        self.steps:typing.List[Step] =  None
        self.include:typing.List[str] = None
        self.extend:typing.List[str] = None
        self.generalization:typing.List[str] = None

    def parseFlow(self)->bool:
        pass

    def getInclude(self)->typing.List[str]:
        return self.include

    def getExtend(self)->typing.List[str]:
        return self.extend

    def getGeneralization(self)->typing.List[str]:
        return self.generalization

class Usecase():
    counter = 0
    def __init__(self,rucm:dict):
        self.name:str = rucm['name']['content']
        self.briefDescription:str = rucm['description']['content']
        specification_content = rucm['specification']['content']
        self.postCondition:Sentence = Sentence(specification_content['basicFlow']['content']['postCondition']['content']['sentences'][0]['content']['content']['content'], self.name)
        self.basicFlow:Flow = Flow(specification_content['basicFlow'], self.name)
        self.specificFlows:typing.List[Flow] = [Flow(f, self.name) for f in specification_content['alternativeFlows']]
        self.id = self.counter
        self.counter += 1

        self.include:typing.List[str] = self.basicFlow.getInclude()
        self.extend:typing.List[str] = self.basicFlow.getExtend()
        self.generalization:typing.List[str] = self.basicFlow.getGeneralization()
        
        for f in self.specificFlows:
            self.include += f.getInclude()
            self.extend += f.getExtend()
            self.generalization += f.getGeneralization()

    def findRfs(self,flowName:str,index:int)->bool:
        pass

class RUCMRRoot:
    useCases: typing.List[Usecase] = []
    actors: typing.List[str] = []

    def __init__(self, rucm_dict:dict):
        modelElements = rucm_dict['root']['content']['modelElements'] 
        for me in modelElements:
            if me['type'] == 'UseCase':
                self.useCases.append(Usecase(me['content']))
            elif me['type'] == 'Actor':
                self.actors.append(me['content']['name']['content'])
            else:
                raise json.JSONDecodeError

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

    @staticmethod
    def getAllSentence()->typing.List[Sentence]:
        pass
