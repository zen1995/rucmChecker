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
        target = []
        if self.target == base.RuleSubject.subject_Val:
            wds = sentence.subjects
            for word in wds:
                target.append(word.val)
        elif self.target == base.RuleSubject.object_Val:
            wds = sentence.objects
            for word in wds:
                target.append(word.val)
        elif self.target == base.RuleSubject.verb_count:
            target.append(len(sentence.verbs))
        elif self.target == base.RuleSubject.verb_tense:
            target.append(sentence.tense.value)
        elif self.target == base.RuleSubject.strs:
            # print(sentence.words)
            target = [word.val for word in sentence.words]
        elif self.target == base.RuleSubject.subject_count:
            target.append(len(sentence.subjects))
        elif self.target == base.RuleSubject.object_count:
            target.append(len(sentence.objects))
        elif self.target == base.RuleSubject.participlePhrases_count:
            target.append(sentence.participle_count)
        elif self.target == base.RuleSubject.adverb_count:
            target.append(sentence.adverb_count)
        elif self.target == base.RuleSubject.modal_verb_count:
            target.append(sentence.modal_verb_count)
        elif self.target == base.RuleSubject.pronoun_count:
            target.append(sentence.pronoun_count)
        elif self.target == base.RuleSubject.sentence_tense:
            target.append(sentence.tense.value)
        else:
            assert False,self.target
        # print(sentence.val, target, value, self.target)
        if self.op == base.SimpleOp.in_:
            if not target:
                return False
            return all(x in value for x in target)
        else:
            if not target:
                return False
            return all(x not in value for x in target)

    def dynamicFill(self, useCaseName: str):
        # fill list with $actor
        # checked right
        value = []
        if '$actor' in self.val:
            value = [x for x in self.val if x != '$actor']
            value += rucmElement.RUCMRoot.getActors(useCaseName)
        else:
            value = self.val
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
                nature = None
                for sentence in step.sentences:
                    # print('to be checked', sentence)
                    # print(sentence.nature)
                    if sentence.nature:
                        nature = sentence.nature
                if nature and nature != base.NatureType.mean_while_:
                    continue
                sentences = step.sentences
                for sentence in sentences:
                    if sentence.nature:
                        continue
                    checkResult = []
                    
                    for rule in self.simpleRule:
                        checkResult.append(rule.check(sentence))
                    result = checkResult[0]
                    for i in range(len(checkResult) - 1):
                        op = self.op[i + 1]
                        assert (op == base.LogicOp.and_ or op == base.LogicOp.or_)
                        if op == base.LogicOp.and_:
                            result = result and checkResult[i+1]
                        elif op == base.LogicOp.or_:
                            result = result or checkResult[i+1]
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
                if sentence.nature:
                    continue
                for rule in self.simpleRule:
                    checkResult.append(rule.check(sentence))
                result = checkResult[0]
                # print(result)
                for i in range(len(checkResult) - 1):
                    op = self.op[i + 1]
                    assert (op == base.LogicOp.and_ or op == base.LogicOp.or_)
                    if op == base.LogicOp.and_:
                        result = result and checkResult[i+1]
                    elif op == base.LogicOp.or_:
                        result = result or checkResult[i+1]
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