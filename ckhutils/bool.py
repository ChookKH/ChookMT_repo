import os, io
import pandas as pd

def bool_output(seriesAff):
    '''
    Function to compare a healthy gait series with the gait series from subject
    '''
    h_gait = pd.read_excel('healthy_gait.xlsx')
    h_gait_series = h_gait.set_index('Gait Parameter')['Computed Mean']
    h_gait_series = h_gait_series.rename_axis(None)
    seriesAff.index = seriesAff.index.str.split('Aff').str[0]
    result = (h_gait_series >= seriesAff).astype(float)

    # print(result)


# === === === ===
# Update 29.03.2023
# -----------------
# Create path to .dat file
current_dir = os.getcwd()
gEventsMedian = os.path.join(current_dir, '..', 'refBand', 'gEventsMedian.dat')

# Read healthy subject .dat file
with open(gEventsMedian, mode='r') as file:
    h_data = file.read()

# Read df and calculate mean
h_df = pd.read_csv(io.StringIO(h_data), sep=' ')
h_df = h_df.assign(MeanNorm=(h_df['LeftNorm'] + h_df['RightNorm'])/2)
h_df = h_df.drop(['LeftNorm', 'RightNorm'], axis=1)

# Converting df to series
h_df = h_df.rename(columns={'Unnamed: 0': ''})
h_string = h_df.to_string(header=False, index=False)
h_dict = {line.split()[0]: float(line.split()[1]) for line in h_string.split('\n')}
h_series = pd.Series(h_dict)
h_series = h_series/100
print(h_series)

# Display gait width
gaitWidth = h_series.diff().dropna()
gaitWidth.index = ['LdRspWidth', 'MdStnWidth', 'TrStnWidth', 'PrSwgWidth', 
                   'InSwgWidth', 'MdSwgWidth', 'TrSwgWidth']
gaitWidth.loc['StrideWidth'] = gaitWidth.iloc[:].sum()
gaitWidth.loc['StanceWidth'] = gaitWidth.iloc[:4].sum()
gaitWidth.loc['SwingWidth'] = gaitWidth.iloc[4:7].sum()
print(gaitWidth)

def h_subject_gait(_phaseStart, _phaseEnd):
    '''
    Function to classify healthy subject gait width and gait start percentage
    '''
    h_metadata = pd.Series({}, dtype=float)

    # Entire stride
    if _phaseStart == "initialContact" and _phaseEnd == "endOfTerminalSwing":
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[7],
                "GaitStart_Aff": h_series[0],
                "GaitWidth_UnAff": gaitWidth[7],
                "GaitStart_UnAff": h_series[0]
            }
        )

    # Stance phase
    if _phaseStart == 'initialContact' and _phaseEnd == 'endOfPreSwing':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[8],
                "GaitStart_Aff": h_series[0],
                "GaitWidth_UnAff": gaitWidth[8],
                "GaitStart_UnAff": h_series[0]
            }
        )

    # Swing phase
    if _phaseStart == 'endOfPreSwing' and _phaseEnd == 'endOfTerminalSwing':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[9],
                "GaitStart_Aff": gaitWidth[8],
                "GaitWidth_UnAff": gaitWidth[9],
                "GaitStart_UnAff": gaitWidth[8]
            }
        )

    # === === === ===
    # Perry phases (ignoring initial contact)
    # Load response
    if _phaseStart == 'initialContact' and _phaseEnd == 'endOfLoadingResponse':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[0],
                "GaitStart_Aff": h_series[0],
                "GaitWidth_UnAff": gaitWidth[0],
                "GaitStart_UnAff": h_series[0]
            }
        )

    # Mid stance
    if _phaseStart == 'endOfLoadingResponse' and _phaseEnd == 'endOfMidStance':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[1],
                "GaitStart_Aff": h_series[1],
                "GaitWidth_UnAff": gaitWidth[1],
                "GaitStart_UnAff": h_series[1]
            }
        )

    # Terminal stance
    if _phaseStart == 'endOfMidstance' and _phaseEnd == 'endOfTerminalStance':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[2],
                "GaitStart_Aff": h_series[2],
                "GaitWidth_UnAff": gaitWidth[2],
                "GaitStart_UnAff": h_series[2]
            }
        )

    # Pre swing
    if _phaseStart == 'endOfTerminalStance' and _phaseEnd == 'endOfPreSwing':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[3],
                "GaitStart_Aff": h_series[3],
                "GaitWidth_UnAff": gaitWidth[3],
                "GaitStart_UnAff": h_series[3]
            }
        )

    # Initial swing
    if _phaseStart == 'endOfPreswing' and _phaseEnd == 'endOfInitialSwing':
        h_metadata = pd.Series(    
            {
                "GaitWidth_Aff": gaitWidth[4],
                "GaitStart_Aff": h_series[4],
                "GaitWidth_UnAff": gaitWidth[4],
                "GaitStart_UnAff": h_series[4]
            }
        )

    # Mid swing
    if _phaseStart == 'endOfInitialSwing' and _phaseEnd == 'endOfMidSwing':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[5],
                "GaitStart_Aff": h_series[5],
                "GaitWidth_UnAff": gaitWidth[5],
                "GaitStart_UnAff": h_series[5]
            }
        )

    # Terminal swing
    if _phaseStart == 'endOfMidSwing' and _phaseEnd == 'endOfTerminalSwing':
        h_metadata = pd.Series(
            {
                "GaitWidth_Aff": gaitWidth[6],
                "GaitStart_Aff": h_series[6],
                "GaitWidth_UnAff": gaitWidth[6],
                "GaitStart_UnAff": h_series[6]
            }
        )

    print(h_metadata)


def series_compare(series1, series2):
    '''
    Function to compare subject and healthy subject, converting into bool
    '''
    series_bool = (series1 >= series2).astype(float)
    print(series_bool)