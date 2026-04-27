# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 21:06:14 2021

@author: Xela
"""


from tqdm import tqdm

powerOf2Component = 1
for i in tqdm(range(7830457)):
   powerOf2Component *= 2
   powerOf2Component %= 1e10


powerOf2ComponentMultiplied = (powerOf2Component * 28433) % 1e10

print((powerOf2ComponentMultiplied + 1)%1e10)