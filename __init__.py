#-*- coding:utf-8 -*-
import sys
from .data import *

__version__ = '0.1.3'
__all__ = ['AssemblyDataReader']
sys.modules['AssemblyDataReader'] = data.AssemblyDataReader