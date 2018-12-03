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
    def check(self, flows):
        errors = []
        valid_pre = []
        valid = []
        for flow in flows:
            # 在每个flow范围内进行规则检测
            for step in flow.steps:
                natureI = {}
                natureI['if'] = -1
                natureI['else'] = -1
                natureI['elseif'] = -1
                natureI['then'] = -1
                natureI['endif'] = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].NatureType == base.NatureType.if_:
                        # 向状态转移栈添加一个元素
                        # 状态转移：接受THEN
                        natureI['if'] = i
                        stackIfNum += 1
                        stackThenNum += 1
                        valid_pre.append(['IF'])
                        valid.append(['THEN'])
                    elif step.sentences[i].NatureType == base.NatureType.else_:
                        # 状态转移：接受END IF
                        natureI['else'] = i
                        if not 'ELSE' in valid[len(valid_pre)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                            continue
                        valid_pre.append(valid.pop())
                        valid.append(['END IF'])
                    elif step.sentences[i].NatureType == base.NatureType.elseif_:
                        # 状态转移：接受THEN
                        natureI['elseif'] = i
                        if not 'ELSE IF' in valid[len(valid_pre)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                            continue
                        valid_pre.append(valid.pop())
                        valid.append(['THEN'])
                    elif step.sentences[i].NatureType == base.NatureType.then_:
                        # 状态转移：如果THEN对应IF，接受ELSE/ELSE IF/END IF
                        # 如果THEN对应ELSE IF，接受END IF
                        # 否则……蜜汁转移出错？
                        natureI['then'] = i
                        if not 'THEN' in valid[len(valid_pre)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                            continue
                        if 'IF' in valid_pre.pop():
                            valid_pre.append(valid.pop())
                            valid.append(['ELSE', 'ELSE IF', 'END IF'])
                        elif 'ELSE IF' in valid_pre.pop():
                            valid_pre.append(valid.pop())
                            valid.append(['END IF'])
                        else:
                            errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                            continue
                    elif step.sentences[i].NatureType == base.NatureType.endif_:
                        # 无状态转移，从状态转移栈移除一个元素
                        natureI['endif'] = i
                        if not 'END IF' in valid[len(valid_pre)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                            continue
                        valid_pre.pop()
                        valid.pop()
                    # IF必须开头
                    if natureI['if'] > 0 or natureI['elseif'] > 0 or natureI['else'] > 0:
                        errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                        continue
                    # THEN必须结尾
                    if natureI['then'] >= 0 and natureI['then'] != len(step.sentences)-1:
                        errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                        continue
                    if natureI['endif'] >= 0 and len(step.sentences) != 1:
                        # 独占一行
                        errors.append(rule.ErrorInfo(self.description, step.usecasename, step.val))
                        continue
                    
            # 正常的话，valid为空
        if valid:
            errors.append(rule.ErrorInfo(self.description, flow.usecasename, flow.title))
                    
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
            # 前后必须有东西
            if i == 0 or i == len(step.sentences)-1:
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
            # doNum:维护的栈的数量，遇到do++,遇到until--
            doNum = 0
            for stepInd, step in enumerate(flow.steps):
                # 找do
                doI = -1
                untilI = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].NatureType == base.NatureType.do_:
                        doI = i
                    if step.sentences[i].NatureType == base.NatureType.until_:
                        untilI = i
                # 找到do
                if doI >= 0:
                    # do占一个step
                    doNum+=1
                    if len(step.sentences) != 1:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, step.val))
                        continue
                    
                if untilI >= 0:
                    # until必须在开头，until后面必须有东西, until前必须已触发do
                    doNum -= 1
                    if untilI != 0 or len(step.sentences) == 1 or doNum == 0:
                        errors.append(rule.ErrorInfo(self.description, flow.usecasename, step.val))
                        continue
            if doNum != 0:
                # do和until的数量不匹配
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
                # 独占一行
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

