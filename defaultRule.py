import rule
import base
import re
import rucmElement
class DefaultRule17(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            sentences = step.sentences
            if sentences[0].nature == base.NatureType.include_usecase_:
                #判断后续语句是否在UseCase的Include字段
                if sentences[1] not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).include:
                    errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))                     
        rule.Reporter.errors += errors

class DefaultRule18(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            sentences = step.sentences
            if sentences[0].nature == base.NatureType.extend_by_usecase_:
                #判断后续语句是否在UseCase的Extend字段
                if sentences[1] not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).extend:
                    errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
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
                    # 规则格式不正确
                    errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                    continue
                if endNum:
                    # 有横杠
                    startNum = int(resNum.group(1))
                    endNum = int(resNum.group(2)[1:])
                    if startNum < endNum:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))
                        continue
                    nums += range(startNum, endNum+1)
                else:
                    # 没横杠
                    nums.append(int(resNum.group(1)))
            for num in nums:
                if not flow.parent.findRfs(flowName, num):
                    errors.append(rule.ErrorInfo(self.description, flow.usecasename, rfs))                
        rule.Reporter.errors += errors

class DefaultRule20(rule.Rule):
    pass

class DefaultRule21(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            # 得到MEANWHILE的index
            i = -1
            for i in range(len(step.sentences)):
                if step.sentences[i].NatureType == base.NatureType.meanwhile_:
                    return
            if i < 0:
                continue
            if i == 0 or i == len(step.sentences):
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule22(rule.Rule):
     def check(self, steps):
        errors = []
        for step in steps:
            # 得到VALIDATES THAT的index
            for i in range(len(step.sentences)):
                if step.sentences[i].NatureType == base.NatureType.validates_that_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if i == 0 or i == len(step.sentences)-1:
                # 前后必须有东西
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule23(rule.Rule):
    def check(self, flows):
        errors = []
        for flow in flows:
            doInd = -1
            untilInd = -1
            for stepInd, step in enumerate(flow.steps):
                # 找do
                doI = -1
                untilI = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].NatureType == base.NatureType.do_:
                        doInd = stepInd
                        doI = i
                    if step.sentences[i].NatureType == base.NatureType.until_:
                        untilInd = stepInd
                        untilI = i
                # 找到do
                if doI >= 0:
                    # do占一个step
                    if len(step.sentences) != 1:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, step.val))
                if untilI >= 0:
                    # until必须在开头，until后面必须有东西, until前必须已触发do
                    if untilI != 0 or len(step.sentences) == 1 or doInd < 0:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, step.val))
            if doInd >= 0 and untilInd < 0:
                # 出现do，没有出现until
                errors.append(rule.ErrorInfo(self.description, flow.usecasename, step.val))
        rule.Reporter.errors += errors
   

class DefaultRule24(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            # 得到ABORT的index
            for i in range(len(step.sentences)):
                if step.sentences[i].NatureType == base.NatureType.validates_that_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if len(step.sentences) != 1:
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule25(rule.Rule):
    def check(self, steps):
        errors = []
        for step in steps:
            # 得到RESUME的index
            for i in range(len(step.sentences)):
                if step.sentences[i].NatureType == base.NatureType.resume_step_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if len(step.sentences) != 2 or i != 0:
                # 找到了，判断RESUME在不在开头，后面是不是只跟了一个序号
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                continue
            try:
                # 判断第二个数是不是序号
                num = int(step.sentences[1])
            except:
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                continue
            if not step.parent.type == 'Specific Flow' or \
            not rucmElement.RUCMRoot.getUseCase(step.usecaseName).findRFS(rucmElement.RUCMRoot.getUseCase(step.usecaseName).basicFlow.title, num):
                # 对应的flow是不是alternative，对应的step在不在basic flow中
                errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
        rule.Reporter.errors += errors 
class DefaultRule26(rule.Rule):
    def check(self, flows):
        errors = []
        for flow in flows:
            if not flow.postcondition:
                errors.append(rule.ErrorInfo(self.description, flow.usecasename, flow.title))
        rule.Reporter.errors += errors 

