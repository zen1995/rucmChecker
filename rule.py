import base
import typing
import abc
import rucmElement
import defaultRule
from reporter import ErrorInfo, Reporter


class Rule():

    def __init__(self):
        self.id: int = -1
        self.description: str = None
        self.status: bool = True
        self.rtype: str = None  # rtype in ["user","system"]

    @abc.abstractmethod
    def check(self) -> typing.List[ErrorInfo]:
        pass

    def __repr__(self):
        return str({
            'id': self.id,
            'description': self.description,
            'status': self.status
        })


class SimpleRule():

    def __init__(self):
        self.target: base.RuleSubject = None
        self.op : base.SimpleOp = None
        self.val: typing.List[str] = []
        self.description: str = ""

    def check(self, sentence: rucmElement.Sentence) -> bool:
        value = self.dynamicFill(sentence.useCaseName)
        if self.target == base.RuleSubject.subject_Val:
            target = sentence.subjects
        elif self.target == base.RuleSubject.object_Val:
            target = sentence.objects
        elif self.target == base.RuleSubject.verb_count:
            target = len(sentence.verbs)
        elif self.target == base.RuleSubject.verb_tense:
            target = sentence.tense
        elif self.target == base.RuleSubject.strs:
            target = [word.val for word in sentence.words]
        elif self.target == base.RuleSubject.subject_count:
            target = len(sentence.subjects)
        elif self.target == base.RuleSubject.object_count:
            target = len(sentence.objects)
        else:
            assert False,self.target
        if not isinstance(target,list):target = [target]

        if self.op == base.SimpleOp.in_:
            print(target,self.op,self.target,self.val,sentence.val,value)
            return all(x in value for x in target)
        else:
            return all(x not in value for x in target)

    def dynamicFill(self, useCaseName: str):
        # fill list with $actor
        value = []
        if '$actor' in self.val:
            value = [x for x in self.val if x != '$actor']
            value += rucmElement.RUCMRoot.getActors(useCaseName)#to do 
        return value


class ComplexRule(Rule):

    def __init__(self, ruleDict: dict):
        super(ComplexRule, self).__init__()
        self.applyScope: base.ApplyScope = None
        self.op: typing.List[base.LogicOp] = []
        self.simpleRule: typing.List[SimpleRule] = []

    def check(self) -> None:
        errors = []
        if self.applyScope == base.ApplyScope.actionStep:
            steps = rucmElement.RUCMRoot.getAllSteps()
            for step in steps:
                sentences = step.sentences
                for sentence in sentences:
                    if sentence.nature:
                        continue
                    checkResult = []
                    result = True
                    
                    for rule in self.simpleRule:
                        checkResult.append(rule.check(sentence))
                    for i in range(len(checkResult) - 1):
                        op = self.op[i + 1]
                        assert (op == base.LogicOp.and_ or op == base.LogicOp.or_)
                        if op == base.LogicOp.and_:
                            result = result and checkResult[i]
                        elif op == base.LogicOp.or_:
                            result = result or checkResult[i]
                    op = self.op[0]
                    assert (op == base.LogicOp.not_ or op == base.LogicOp.skip_)
                    if op == base.LogicOp.not_:
                        result = not result
                    if not result:
                        errors.append(ErrorInfo(self.description, \
                                                sentence.useCaseName, sentence))

        elif self.applyScope == base.ApplyScope.allSentence:
            sentences = rucmElement.RUCMRoot.getAllSentences()
            for sentence in sentences:
                checkResult = []
                result = True
                if sentence.nature:
                    continue
                for rule in self.simpleRule:
                    checkResult.append(rule.check(sentence))
                    for i in range(len(checkResult) - 1):
                        op = self.op[i + 1]
                        assert (op == base.LogicOp.and_ or op == base.LogicOp.or_)
                        if op == base.LogicOp.and_:
                            result = result and checkResult[i]
                        elif op == base.LogicOp.or_:
                            result = result or checkResult[i]
                    op = self.op[0]
                    assert (op == base.LogicOp.not_ or op == base.LogicOp.skip_)
                    if op == base.LogicOp.not_:
                        result = not result
                    if not result:
                        errors.append(ErrorInfo(self.description, \
                                                sentence.useCaseName, sentence))
        Reporter.errors += errors

class RuleDB():
    defaultRules:typing.List[Rule]=[]
    userRules:typing.List[Rule]=[]