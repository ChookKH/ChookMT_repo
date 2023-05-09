import time
import pandas as pd

def extract_gaitparameters(gp, _affSide, _side="Aff", stance_swing=False):
    '''
    Extracting and processing gait parameters to be represented as features

    Please indiciate if gait parameters are that of the affected (Aff) stride or unaffected stride (UnAff)
    '''
    gpSeries = pd.Series(dtype=float)

    # Convert pelvis and leg lengths to meters
    pelvisWidth = gp['InterAsisDistance']/1000

    if (_affSide == "R" and _side=="Aff"):
        refLeg = 'RLegLength'
    elif (_affSide == "R" and _side=="UnAff"):
        refLeg = 'LLegLength'
    elif (_affSide == "L" and _side=="Aff"):
        refLeg = "LLegLength"
    elif (_affSide == "L" and _side=="UnAff"):
        refLeg = "RLegLength"

    refLegLength = gp[refLeg]/1000

    stride_time = gp['strideTime']

    # Walking speed
    gpSeries = pd.concat([gpSeries, pd.Series([gp['walkingSpeed']], index=[f'gaitSpeed{_side}'])])
    gpSeries = pd.concat([gpSeries, pd.Series([gp['stepTime']], index=[f'stepTime{_side}'])])
    gpSeries = pd.concat([gpSeries, pd.Series([gp['cadence'] / 60], index=[f'cadence{_side}'])])

    # Update 05.04.2022 - Reincluding stance and swing time here because the absolute values
    # are probably more informative
    gpSeries = pd.concat([gpSeries, pd.Series([stride_time], index=[f'strideTime{_side}'])])

    if stance_swing:
        stance_time = ((gp['endOfPreswing'] - gp['initialContact']) / 100) * stride_time
        gpSeries    = pd.concat([gpSeries, pd.Series([stance_time], index=[f'stanceTime{_side}'])])

        swing_time  = ((gp['endOfTerminalSwing'] - gp['endOfPreswing']) / 100) * stride_time
        gpSeries    = pd.concat([gpSeries, pd.Series([swing_time], index=[f'swingTime{_side}'])])

    sSPortion = gp['singleSupport'] / 100; dSPortion = gp['doubleSupport'] / 100

    gpSeries = pd.concat([gpSeries, pd.Series([sSPortion], index=[f'sSupportPortion{_side}'])])
    gpSeries = pd.concat([gpSeries, 
        pd.Series([sSPortion * stride_time], index=[f'singleSupportTime{_side}'])]
    )

    gpSeries = pd.concat([gpSeries, pd.Series([dSPortion], index=[f'dSupportPortion{_side}'])])
    gpSeries = pd.concat([gpSeries, 
        pd.Series([dSPortion * stride_time], index=[f'doubleSupportTime{_side}'])]
    )

    gpSeries = pd.concat([gpSeries, pd.Series([gp['limpIndex']], index=[f'limpIdx{_side}'])])

    # Stride and step length (normalized with respect to length of leg on the affected side)
    gpSeries = pd.concat([gpSeries, pd.Series([gp['stepLength'] / refLegLength], index=[f'StepFactor{_side}'])])
    gpSeries = pd.concat([gpSeries, pd.Series([gp['strideLength'] / refLegLength], index=[f'StrideFactor{_side}'])])

    gpSeries = pd.concat([gpSeries, pd.Series([gp['stepWidth'] / pelvisWidth], index=[f'StepWidth{_side}'])])
    
    return gpSeries
