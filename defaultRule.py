import rule
import base
import re
import rucmElement
class DefaultRule17(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            sentences = step.sentences
            for sentence in sentences:
                if sentence.nature == base.NatureType.include_usecase_:
                    #判断后续语句是否在UseCase的Include字段
                    res = re.search('(INCLUDE USE CASE )(.*)', sentence.val)
                    if not res.group(2) in rucmElement.getUseCase(step.useCaseName).include:
                        errors.append(rule.ErrorInfo(self.description, sentence.usecasename, sentence))
        rule.Reporter.errors += errors

class DefaultRule18(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            sentences = step.sentences
            for sentence in sentences:
                if sentence.nature == base.NatureType.extend_by_usecase_:
                    #判断后续语句是否在UseCase的Extend字段
                    res = re.search('(EXTENDED BY USE CASE )(.*)', sentence.val)
                    if not res.group(2) in rucmElement.getUseCase(step.useCaseName).extend:
                        errors.append(rule.ErrorInfo(self.description, sentence.usecasename, sentence))
        rule.Reporter.errors += errors

class DefaultRule19(rule.Rule):
    def check(self, flows):
        errors = []
        for flow in flows:
            rfs = flow.RfsSemtence
            res = re.search('(RFS )(\D+ )(\d.*)', rfs)
            if not res:
                errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                continue
            flowName = res.group(2)
            _str = res.group(3).remove(' ')
            stepNums = _str.split(',')
            nums = []
            for stepNum in stepNums:
                resNum = re.fullmatch('(\d+)(-\d+)?', stepNum)
                if not resNum:
                    errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                    continue
                if not endNum:
                    startNum = int(resNum.group(1))
                    endNum = int(resNum.group(2)[1:])
                    if startNum < endNum:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                        continue
                    nums += range(startNum, endNum+1)
                else:
                    nums.append(int(resNum.group(1)))
            for num in nums:
                if not flow.parent.findRfs(flowName, num):
                    errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                
        rule.Reporter.errors += errors

class DefaultRule20(rule.Rule):
    def check(self, flows):
        pass

class DefaultRule21(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps：
            sentences = step.sentences
            for sentence in sentences:
                if sentence.nature == base.NatureType.meanwhile_:
                    res = re.fullmatch('.+MEANWHILE.+', sentence.val)
                    if not res:
                       errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
        rule.Reporter.errors += errors 


class DefaultRule22(rule.Rule):
    pass

class DefaultRule23(rule.Rule):
    pass

class DefaultRule24(rule.Rule):
    pass

class DefaultRule25(rule.Rule):
    pass

class DefaultRule26(rule.Rule):
    pass


