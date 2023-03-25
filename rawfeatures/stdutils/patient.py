import os
import pandas as pd
from pathlib import Path

class Patient:
    '''
    Class to represent an individual patient
    '''
    def __init__(self, ID, _metadata):
        # The patient's ID
        self.ID = ID

        # The WalkMode describes if the patient is walking barefooted, wearing shoes or
        # using a walking cane
        self.WalkTool = _metadata[0]

        # Patient's affected side
        self.AffectedSide = _metadata[1]

        # All trials
        self.Trials = []
        self.nTotalTrials = len(self.Trials)

        # Unclean trials
        self.UncleanTrials = []
        self.nUncleanTrials = len(self.UncleanTrials)

        # Clean trials
        self.CleanTrials = []
        self.nCleanTrials = self.nTotalTrials - self.nUncleanTrials


    def __str__(self):
        '''
        Print key properties
        '''
        trialslist = ""
        for t in self.Trials:
            trialslist += f" - {t}"
            if t in self.UncleanTrials:
                trialslist += " (faulty)"
            trialslist += "\n"

        return(
            f"ID: {self.ID}\n" +
            f"WalkTool: {self.WalkTool}\n" +
            f"AffectedSide: {self.AffectedSide}\n"
            f"Trials:\n" +
            trialslist
        )


    def updateTrialCount(self):
        '''
        Method to update the trials (total, unclean and clean)
        '''
        self.nTotalTrials = len(self.Trials)
        self.nUncleanTrials = len(self.UncleanTrials)
        self.nCleanTrials = self.nTotalTrials - self.nUncleanTrials

        # Resetting the CleanTrials and then repopulating it if needed
        self.CleanTrials = []

        for trial in self.Trials:
            # If trial is not corrupted and not yet in the valid list, then add it to CleanTrials
            if not trial in self.UncleanTrials:
                if not trial in self.CleanTrials:
                    self.CleanTrials.append(trial)
            # Else just do nothing, since the trial has already been added to UncleanTrials


    def appendTrial(self, _dataName):
        '''Adds _dataName to the Trials and updates the data count'''
        self.Trials.append(_dataName)
        self.updateTrialCount()


    def appendUncleanTrial(self, _dataName):
        '''Adds _dataName to the UncleanTrials and updates the data count'''
        self.UncleanTrials.append(_dataName)
        self.updateTrialCount()


class Trial:
    '''
    Class to handle each trial
    '''
    def __init__(self, _trialID, FolderPath, _metadata):
        # Folder name with patientID + measurement number
        self.TrialID = _trialID
        self.FolderPath = FolderPath
        self.WalkTool = _metadata[0]

        # Affected side
        self.AffectedSide = _metadata[1]

        # Right stride normalized data
        self.KinematicsR = []
        self.GaitEventsR = []
        self.GaitParametersR = []

        # Left stride normalized data
        self.KinematicsL = []
        self.GaitEventsL = []
        self.GaitParametersL = []


    def __str__(self):
        '''
        Print key properties
        '''
        out = (
            f"TrialID: {self.TrialID}\n" +
            f"FolderPath: {self.FolderPath}\n" +
            f"WalkTool: {self.WalkTool}\n" +
            f"AffectedSide: {self.AffectedSide}\n"
        )

        out += "KinematicsR:\n"
        for f in self.KinematicsR:
            f = (Path(f)).name
            out += f" - {f}\n"

        out += "GaitEventsR:\n"
        for f in self.GaitEventsR:
            f = (Path(f)).name
            out += f" - {f}\n"

        out += "GaitParametersR:\n"
        for f in self.GaitParametersR:
            f = (Path(f)).name
            out += f" - {f}\n"

        out += "KinematicsL:\n"
        for f in self.KinematicsL:
            f = (Path(f)).name
            out += f" - {f}\n"

        out += "GaitEventsL:\n"
        for f in self.GaitEventsL:
            f = (Path(f)).name
            out += f" - {f}\n"

        out += "GaitParametersL:\n"
        for f in self.GaitParametersL:
            f = (Path(f)).name
            out += f" - {f}\n"

        return out


    def checkIfTrialIsValid(self):
        '''
        Check if the non-faulty exported trial gait data is sufficient
        to be considered for further analysis
        '''
        validTrial = True

        if (len(self.KinematicsR) == 0 or len(self.KinematicsL) == 0):
            validTrial = False

        if validTrial:
            if (len(self.GaitParametersR) == 0 or len(self.GaitParametersL) == 0):
                validTrial = False

        if validTrial:
            if (len(self.GaitEventsR) == 0 or len(self.GaitEventsL) == 0):
                validTrial = False

        return validTrial


    def cleanProperties(self):
        '''
        Method to clean all the lists
        '''
        # Right stride normalized data
        self.KinematicsR = []
        self.GaitEventsR = []
        self.GaitParametersR = []

        # Left stride normalized data
        self.KinematicsL = []
        self.GaitEventsL = []
        self.GaitParametersL = []


    def getData(self, _listOfCorruptedFiles, folderPath=None):
        '''
        Going through each folder and assigning the appropriate path to each of the obj
        properties

        Update 06.08.2021: Multiple strides per trial
        (Example: ES001BB1969a-B-3Gang18_01_<typeOfFile.dat>)
        '''
        if folderPath is None:
            subFolderContents = [f for f in os.scandir(self.FolderPath)]
        else:
            subFolderContents = [f for f in os.scandir(folderPath)]

        for content in subFolderContents:

            if not content.name in _listOfCorruptedFiles:
                if "_" in content.name:

                    underScoreSeparator = [idx for idx, c in enumerate(content.name) if c=="_"][-1]

                    # === === === ===
                    # Gait events
                    if content.name[underScoreSeparator:] == "_eventsLeftNorm.dat":
                        self.GaitEventsL.append(content.path)
                    elif content.name[underScoreSeparator:] == "_eventsRightNorm.dat":
                        self.GaitEventsR.append(content.path)

                    # === === === ===
                    # Patients and test subjects kinematics
                    elif (
                            (content.name[underScoreSeparator:] == "_affLeft.dat") or
                            (content.name[underScoreSeparator:] == "_unaffLeft.dat")
                    ):
                        self.KinematicsL.append(content.path)
                    elif (
                            (content.name[underScoreSeparator:] == "_affRight.dat") or
                            (content.name[underScoreSeparator:] == "_unaffRight.dat")
                    ):
                        self.KinematicsR.append(content.path)

                    elif content.name[underScoreSeparator:] == "_noneLeft.dat":
                        self.KinematicsL.append(content.path)
                    elif content.name[underScoreSeparator:] == "_noneRight.dat":
                        self.KinematicsR.append(content.path)

                    # === === === ===
                    # Gait parameters
                    elif content.name[underScoreSeparator:] == "_gaitParametersLeftNorm.dat":
                        self.GaitParametersL.append(content.path)
                    elif content.name[underScoreSeparator:] == "_gaitParametersRightNorm.dat":
                        self.GaitParametersR.append(content.path)

                else:
                    pass

            else:
                print(f"Faulty :: {content.name}")


    def __getstate__(self):
        '''
        Copy the object's state from self.__dict__ which contains all our instance attributes.
        Always use the dict.copy() method to avoid modifying the original state.

        Every attribute is saved except for the dataframes
        '''
        state = self.__dict__.copy()

        return state


    def __setstate__(self, state):
        '''
        Restore instance attributes
        '''
        self.__dict__.update(state)

