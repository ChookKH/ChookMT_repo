import os, sys
import csv
import pandas as pd
import numpy as np
from collections import defaultdict

class DataTable:
    def __init__(self, _EPDir, _GaitPhaseDir, _ESDir, _normSide, CI, _selES):
        self.normSide = _normSide
        self.EPDir = _EPDir
        self.ESDir = _ESDir
        self.selectData(_selES)
        self.CI = CI
        self.GaitPhaseDir = _GaitPhaseDir
        self.readGaitPhaseFile()
        self.partitionGaitPhase()

    @classmethod
    def onlyEP(cls, _EPDir, _GaitPhaseDir, _normSide, CI):
        obj = cls.__new__(cls) # Doesn't call __init__
        obj.normSide = _normSide
        obj.EPDir = _EPDir
        obj.selectData(False)
        obj.CI = CI
        obj.GaitPhaseDir = _GaitPhaseDir
        obj.readGaitPhaseFile()
        obj.partitionGaitPhase()
        return obj

    def selectData(self, selES):
        if self.normSide == "right":
            self.EPDFrame = pd.read_table("{0}\\RightNormalizedData.dat".format(self.EPDir), 
                                          sep=' ', index_col=0, low_memory=False)   
        elif self.normSide == "left":
            self.EPDFrame = pd.read_table("{0}\\LeftNormalizedData.dat".format(self.EPDir), 
                                          sep=' ', index_col=0, low_memory=False)

        if selES:
            # Selects the appropriate ES Data according to the desired normalized side
            self.selectESData_NormSide()

        # Selects the appropriate EP Mean Data according to the desired normalized side
        self.selectEPMean_NormSide()
    def selectESData_NormSide(self):
        if self.normSide == "right":
            for f in os.scandir(self.ESDir):
                if ("_affRight.dat" in f.name) or ("_unaffRight.dat" in f.name):
                    ESRight = f.name
                    self.ESDFrame = pd.read_table("{0}\\{1}".format(self.ESDir, ESRight), 
                                                  sep=' ', index_col=0)
        elif self.normSide == "left":
            for f in os.scandir(self.ESDir):
                if ("_affLeft.dat" in f.name) or ("_unaffLeft.dat" in f.name):
                    ESLeft = f.name
                    self.ESDFrame = pd.read_table("{0}\\{1}".format(self.ESDir, ESLeft), 
                                                  sep=' ', index_col=0)
    def selectEPMean_NormSide(self):
        if self.normSide == "right":
            self.EPMean = pd.read_table("{0}\\AggData_Right\\Mean.dat".format(self.EPDir), sep=' ', index_col=0)
        elif self.normSide == "left":
            self.EPMean = pd.read_table("{0}\\AggData_Left\\Mean.dat".format(self.EPDir), sep=' ', index_col=0) 


    def readGaitPhaseFile(self):
        self.GaitParDict = defaultdict(float)
        with open(self.GaitPhaseDir, mode='r') as infile:
            reader = csv.reader(infile)
            for line in reader:
                if not len(line) == 0:
                    self.GaitParDict[line[0]] = line[1]


    def partitionGaitPhase(self):
        GaitParDFIndex = [
            "Initial Contact", 
            "End of Loading Response", 
            "End of Mid Stance", 
            "End of Terminal Stance", 
            "End of Pre-Swing", 
            "End of Initial Swing", 
            "End of Mid-Swing", 
            "End of Terminal Swing"
        ]
        GaitParDFHeader = ["%time"]
        GaitParDFHeader = [*GaitParDFHeader, *self.EPMean.columns]
        headerLength    = len(GaitParDFHeader)
        # Initializing the dataframe
        self.GaitParDF = pd.DataFrame(
            data=np.zeros((8,headerLength)), 
            index=GaitParDFIndex, 
            columns=GaitParDFHeader, 
            dtype=float
        )

        # Filling the dataframe (time series)
        self.GaitParDF["%time"][0] = self.GaitParDict["1. initial contact"]
        self.GaitParDF["%time"][1] = self.GaitParDict["2. end of loading response"]
        self.GaitParDF["%time"][2] = self.GaitParDict["3. end of midstance"]
        self.GaitParDF["%time"][3] = self.GaitParDict["4. end of terminal stance"]
        self.GaitParDF["%time"][4] = self.GaitParDict["5. end of preswing"]
        self.GaitParDF["%time"][5] = self.GaitParDict["6. end of initial swing"]
        self.GaitParDF["%time"][6] = self.GaitParDict["7. end of mid swing"]
        self.GaitParDF["%time"][7] = self.GaitParDict["8. end of terminal swing"]
        # Filling the dataframe (interpolated values)
        for col in self.EPMean.columns:
            for i in range(8):
                self.GaitParDF[col][i] = self.interpolateGaitPhase(self.GaitParDF["%time"][i], self.EPMean[col])
    def interpolateGaitPhase(self, _tGait, _pdSeries):
        '''
        Given a particular time, interpolate and return the corresponding value
        '''
        # Using a binary algo to search the two neighbouring indices
        tArray = _pdSeries.index
        p1 = 0
        p2 = len(_pdSeries) - 1
        for i in range(int(len(_pdSeries)/2) + 1):
            m = int((p1+p2) / 2)
            if tArray[m] < _tGait:
                p1 = m + 1
            elif tArray[m] > _tGait:
                p2 = m - 1
            
            if p1 > p2:
                break
        
        # Interpolate and return
        dy = _pdSeries[tArray[p1]] - _pdSeries[tArray[p2]]
        dx = tArray[p1] - tArray[p2]
        val = dy/dx * (_tGait - tArray[p2]) + _pdSeries[tArray[p2]]
        return val


class DataTable_GroupSubScore:
    def __init__(self, _EPDir, _GaitPhaseDir, _ESGroupDir, _normSide, CI):
        self.normSide = _normSide
        self.EPDir = _EPDir
        self.ESGroupDir = _ESGroupDir
        self.selectData()
        self.CI = CI
        self.GaitPhaseDir = _GaitPhaseDir
        self.readGaitPhaseFile()
        self.partitionGaitPhase()

    def selectData(self):
        if self.normSide == "right":
            self.EPDFrame = pd.read_table("{0}\\RightNormalizedData.dat".format(self.EPDir), 
                                          sep=' ', index_col=0, low_memory=False)   
        elif self.normSide == "left":
            self.EPDFrame = pd.read_table("{0}\\LeftNormalizedData.dat".format(self.EPDir), 
                                          sep=' ', index_col=0, low_memory=False)
        # Selects the appropriate ES Data according to the desired normalized side
        self.selectESData_NormSide() 
        # Selects the appropriate EP Mean Data according to the desired normalized side
        self.selectEPMean_NormSide()
    
    # This method must now be expanded to scan through directories
    def selectESData_NormSide(self):
        self.ESDFrame = defaultdict()
        for patID in os.scandir(self.ESGroupDir):
            if (patID.name[0:2] == "ES") and (self.normSide == "right"):
                for patMeas in os.scandir(patID):
                    for f in os.scandir(patMeas):
                        if ("_affRight.dat" in f.name) or ("_unaffRight.dat" in f.name):
                            print(f"{f.path} is being added")
                            self.ESDFrame[f.name] = pd.read_table(f.path, sep=' ', index_col=0)
            elif (patID.name[0:2] == "ES") and (self.normSide == "left"):
                for patMeas in os.scandir(patID):
                    for f in os.scandir(patMeas):
                        if ("_affLeft.dat" in f.name) or ("_unaffLeft.dat" in f.name):
                            print(f"{f.path} is being added")
                            self.ESDFrame[f.name] = pd.read_table(f.path, sep=' ', index_col=0)

    def selectEPMean_NormSide(self):
        if self.normSide == "right":
            self.EPMean = pd.read_table("{0}\\AggData_Right\\Mean.dat".format(self.EPDir), sep=' ', index_col=0)
        elif self.normSide == "left":
            self.EPMean = pd.read_table("{0}\\AggData_Left\\Mean.dat".format(self.EPDir), sep=' ', index_col=0) 

    def readGaitPhaseFile(self):
        self.GaitParDict = defaultdict(float)
        with open(self.GaitPhaseDir, mode='r') as infile:
            reader = csv.reader(infile)
            for line in reader:
                if not len(line) == 0:
                    self.GaitParDict[line[0]] = line[1]

    def partitionGaitPhase(self):
        GaitParDFIndex = [
            "Initial Contact", 
            "End of Loading Response", 
            "End of Mid Stance", 
            "End of Terminal Stance", 
            "End of Pre-Swing", 
            "End of Initial Swing", 
            "End of Mid-Swing", 
            "End of Terminal Swing"
        ]
        GaitParDFHeader = ["%time"]
        GaitParDFHeader = [*GaitParDFHeader, *self.EPMean.columns]
        headerLength    = len(GaitParDFHeader)
        # Initializing the dataframe
        self.GaitParDF = pd.DataFrame(
            data=np.zeros((8,headerLength)), 
            index=GaitParDFIndex, 
            columns=GaitParDFHeader, 
            dtype=float
        )

        # Filling the dataframe (time series)
        self.GaitParDF["%time"][0] = self.GaitParDict["1. initial contact"]
        self.GaitParDF["%time"][1] = self.GaitParDict["2. end of loading response"]
        self.GaitParDF["%time"][2] = self.GaitParDict["3. end of midstance"]
        self.GaitParDF["%time"][3] = self.GaitParDict["4. end of terminal stance"]
        self.GaitParDF["%time"][4] = self.GaitParDict["5. end of preswing"]
        self.GaitParDF["%time"][5] = self.GaitParDict["6. end of initial swing"]
        self.GaitParDF["%time"][6] = self.GaitParDict["7. end of mid swing"]
        self.GaitParDF["%time"][7] = self.GaitParDict["8. end of terminal swing"]
        # Filling the dataframe (interpolated values)
        for col in self.EPMean.columns:
            for i in range(8):
                self.GaitParDF[col][i] = self.interpolateGaitPhase(self.GaitParDF["%time"][i], self.EPMean[col])
    def interpolateGaitPhase(self, _tGait, _pdSeries):
        '''
        Given a particular time, interpolate and return the corresponding value
        '''
        # Using a binary algo to search the two neighbouring indices
        tArray = _pdSeries.index
        p1 = 0
        p2 = len(_pdSeries) - 1
        for i in range(int(len(_pdSeries)/2) + 1):
            m = int((p1+p2) / 2)
            if tArray[m] < _tGait:
                p1 = m + 1
            elif tArray[m] > _tGait:
                p2 = m - 1
            
            if p1 > p2:
                break
        
        # Interpolate and return
        dy = _pdSeries[tArray[p1]] - _pdSeries[tArray[p2]]
        dx = tArray[p1] - tArray[p2]
        val = dy/dx * (_tGait - tArray[p2]) + _pdSeries[tArray[p2]]
        return val 


class DataTable_ESBundle:
    def __init__(self, _ESDir, _normSide, CI):
        self.normSide = _normSide
        self.ESDir = _ESDir
        self.selectData()
        self.extractDataName()
        self.createDataFrames()
        self.CI = CI

    def selectData(self):
        self.DataFileDirList = []
        for subfolder in os.scandir(self.ESDir):
            for f in os.scandir(subfolder.path):
                if self.normSide == "right":
                    if "_affRight.dat" in f.name:
                        self.DataFileDirList.append(f.path)
                    elif "_unaffRight.dat" in f.name:
                        self.DataFileDirList.append(f.path)
                elif self.normSide == "left":
                    if "_affLeft.dat" in f.name:
                        self.DataFileDirList.append(f.path)
                    elif "_unaffLeft.dat" in f.name:
                        self.DataFileDirList.append(f.path)
    
    def extractDataName(self):
        self.DataNames = []
        for dir in self.DataFileDirList:
            FileName = dir.split("\\")[-1]
            FileName = FileName.split("_")[0]
            self.DataNames.append(FileName)

    def createDataFrames(self):
        self.DataFramesList = []
        for dir in self.DataFileDirList:
            df = pd.read_table("{0}".format(dir), sep=' ', index_col=0)
            self.DataFramesList.append(df)
        
        for i in range(len(self.DataFramesList)):
            if i == 0:
                self.DataFrameAgg = self.DataFramesList[i].copy()
            else:
                self.DataFrameAgg = pd.concat([self.DataFrameAgg, self.DataFramesList[i]])
