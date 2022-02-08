# from .local import *  # local mode
from .deploy import *  # deploy mode

"""
local mode <-> deploy mode 스위치 때 수정해야할 곳

1.
myapi/settings/__init__.py 
# from .local import *  # local mode
from .deploy import *  # deploy mode

2.
dailypathapp/utils.py
# from myapi.settings.local import *
from myapi.settings.deploy import *
"""
