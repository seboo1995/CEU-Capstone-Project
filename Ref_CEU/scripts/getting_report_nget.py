#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 17:37:00 2020

@author: sebair
"""


from tabula import read_pdf
import os

file_paths = "../data/reports_from_nget/op_cost.csv"
### NEED TO FIND A WAY TO READ THE REPORTS, BUT FOR NOW I WILL READ THEM 
### MANUALLY. There is a csv file

import pandas as pd

def get_op_cost():


df = pd.read_csv(file_paths)