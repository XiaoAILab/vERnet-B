"""
@author Chantal Li
@desc 从nint.ea格式生成用于深度学习的mat
@date 2021/12/10

    Input: ea_path(string), mat_path(string), variant_type(int)
    Output: null
    Retrun: 0/variant_type
"""

import os
import sys
import re
import time
import scipy.io as scio
import numpy as np
import pandas as pd

try:
    ea_path = sys.argv[1]
    mat_path = sys.argv[2]
    variant_type = int(sys.argv[3])
    if(variant_type == 1):
    # missense mutation in BRCT domain of BRCA1
        matrix = np.zeros((214,214,7))
        with open(ea_path, 'r') as fh:
            for line in fh:
                res = re.split('[ \\t]+', line)
                if(len(res) > 3):
                    Astr = res[0]
                    Bstr = res[2]
                    Intstr = res[1]
                    weight = int(res[3])
                    A = int(re.split(':', line)[1]) - 1
                    B = int(re.split(':', Bstr)[1]) - 1
                    node1 = min(A, B)
                    node2 = max(A, B)
                    
                    if(Intstr == '(cnt:mc_mc)'):
                        matrix[node1, node2, 0] = weight
                    elif(Intstr == '(cnt:sc_sc)'):
                        matrix[node2, node1, 0] = weight
                    elif(Intstr == '(cnt:mc_sc)'):
                        matrix[A, B, 1] = weight
                    elif(Intstr == '(hbond:mc_mc)'):
                        matrix[node1, node2, 2] = weight
                    elif(Intstr == '(hbond:sc_sc)'):
                        matrix[node2, node1, 2] = weight
                    elif(Intstr == '(hbond:mc_sc)'):
                        matrix[A, B, 3] = weight
                    elif(Intstr == '(ovl:mc_mc)'):
                        matrix[node1, node2, 5] = weight
                    elif(Intstr == '(ovl:sc_sc)'):
                        matrix[node2, node1, 5] = weight
                    elif(Intstr == '(ovl:mc_sc)'):
                        matrix[A, B, 6] = weight
                    elif(Intstr == '(combi:all_all)'):
                        matrix[node1, node2, 4] = weight
                    else:
                        print(line)

    scio.savemat(mat_path, {'A':matrix})
except:
    sys.exit(0)
sys.exit(variant_type)
