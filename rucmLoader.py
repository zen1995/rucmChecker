import base
from rucmElement import RUCMRRoot
import typing

class RucmLoader(base.Loader):
    def __init__(self,filepath:str):
        super(RucmLoader,self).__init__(filepath)
        self.rucm_root = self.load()

    def load(self):
        super(RucmLoader,self).load()
        return RUCMRRoot(self.dict_content)

