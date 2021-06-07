try:
    from .ArticutAPI import Articut
    from .Toolkit.analyse import AnalyseManager
    from .Toolkit.localRE import TaiwanAddressAnalizer
    from .Toolkit.toolkits import *
    from .Toolkit.NER import GenericNER
except:
    from ArticutAPI import Articut
    from Toolkit.analyse import AnalyseManager
    from Toolkit.localRE import TaiwanAddressAnalizer
    from Toolkit.toolkits import *
    from Toolkit.NER import GenericNER
