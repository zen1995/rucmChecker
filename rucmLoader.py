import base
from rucmElement import RUCMRoot
import typing


class RucmLoader(base.Loader):
    def __init__(self, filepath: str):
        super(RucmLoader, self).__init__(filepath)
        RUCMRoot.init(self.dict_content)

    def load(self)->bool:
        super(RucmLoader, self).load()
        return True

    def __repr__(self):
        return RUCMRoot.__repr__()