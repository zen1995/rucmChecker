import rule
import base
import re
import rucmElement
class DefaultRule17(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到INCLUDE USE CASE的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.include_use_case_:
                    break
            if i == len(step.sentences):
                continue
            # 必须开头，后有且仅有一个USE CASE
            if i != 0 or len(step.sentences) != 2:
                errors.append(rule.ErrorInfo(self.description+'AAA', step.useCaseName, step.val))
                continue
            if step.sentences[1].val not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).include:
                print(rucmElement.RUCMRoot.getUseCase(step.useCaseName).include)
                errors.append(rule.ErrorInfo(self.description+'BBB', step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule18(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到EXTENDED USE CASE的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.extened_by_usecase_:
                    break
            if i == len(step.sentences):
                continue
            # 必须开头，后有且仅有一个USE CASE
            if i != 0 or len(step.sentences) != 2:
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            if step.sentences[1].val not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).extend:
                print(rucmElement.RUCMRoot.getUseCase(step.useCaseName).extend)
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors

class DefaultRule19(rule.Rule):
    def check(self):
        flows = rucmElement.RUCMRoot.getAllFlows()
        errors = []
        for flow in flows:
            if flow.type == 'BasicFlow' or flow.type == 'Global Alternative Flow':
                continue
            rfs = flow.RfsSentence
            res = re.search(r'(RFS )(\D+ )(\d.*)', rfs)
            if not res:
                errors.append(rule.ErrorInfo(self.description+'aaa', flow.useCaseName, rfs))
                continue
            flowName = res.group(2).rstrip(' ')
            _str = res.group(3).replace(' ', '')
            stepNums = _str.split(',')
            nums = []
            for stepNum in stepNums:
                resNum = re.fullmatch(r'(\d+)(-\d+)?( )?', stepNum)
                if not resNum:
                    # 规则格式不正确
                    errors.append(rule.ErrorInfo(self.description+'bbb', flow.useCaseName, rfs))
                    continue
                startNum = resNum.group(1)
                endNum = resNum.group(2)
                if endNum:
                    # 有横杠
                    endNum = endNum[1:]
                    startNum = int(startNum)
                    endNum = int(endNum)
                    if startNum >= endNum:
                        errors.append(rule.ErrorInfo(self.description+'ccc', flow.useCaseName, rfs))
                        continue
                    nums += range(startNum, endNum+1)
                else:
                    # 没横杠
                    nums.append(int(resNum.group(1)))
            for num in nums:
                if not flow.parent.findRFS(flowName, num):
                    errors.append(rule.ErrorInfo(self.description+'ddd', flow.useCaseName, rfs))
                    break                
        rule.Reporter.errors += errors

class DefaultRule20(rule.Rule):
    def check(self):
        flows = rucmElement.RUCMRoot.getAllFlows()
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
                    if step.sentences[i].nature == base.NatureType.if_:
                        # 向状态转移栈添加一个元素
                        # 状态转移：接受THEN
                        natureI['if'] = i
                        #stackIfNum += 1
                        #stackThenNum += 1
                        valid_pre.append(['IF'])
                        valid.append(['THEN'])
                    elif step.sentences[i].nature == base.NatureType.else_:
                        # 状态转移：接受END IF
                        # 没进入状态

                        if not valid:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        natureI['else'] = i
                        if not 'ELSE' in valid[len(valid_pre)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        valid_pre.pop()
                        valid_pre.append(valid.pop())
                        valid.append(['END IF'])
                    elif step.sentences[i].nature == base.NatureType.elseif_:
                        # 状态转移：接受THEN
                        natureI['elseif'] = i
                        # 没进入状态
                        if not valid:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        if not 'ELSE IF' in valid[len(valid)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        valid_pre.pop()
                        valid_pre.append(valid.pop())
                        valid.append(['THEN'])
                    elif step.sentences[i].nature == base.NatureType.then_:
                        # 状态转移：如果THEN对应IF，接受ELSE/ELSE IF/END IF
                        # 如果THEN对应ELSE IF，接受END IF
                        # 否则……蜜汁转移出错？
                        natureI['then'] = i
                        # 没进入状态
                        if not valid:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        if not 'THEN' in valid[len(valid)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        v_pre = valid_pre.pop()
                        if 'IF' in v_pre:
                            valid_pre.append(valid.pop())
                            valid.append(['ELSE', 'ELSE IF', 'END IF'])
                        elif 'ELSE IF' in v_pre:
                            valid_pre.append(valid.pop())
                            valid.append(['END IF'])
                        else:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        
                    elif step.sentences[i].nature == base.NatureType.endif_:
                        # 无状态转移，从状态转移栈移除一个元素
                        # 没进入状态
                        if not valid:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        natureI['endif'] = i
                        if not 'END IF' in valid[len(valid)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        valid_pre.pop()
                        valid.pop()
                        
                    # IF必须开头
                    if natureI['if'] > 0 or natureI['elseif'] > 0 or natureI['else'] > 0:
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                    # THEN必须结尾
                    if natureI['then'] >= 0 and natureI['then'] != len(step.sentences)-1:
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                    if natureI['endif'] >= 0 and len(step.sentences) != 1:
                        # 独占一行
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                
            # 正常的话，valid为空
        if len(valid):
            errors.append(rule.ErrorInfo(self.description, flow.useCaseName, flow.title))
        rule.Reporter.errors += errors

                    
class DefaultRule21(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到MEANWHILE的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.mean_while_:
                    break
            if i == len(step.sentences):
                continue
            # 前后必须有东西
            if i == 0 or i == len(step.sentences)-1:
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule22(rule.Rule):
     def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到VALIDATES THAT的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.validates_that_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if i == 0 or i == len(step.sentences)-1:
                # 前后必须有东西
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule23(rule.Rule):
    def check(self):
        flows = rucmElement.RUCMRoot.getAllFlows()
        errors = []
        for flow in flows:
            # doNum:维护的栈的数量，遇到do++,遇到until--
            doNum = 0
            for stepInd, step in enumerate(flow.steps):
                # 找do
                doI = -1
                untilI = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].nature == base.NatureType.do_:
                        doI = i
                    if step.sentences[i].nature == base.NatureType.until_:
                        untilI = i
                # 找到do
                if doI >= 0:
                    # do占一个step
                    doNum+=1
                    if len(step.sentences) != 1:
                        errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
                        continue
                    
                if untilI >= 0:
                    # until必须在开头，until后面必须有东西, until前必须已触发do
                    if untilI != 0 or len(step.sentences) == 1 or doNum == 0:
                        errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
                        continue
                    doNum -= 1
            if doNum != 0:
                # do和until的数量不匹配
                errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
        rule.Reporter.errors += errors
   

class DefaultRule24(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到ABORT的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.abort_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if len(step.sentences) != 1:
                # 独占一行
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule25(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # 得到RESUME的index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.resume_step_:
                    break
            if i == len(step.sentences):
                # 没有
                continue
            if len(step.sentences) != 2 or i != 0:
                # 找到了，判断RESUME在不在开头，后面是不是只跟了一个序号
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            try:
                # 判断第二个数是不是序号
                num = int(step.sentences[1].val)
            except Exception as e:
                print(e)
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            if not step.parent.type == 'Specific Flow' or \
            not rucmElement.RUCMRoot.getUseCase(step.useCaseName).findRFS(rucmElement.RUCMRoot.getUseCase(step.useCaseName).basicFlow.title, num):
                # 对应的flow是不是alternative，对应的step在不在basic flow中
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
        rule.Reporter.errors += errors 
class DefaultRule26(rule.Rule):
    def check(self):
        flows = rucmElement.RUCMRoot.getAllFlows()
        errors = []
        for flow in flows:
            if not flow.postCondition:
                errors.append(rule.ErrorInfo(self.description, flow.useCaseName, flow.title))
        rule.Reporter.errors += errors 

