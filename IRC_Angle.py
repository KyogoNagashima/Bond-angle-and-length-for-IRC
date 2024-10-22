#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:41:03 2023

@author: kyogonagashima
"""

import numpy
import matplotlib.pyplot as plt

count = 0
TS = -1
masterList = []
angles = []
y = []
x = []
a=0
b=0
c=0
k=0
j=0


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
    global atom3
    
    from sys import argv
    atom1 = argv[2]
    atom2 = argv[3]
    atom3 = argv[4]
    
    if line =='---------------------------------------------------------------------':
        return
    
    list = line.split()
    atomNum= list[0]
    atomNum = atomNum.strip()
    x = list[3]
    y = list[4]
    z = list[5]
    
    
    
    if atomNum == atom1 or atomNum == atom2 or atomNum == atom3:
        masterList.append(x)
        masterList.append(y)
        masterList.append(z)

def procList():
    global masterList
    
    coordList = []
    for i in range(0, len(masterList), 1):
        if len(coordList) == 9:
            calcAngle(coordList)
            #coordList.clear() #to be used it user uses python 3
            coordList = [] #compatible with python 2 but comment out if user is using python 2
        coordList.append(masterList[i])
            

def calcAngle(coordList):
    global a
    global b
    global c
    global k
    global j
    
    x1 = float(coordList[0])
    y1 = float(coordList[1])
    z1 = float(coordList[2])
    
    x2 = float(coordList[3])
    y2 = float(coordList[4])
    z2 = float(coordList[5])
    
    x3 = float(coordList[6])
    y3 = float(coordList[7])
    z3 = float(coordList[8])
    
    a = numpy.array([x1, y1, z1])
    b = numpy.array([x2, y2, z2])
    c = numpy.array([x3, y3, z3])
    
    k = a-b
    j = c-b
    
    m = numpy.dot(k, j, out=None)
    
    # m1 = float(k[0])*float(j[0])
    # m2 = float(k[1])*float(j[1])
    # m3 = float(k[2])*float(j[2])
    # m = m1+m2+m3
    
    lenK = numpy.sqrt(numpy.dot(k, k, out=None))
    lenJ = numpy.sqrt(numpy.dot(j, j, out=None))
    
    angle = numpy.arccos(m/(lenK*lenJ))
    
    angles.append(angle)
    
def table():
    global y
    global x
    global angles
    
    angles = numpy.rad2deg(angles)
    
    j=0
    for i in range(len(angles)-1, TS, -1):
        j+=1
        y.append(angles[i])
        x.append(j)
        print(angles[i])
    for i in range(0, TS+1, 1):
        j+=1
        y.append(angles[i])
        x.append(j)
        print(angles[i])
    
    
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
    print(atom2, end = ', ')
    print(atom3)
    table()
    plot()
  

if __name__ == "__main__":
  main()









