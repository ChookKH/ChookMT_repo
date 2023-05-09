import pandas as pd
import os,io

class healthy_data:

    def __init__(self):
           
        # Obtaining healthy gait event durations, parameters and phases
        self.gait_eve, self.gait_par, self.gait_pha = self.initialize_hData()

    def initialize_hData(self):
        '''
        Extract healthy gait event durations, parameter and phases
        '''
        # Read .dat file
        cwd = os.getcwd()
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