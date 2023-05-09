import pandas as pd
import os
import io

cwd = os.getcwd()

current_dir = os.getcwd()
newRefband = os.path.join(
    current_dir, '..', 'refBand', 'RefBand_GaitPE_repTrials_n1.dat'
)

with open(newRefband, mode='r') as file:
            h_data = file.read()

# read file
h_df = pd.read_csv(io.StringIO(h_data), sep=' ')
h_df = h_df.rename(columns={'Unnamed: 0': ''})

gait_phase_duration = h_df.iloc[:6, :]
gait_parameters = h_df.iloc[6:18, :]
gait_parameters = gait_parameters.rename(columns={gait_parameters.columns[0]: 'Measure'})
gait_parameters = gait_parameters.set_index('Measure')
print(gait_parameters)
gait_phases = h_df.iloc[18:, :]

series_data = {'gaitSpeedAff': 0.919874, 'stepTimeAff': 0.480000, 'cadenceAff': 2.030450,
               'strideTimeAff': 0.985000, 'sSupportPortionAff': 0.350254, 'singleSupportTimeAff': 0.345000,
               'dSupportPortionAff': 0.299492, 'doubleSupportTimeAff': 0.295000, 'limpIdxAff': 1.020260,
               'StepFactorAff': 0.557138, 'StrideFactorAff': 1.053577, 'StepWidthAff': 0.830002}

s = pd.Series(series_data)

s.index = ['gaitSpeed', 'stepTime', 'cadence', 'strideTime', 'sSupportPortion',
            'singleSupportTime', 'dSupportPortion', 'doubleSupportTime', 'limpIdx',
            'StepFactor', 'StrideFactor', 'StepWidth']

s_df = s.to_frame().rename(columns={0: 'Stats'})
print(s_df)

sd_df = pd.DataFrame(((gait_parameters['Lower-S.D'] <= s_df['Stats']) & (s_df['Stats'] <= gait_parameters['Upper-S.D'])).astype(int), columns=['S.D'])
ci_df =pd.DataFrame(((gait_parameters['Upper-CI'] <= s_df['Stats']) & (s_df['Stats'] <= gait_parameters['Upper-CI'])).astype(int), columns=['CI'])
merged_df = pd.merge(sd_df, ci_df, on='Measure')
not_df = ~merged_df.astype(bool)
not_df = not_df.astype(int)
print(not_df)

