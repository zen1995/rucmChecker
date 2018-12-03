import base
import typing
import abc
import rucmElement
import sys
import defaultRule

default_rules = {
    17: defaultRule.DefaultRule17(),
    18: defaultRule.DefaultRule18(),
    19: defaultRule.DefaultRule19(),
    20: defaultRule.DefaultRule20(),
    21: defaultRule.DefaultRule21(),
    22: defaultRule.DefaultRule22(),
    23: defaultRule.DefaultRule23(),
    24: defaultRule.DefaultRule24(),
    25: defaultRule.DefaultRule25(),
    26: defaultRule.DefaultRule26()
}

class RuleLoader(base.Loader):

    def __init__(self, filepath: str):
        super(RuleLoader, self).__init__(filepath)
        self.json = dict()
        self.rules = []

    def load(self)->bool:
        # load to ruleDB
        if not super(RuleLoader, self).load():
            return False
        
        if not self.checkFileFormat():
            return False

        if not self.parseDefaultRule():
            return False
        
        if 'user_def' in self.dict_content:
            for rule in self.dict_content['user_def']:
                self.parseComplexRule(rule)

        return True


    def checkFileFormat(self)->bool:
        pass

    def parseDefaultRule(self)->bool:
        try:
            if 'disabledID' in self.dict_content:
                for i in self.dict_content['disabledID']:
                    if i in default_rules:
                        default_rules[i].status = False
        
            for i in default_rules:
                RuleDB.defaultRules.append(default_rules[i])
        except Exception:
            return False
        
        return True


    def parseComplexRule(self, rule: dict)->bool:
        RuleDB.userRules.append(ComplexRule(rule))
        return True

    def parseSampleRule(self, rule: dict)->bool:
        pass


class ErrorInfo():
    def __init__(self, rulename='', usecasename='', sentence=''):
        self.rulename: str = rulename
        self.usecasename: str = usecasename
        self.sentence: str = sentence


class Reporter():
    errors: typing.List[ErrorInfo] = []
    reporter = sys.stdout

    @staticmethod
    def generateReport(filePath: str)->None:
        Reporter.reporter = open(filePath, "w", encoding="utf-8")

    @staticmethod
    def reportError(rulename='', usecasename='', sentence=''):
        Reporter.errors.append(ErrorInfo(rulename, usecasename, sentence))


class Rule():

    def __init__(self):
        self.id: int = -1
        self.description: str = None
        self.status: bool = True
        self.rtype: str = None  # rtype in ["user","system"]

    @abc.abstractmethod
    def check(self)->typing.List[ErrorInfo]:
        pass


class SimpleRule():

    def __init__(self):
        self.target: base.RuleSubject = None
        self.op = base.SimpleOp = None
        self.val: typing.List[str] = []
        self.description: str = ""

    def check(self, sentece: rucmElement.Sentence)->bool:
        pass


class ComplexRule(Rule):

    def __init__(self, ruleDict: dict):
        super(ComplexRule, self).__init__()
        self.applyScope: base.ApplyScope = None
        self.op: typing.List[base.LogicOp] = None
        self.sampleRule: typing.List[SimpleRule] = None

    def check(self)->typing.List[ErrorInfo]:
        #
        pass

    def dynamicFill(self, s: str):
        # fill list with $actor
        pass


class RuleDB():
    defaultRules: typing.List[Rule] = []
    userRules: typing.List[Rule] = []


if __name__ == "__main__":
    print('-' * 20, 'test Report', '-' * 20)
    # Reporter.generateReport('report.txt')
    Reporter.reportError('rule1', 'usecase1', 'I am kind')
    Reporter.reportError('rule2', 'usecase2', 'I am dog')
    Reporter.reportError('rule3', 'usecase3', 'I am cat')
    Reporter.reportError('rule4', 'usecase4', 'I am monkey')
    for e in Reporter.errors:
        Reporter.reporter.write(
            f"Sentence ({e.sentence}) in use case({e.usecasename}) violates the rule({e.rulename}).\n")
    print('-' * 60)
