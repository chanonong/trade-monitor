from enum import Enum
import json

class Repr:
    def reprJSON(self):
        d = dict()
        for a, v in self.__dict__.items():
            if (isinstance(v, list)):
                d[a] = [_.reprJSON() if hasattr(_, "reprJSON") else _ for _ in v]
            elif (isinstance(v, Enum)):
                d[a] = v.value
            elif (hasattr(v, "reprJSON")):
                d[a] = v.reprJSON()
            else:
                d[a] = v
        return d
    
    def __repr__(self) -> str:
        return json.dumps(self.reprJSON(), indent=2)

class NoRepr:
    def reprJSON(self):
        return "MASKED"

    def __repr__(self) -> str:
        return "MASKED"