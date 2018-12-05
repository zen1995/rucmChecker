import base
import typing
import abc
import defaultRule
from rule import *


class RuleLoader(base.Loader):

    def __init__(self, filepath: str):
        super(RuleLoader, self).__init__(filepath)
        self._json = self.dict_content
        self.__user_rule_id = []
        self.load()

    # 加载字典元素到RuleDB中去
    def load(self) -> bool:
        # load to ruleDB

        if self.checkFileFormat():  # 检查格式正确性
            self.parseDefaultRule(self._json['default'])  # 加载默认规则
            if 'user-def' in self._json:  # 加载用户规则
                for rule in self._json['user-def']:
                    RuleDB.userRules.append(self.parseComplexRule(rule))
            return True
        else:
            print('load Fall')
            return False

    def checkFileFormat(self) -> bool:
        # 检查默认规则格式
        if 'default' in self._json:
            default_rules = self._json['default']
            for rule in default_rules:
                # id存在性检查
                if 'id' not in rule:
                    print('Default Rule id lost')
                    return False
                # id 范围检查
                if rule['id'] not in range(27):
                    print('Default Rule id lost')
                    return False
                # 具体检查每一条默认规则
                if rule['id'] <= 16:
                    if not self.__checkComplexRule(rule):
                        return False
                elif rule['id'] > 16:
                    if not self.__checkAttribute(rule, 'status', [True, False]):
                        return False
        # 检查用户规则格式
        checked_id = []
        if 'user-def' in self._json:
            for rule in self._json['user-def']:
                # 具体检查每一条用户规则
                if not self.__checkComplexRule(rule):
                    return False
                # 检查id是否重复
                a = rule['id']
                if rule['id'] in checked_id:
                    return False
                checked_id.append(rule['id'])
        return True

    # 提取默认规则到规则库，返回处理结果
    def parseDefaultRule(self, default_rules) -> bool:
        for rule in default_rules:
            # 添加默认规则。如果规则id < 16，则它是以复杂规则表示的，否则是其他种类的规则，
            if rule['id'] <= 16:
                RuleDB.defaultRules.append(self.parseComplexRule(rule))
            else:
                if rule['id'] == 17 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule17())
                elif rule['id'] == 18 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule18())
                elif rule['id'] == 19 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule19())
                elif rule['id'] == 20 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule20())
                elif rule['id'] == 21 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule21())
                elif rule['id'] == 22 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule22())
                elif rule['id'] == 23 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule23())
                elif rule['id'] == 24 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule24())
                elif rule['id'] == 25 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule25())
                elif rule['id'] == 26 and rule['status'] == True:
                    RuleDB.defaultRules.append(defaultRule.DefaultRule26())

    # 提取复杂规则，返回复杂规则
    def parseComplexRule(self, rule: dict):
        complex_rule = ComplexRule(rule)
        complex_rule.id = rule['id']  # 设置id
        complex_rule.status = rule['status']  # 设置status
        # 设置作用域
        if rule['applyScope'] == 'actionStep':
            complex_rule.applyScope = base.ApplyScope.actionStep
        elif rule['applyScope'] == 'allSentence':
            complex_rule.applyScope = base.ApplyScope.allSentence
        # 添加simple_rule
        for simple_rule in rule['simpleRules']:
            complex_rule.simpleRule.append(self.parseSimpleRule(simple_rule))
        complex_rule.description = None
        # 添加opration到op
        for op in rule['operation']:
            if op == '-':
                op = base.LogicOp.skip_
            elif op == '!':
                op = base.LogicOp.not_
            elif op == '&':
                op = base.LogicOp.and_
            elif op == '|':
                op = base.LogicOp.or_
            complex_rule.op.append(op)
        return complex_rule

    # 提取简单规则，返回简单规则
    def parseSimpleRule(self, rule: dict):
        simple_rule = SimpleRule()
        # 设置target
        if rule['subject'] == 'subject_Val':
            simple_rule.target = base.RuleSubject.subject_Val
        elif rule['subject'] == 'object_Val':
            simple_rule.target = base.RuleSubject.object_Val
        elif rule['subject'] == 'verb_count':
            simple_rule.target = base.RuleSubject.verb_count
        elif rule['subject'] == 'verb_tense':
            simple_rule.target = base.RuleSubject.verb_tense
        elif rule['subject'] == 'str_':
            simple_rule.target = base.RuleSubject.str_
        elif rule['subject'] == 'strs':
            simple_rule.target = base.RuleSubject.strs
        elif rule['subject'] == 'subject_count':
            simple_rule.target = base.RuleSubject.subject_count
        elif rule['subject'] == 'object_count':
            simple_rule.target = base.RuleSubject.object_count
        elif rule['subject'] == 'participlePhrases_count':
            simple_rule.target = base.RuleSubject.participlePhrases_count

        # 设置operation
        if rule['operation'] == 'in':
            simple_rule.op = base.SimpleOp.in_
        elif rule['operation'] == 'notIn':
            simple_rule.op = base.SimpleOp.notin_
        simple_rule.description = None
        # 设置取值范围
        simple_rule.val = rule['val']
        return simple_rule

    # 检查复杂规则正确性
    def __checkComplexRule(self, rule: dict) -> bool:
        # id存在
        if(not self.__checkAttribute(rule, 'id', [])):
            print('ComplexRule id Wrong')
            return False
        # status存在，且status在[True, False]内
        if(not self.__checkAttribute(rule, 'status', [True, False])):
            print('ComplexRule id %d: status Wrong' % rule['id'])
            return False
        # applyScope存在，且applyScope在ApplyScope规定的取值内
        if (not self.__checkAttribute(rule, 'applyScope', base.ApplyScope.__members__.keys())):
            print('ComplexRule id %d: applyScope Wrong' % rule['id'])
            return False
        # operation存在，且operation为['|', '-', '&', '!']四种之一
        if ('operation' not in rule):
            print('ComplexRule id %d: don not habe operation' % rule['id'])
            return False
        else:
            for op in rule['operation']:
                if op not in ['|', '-', '&', '!']:
                    print('ComplexRule id %d: operation Wrong' % rule['id'])
                    return False

        # 检查每条simpleRule是否符合规范
        for i, simple_rule in enumerate(rule['simpleRules']):
            if(not self.__checkSimpleRule(simple_rule)):
                print('ComplexRule id %d SimpleRule id %d: operation Wrong' %
                      (rule['id'], i))
                return False
        return True

    def __checkSimpleRule(self, rule: dict) -> bool:
        # subject存在，且subject在RuleSubject规定的取值内
        if(not self.__checkAttribute(rule, 'subject', base.RuleSubject.__members__.keys())):
            print('SimpleRule subject Wrong')
            return False
        # operation存在，operation取值范围为 ['in', 'notIn']
        if (not self.__checkAttribute(rule, 'operation', ['in', 'notIn'])):
            print('SimpleRule operation Wrong')
            return False
        return True

    def __checkAttribute(self, rule, attribute: str, scope) -> bool:
        if attribute not in rule:
            return False
        else:
            if len(scope) != 0:
                if rule[attribute] not in scope:
                    return False
        return True

    def __repr__(self):
        return str({
            'default rules': RuleDB.defaultRules,
            'userRules': RuleDB.userRules
        })


class RuleDB():
    defaultRules: typing.List[Rule] = []
    userRules: typing.List[Rule] = []


# import json
# load_dict = {}
# with open("C://Users//FS//Desktop//rule//rule-template.txt",'r') as load_f:
#     load_dict = json.load(load_f)
# a = RuleLoader(load_dict)
# b = RuleDB.defaultRules
# c = RuleDB.userRules
# d = 0
