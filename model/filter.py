
import os
import re
from PIL import Image
import cv2
import matplotlib.pyplot as plt

import pandas
import numpy as np

requests = []

def filterData(logs):
    with logs as fin:
        for line in fin:
            actual = re.findall(r'"(.*)$', line)
            requests.append(actual)
    return requests


def saveData(filteredLogs):
    clearData = []
    injectionLogs = []
    with open('/Users/greycr0w/Development/flare-wtf-model/train.csv', mode='wt', encoding='utf-8') as myfile:
        for log in filteredLogs:
            strLog = re.findall(r'^(.*?) (.*?) (.*)$', str(log))
            myfile.write(str(strLog[0][1]).replace(",", "") + ", 1" + '\n')
            print("|" + str(strLog[0][1]))
            clearData.append(strLog[0][1])
        print(clearData[0])
        return clearData


def createImagesFromHttp(savePath, dataPath):

    data = open(dataPath)
    fileToSave = open(savePath, mode='wt', encoding='utf-8')
    vectors = []
    allVectors = []
    with data as fin:
        print('line')
        for line in data:
            print('data')
            print(line)
            for c in line:
                vectors.append(ord(c))

            allVectors.append(vectors)
            vectors = []

    print(len(allVectors))

    for elem in allVectors:
        fileToSave.write(str(elem) + '\n')
    return allVectors




    # print(vectors)
    # npvector = np.array(vectors)
    # img = cv2.imread("/Users/greycr0w/Development/flare-wtf-model/injectionImages.txt", 0)
    # print(npvector)
    # pass

def retFilter(path):
    data = open(path, mode='r', encoding='utf-8')
    fileToWrite = open("/Users/greycr0w/Development/flare-wtf-model/filteredData.csv", mode="w")

    with data as fin:
        for line in data:
            print(line)
            data = line.replace('"', "")
            fileToWrite.write(data)

    pass
def main():
    logs = open('website.access.log')
    filteredLogs = filterData(logs)
    clearData = saveData(filteredLogs)
    retFilter("/Users/greycr0w/Development/flare-wtf-model/train.csv")



    # images = createImagesFromHttp("/Users/greycr0w/Development/flare-wtf-model/injectionImages.txt", "/Users/greycr0w/Development/flare-wtf-model/injectionHTTPs.txt")

#
main()
