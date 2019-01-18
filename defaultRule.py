import rule
import base
import re
import rucmElement
class DefaultRule17(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�INCLUDE USE CASE��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.include_use_case_:
                    break
            if i == len(step.sentences):
                continue
            # ���뿪ͷ�������ҽ���һ��USE CASE
            if i != 0 or len(step.sentences) != 2:
                errors.append(rule.ErrorInfo(self.description+'AAA', step.useCaseName, step.val))
                continue
            if step.sentences[1].val not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).include:
                # print(rucmElement.RUCMRoot.getUseCase(step.useCaseName).include)
                errors.append(rule.ErrorInfo(self.description+'BBB', step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule18(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�EXTENDED USE CASE��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.extened_by_usecase_:
                    break
            if i == len(step.sentences):
                continue
            # ���뿪ͷ�������ҽ���һ��USE CASE
            if i != 0 or len(step.sentences) != 2:
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            if step.sentences[1].val not in rucmElement.RUCMRoot.getUseCase(step.useCaseName).extend:
                # print(rucmElement.RUCMRoot.getUseCase(step.useCaseName).extend)
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
                    # �����ʽ����ȷ
                    errors.append(rule.ErrorInfo(self.description+'bbb', flow.useCaseName, rfs))
                    continue
                startNum = resNum.group(1)
                endNum = resNum.group(2)
                if endNum:
                    # �к��
                    endNum = endNum[1:]
                    startNum = int(startNum)
                    endNum = int(endNum)
                    if startNum >= endNum:
                        errors.append(rule.ErrorInfo(self.description+'ccc', flow.useCaseName, rfs))
                        continue
                    nums += range(startNum, endNum+1)
                else:
                    # û���
                    nums.append(int(resNum.group(1)))
            for num in nums:
                print(flowName)
                if not flow.parent.findRFS(flowName.replace(' ',''), num):
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
            # ��ÿ��flow��Χ�ڽ��й�����
            for step in flow.steps:
                natureI = {}
                natureI['if'] = -1
                natureI['else'] = -1
                natureI['elseif'] = -1
                natureI['then'] = -1
                natureI['endif'] = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].nature == base.NatureType.if_:
                        # ��״̬ת��ջ���һ��Ԫ��
                        # ״̬ת�ƣ�����THEN
                        natureI['if'] = i
                        #stackIfNum += 1
                        #stackThenNum += 1
                        valid_pre.append(['IF'])
                        valid.append(['THEN'])
                    elif step.sentences[i].nature == base.NatureType.else_:
                        # ״̬ת�ƣ�����END IF
                        # û����״̬

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
                        # ״̬ת�ƣ�����THEN
                        natureI['elseif'] = i
                        # û����״̬
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
                        # ״̬ת�ƣ����THEN��ӦIF������ELSE/ELSE IF/END IF
                        # ���THEN��ӦELSE IF������END IF
                        # ���򡭡���֭ת�Ƴ���
                        natureI['then'] = i
                        # û����״̬
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
                        # ��״̬ת�ƣ���״̬ת��ջ�Ƴ�һ��Ԫ��
                        # û����״̬
                        if not valid:
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        natureI['endif'] = i
                        if not 'END IF' in valid[len(valid)-1] :
                            errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                            continue
                        valid_pre.pop()
                        valid.pop()
                        
                    # IF���뿪ͷ
                    if natureI['if'] > 0 or natureI['elseif'] > 0 or natureI['else'] > 0:
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                    # THEN�����β
                    if natureI['then'] >= 0 and natureI['then'] != len(step.sentences)-1:
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                    if natureI['endif'] >= 0 and len(step.sentences) != 1:
                        # ��ռһ��
                        errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                        continue
                
            # �����Ļ���validΪ��
        if len(valid):
            errors.append(rule.ErrorInfo(self.description, flow.useCaseName, flow.title))
        rule.Reporter.errors += errors

                    
class DefaultRule21(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�MEANWHILE��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.mean_while_:
                    break
            if i == len(step.sentences):
                continue
            # ǰ������ж���
            if i == 0 or i == len(step.sentences)-1:
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule22(rule.Rule):
     def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�VALIDATES THAT��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.validates_that_:
                    break
            if i == len(step.sentences):
                # û��
                continue
            if i == 0 or i == len(step.sentences)-1:
                # ǰ������ж���
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule23(rule.Rule):
    def check(self):
        flows = rucmElement.RUCMRoot.getAllFlows()
        errors = []
        for flow in flows:
            # doNum:ά����ջ������������do++,����until--
            doNum = 0
            for stepInd, step in enumerate(flow.steps):
                # ��do
                doI = -1
                untilI = -1
                for i in range(len(step.sentences)):
                    if step.sentences[i].nature == base.NatureType.do_:
                        doI = i
                    if step.sentences[i].nature == base.NatureType.until_:
                        untilI = i
                # �ҵ�do
                if doI >= 0:
                    # doռһ��step
                    doNum+=1
                    if len(step.sentences) != 1:
                        errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
                        continue
                    
                if untilI >= 0:
                    # until�����ڿ�ͷ��until��������ж���, untilǰ�����Ѵ���do
                    if untilI != 0 or len(step.sentences) == 1 or doNum == 0:
                        errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
                        continue
                    doNum -= 1
            if doNum != 0:
                # do��until��������ƥ��
                errors.append(rule.ErrorInfo(self.description, flow.useCaseName, step.val))
        rule.Reporter.errors += errors
   

class DefaultRule24(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�ABORT��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.abort_:
                    break
            if i == len(step.sentences):
                # û��
                continue
            if len(step.sentences) != 1:
                # ��ռһ��
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val)) 
        rule.Reporter.errors += errors 

class DefaultRule25(rule.Rule):
    def check(self):
        steps = rucmElement.RUCMRoot.getAllSteps()
        errors = []
        for step in steps:
            # �õ�RESUME��index
            for i in range(len(step.sentences)+1):
                if i == len(step.sentences):
                    break
                if step.sentences[i].nature == base.NatureType.resume_step_:
                    break
            if i == len(step.sentences):
                # û��
                continue
            if len(step.sentences) != 2 or i != 0:
                # �ҵ��ˣ��ж�RESUME�ڲ��ڿ�ͷ�������ǲ���ֻ����һ�����
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            try:
                # �жϵڶ������ǲ������
                num = int(step.sentences[1].val)
            except Exception as e:
                print(e)
                errors.append(rule.ErrorInfo(self.description, step.useCaseName, step.val))
                continue
            if not step.parent.type == 'Specific Flow' or \
            not rucmElement.RUCMRoot.getUseCase(step.useCaseName).findRFS(rucmElement.RUCMRoot.getUseCase(step.useCaseName).basicFlow.title, num):
                # ��Ӧ��flow�ǲ���alternative����Ӧ��step�ڲ���basic flow��
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

