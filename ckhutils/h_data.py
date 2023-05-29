import pandas as pd
import os, io, zipfile, sys

class healthy_data:

    def __init__(self):
           
        # Obtaining healthy gait event durations, parameters and phases
        self.gait_eve, self.gait_par, self.gait_pha = self.initialize_hData()

    def initialize_hData(self):
        '''
        Extract healthy gait event durations, parameter and phases
        '''
        # Read .dat file
        current_dir = os.getcwd()
        newRefband = os.path.join(
            current_dir, '..', 'refBand', 
            'RefBand_GaitPE_repTrials_n1.dat'
        )

        with open(newRefband, mode='r') as file:
            h_data = file.read()

        # Classify into phase duration, parameters and phases
        h_df = pd.read_csv(io.StringIO(h_data), sep=' ')
        h_df = h_df.rename(columns={'Unnamed: 0': 'Measure'})

        gait_events = h_df.iloc[:6, :]
        gait_parameters = h_df.iloc[6:18, :]
        gait_phases = h_df.iloc[18:, :]

        return gait_events, gait_parameters, gait_phases
    

    def intialize_hKinematics(self, fileName):
        '''
        Extract kinematic data of healthy subjects 
        '''
        # Connect current directory to zip file location
        zip_path = os.path.join(os.pardir, 'testSubjectsCollective.zip')

        # Read .dat files and assign headers
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for filename in zip_ref.namelist():
                if filename.endswith('.dat') and filename == fileName:
                    with zip_ref.open(filename) as file:
                        for line in file:
                            kineDF = pd.read_csv(file, sep=' ', index_col=0, header=None)   
                            kineDF.index.name = 'Stats'

                            # For InCnt.dat
                            if kineDF.shape[1] == 1:
                                kineDF.columns = ['Measurement']

                            # For the remaining .dat files
                            if kineDF.shape[1] == 3:    
                                kineDF.columns = ['Min', 'Median', 'Max']

                            return(kineDF)
                        

    def unravel(self, dataFrame):
        '''
        Unravel the 3 min, median and max columns into 1 column
        '''
        # Reset the indexing
        dataFrame.reset_index(inplace=True)

        # Split the column names using '__' as a seperator
        dataFrame.columns = dataFrame.columns.str.split('__', expand=True)

        # Stack the df from columns to rows
        dataFrame = dataFrame.set_index('OriIndex').stack().reset_index()

        # Merge 
        dataFrame['OriIndex'] = dataFrame['OriIndex'] + '__' + dataFrame['level_1']
        dataFrame = dataFrame.rename(columns={0: 'Status'})[['OriIndex', 'Status']].set_index('OriIndex') 

        return dataFrame
    
    def export_data(self, subFolder, datFileName, dataframe):
        '''
        Export data into subfolders according to stride pair id
        '''
        # Get the current working directory
        currentDir = os.getcwd()

        # Go one level up to the parent directory
        parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))

        if sys.argv[3] == 'std':

            # Specify the path to the ckhExportedData folder
            exportedDir = os.path.join(parentDir, 'ckhExportedDataSTD')

            # Creating subfolder name
            subfolderName = subFolder

            # Create the subfolder within the exportedData directory
            subfolder_path = os.path.join(exportedDir, subfolderName)
            if os.path.isdir(subfolder_path):
                pass
            else:
                os.makedirs(subfolder_path)

            # Specify the file name and path within the subfolder
            file_name = datFileName
            file_path = os.path.join(subfolder_path, file_name)

            # Save DataFrame as .dat file
            dataframe.to_csv(file_path, sep=' ', index=True)

        if sys.argv[3] == 'ci':

            # Specify the path to the ckhExportedData folder
            exportedDir = os.path.join(parentDir, 'ckhExportedDataCI')

            # Creating subfolder name
            subfolderName = subFolder

            # Create the subfolder within the exportedData directory
            subfolder_path = os.path.join(exportedDir, subfolderName)
            if os.path.isdir(subfolder_path):
                pass
            else:
                os.makedirs(subfolder_path)

            # Specify the file name and path within the subfolder
            file_name = datFileName
            file_path = os.path.join(subfolder_path, file_name)

            # Save DataFrame as .dat file
            dataframe.to_csv(file_path, sep=' ', index=True)