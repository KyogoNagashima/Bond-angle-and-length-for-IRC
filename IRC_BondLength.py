#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 16:51:30 2023

@author: kyogonagashima
"""
import math
import matplotlib.pyplot as plt

count = 0
TS = -1
masterList = []
distances = []
y = []
x = []


def scanIRC():
    #variables
    global count
    global TS
    midPointReached = False
    keyFound = False
    skipLines = 0
    
    from sys import argv
    path = argv[1]
    print(path) #/Users/kyogonagashima/Desktop/Files/IRC.txt

    file = open(path, 'r')
    
    for line in file:
        line = line.strip()
        
        # Finding if midpoint is reached
        if line == 'Calculation of FORWARD path complete.':
            if not midPointReached:
                TS+=count
                midPointReached = True
        
        # Finding starting keyword
        if not keyFound:
            if line=='Input orientation:':
                skipLines = 0
                count+=1
                keyFound = True
                continue
        
        # After starting keyword is found
        else:
            if line == 'Distance matrix (angstroms):' or line.split()[0] == 'Rotational':
                keyFound = False
                continue
            else:
                if skipLines >= 2:
                    lineScan(line)
                else:
                    skipLines+=1

    file.close()    



def lineScan(line):
    global masterList
    global atom1
    global atom2
    
    from sys import argv
    atom1 = argv[2]
    atom2 = argv[3]
    
    if line =='---------------------------------------------------------------------':
        return
    
    list = line.split()
    atomNum= list[0]
    atomNum = atomNum.strip()
    x = list[3]
    y = list[4]
    z = list[5]
    
    if atomNum == atom1 or atomNum == atom2:
        masterList.append(x)
        masterList.append(y)
        masterList.append(z)

def procList():
    global masterList
    
    coordList = []
    for i in range(0, len(masterList), 1):
        if len(coordList) == 6:
            calcDist(coordList)
            #coordList.clear() #to be used it user uses python 3
            coordList = [] #compatible with python 2 but comment out if user is using python 2
        coordList.append(masterList[i])
            

def calcDist(coordList):
    x1 = float(coordList[0])
    y1 = float(coordList[1])
    z1 = float(coordList[2])
    x2 = float(coordList[3])
    y2 = float(coordList[4])
    z2 = float(coordList[5])
    
    x = x2 - x1
    y = y2 - y1
    z = z2 - z1
    
    xsq = x**2
    ysq = y**2
    zsq = z**2
    
    distance = math.sqrt(xsq+ysq+zsq)
    distances.append(distance)
    
def table():
    global y
    global x
    global distances
    
    j=0
    for i in range(len(distances)-1, TS, -1):
        j+=1
        y.append(distances[i])
        x.append(j)
        print(distances[i])
    for i in range(0, TS+1, 1):
        j+=1
        y.append(distances[i])
        x.append(j)
        print(distances[i])
    
    
def plot():
    global y
    global x
    
    plt.scatter(x, y)
    plt.show()
    

def main():
    scanIRC()
    procList()
    print('atoms: ', end = '')
    print(atom1, end = ', ')
    print(atom2)
    table()
    plot()
  

if __name__ == "__main__":
  main()









