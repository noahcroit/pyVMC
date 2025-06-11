# -*- coding: utf-8 -*-

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # This is 'your_project_root/'
sys.path.insert(0, parent_dir)

import vmc
