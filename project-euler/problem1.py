# -*- coding: utf-8 -*-
"""
Created on Tue May 25 16:21:25 2021

@author: Xela
"""


multiples = [i for i in range(1000) if (i%3==0) or (i%5==0)]
out = sum(multiples)