import pandas as pd

from stdutils import extract_gaitphase_rawfeatures

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

def check_gpWithinNorm(_gpSeries, _gpSeriesAff, _gpSeriesUnAff, _healthyData):
    # Remove "Aff" for series comparison
    gpSeriesAff_tmp = pd.Series(
        _gpSeriesAff.values, index=_gpSeriesAff.index.str.replace("Aff", '')
    )

    # Remove "UnAff" for series comparison
    gpSeriesUnAff_tmp = pd.Series(
        _gpSeriesUnAff.values, index=_gpSeriesUnAff.index.str.replace("UnAff", '')
    )
    
    # Check if patient's values lie within the standard deviation
    parameterSD = _healthyData.gaitParameters.set_index('Measure')

    affWithinSDCheck = _healthyData.check_within_limits(
        gpSeriesAff_tmp, parameterSD['Lower-S.D'], parameterSD['Upper-S.D']
    )   
    unAffWithinSDCheck = _healthyData.check_within_limits(
        gpSeriesUnAff_tmp, parameterSD['Lower-S.D'], parameterSD['Upper-S.D']
    )

    # Re-initializing the gait parameters series (_gpSeries)
    combinedSeries = pd.Series(dtype=object,index=_gpSeries.index)
    combinedSeries['StridePairID'] = _gpSeries['StridePairID']
    combinedSeries['Auxiliary']    = _gpSeries['Auxiliary']
    
    for index in affWithinSDCheck.index:
        combinedSeries[index + 'Aff'] = affWithinSDCheck[index]

    for index in unAffWithinSDCheck.index:
        combinedSeries[index + 'UnAff'] = unAffWithinSDCheck[index]

    return combinedSeries

def process_phaseData(idx, patRB_group, _healthyData, stridePairID, phaseStart, phaseEnd):
    '''
    Process the phases to print out 1 or 0 and export .dat file 
    '''
    phase_data = extract_gaitphase_rawfeatures(
        idx, patRB_group, stridePairID, _phaseStart=phaseStart, _phaseEnd=phaseEnd,
        _healthyData=_healthyData
    )

    # Create a column OriIndex to retain original index
    phase_data.UnAffDF = pd.concat(
        [
            phase_data.UnAffDF, 
                pd.DataFrame(
                    data=list(phase_data.UnAffDF.index), 
                    columns=['OriIndex'], 
                    index=phase_data.UnAffDF.index
                )
        ], axis=1
    )

    phase_data.AffDF = pd.concat(
        [
            phase_data.AffDF, 
            pd.DataFrame(
                data=list(phase_data.AffDF.index), 
                columns=['OriIndex'], 
                index=phase_data.AffDF.index
            )
        ], axis=1
    )

    # Unaffected side of subject do within refband check (within=0, else=1) 
    phase_UnAff_RB_check = phase_data.within_RB_check('UnAff')

    # Affected side of subject do within refband check (within=0, else=1)
    phase_Aff_RB_check = phase_data.within_RB_check('Aff')

    # Get healthy subject upper and lower boundary metadata
    phase_upper = phase_data.get_hUpperMetadata(phaseStart, phaseEnd, "std")
    phase_lower = phase_data.get_hLowerMetadata(phaseStart, phaseEnd, "std")
    pat_phase = phase_data.Metadata

    # Patient metadat of subject do is_in refband check (within=0, else=1)
    phase_is_in = ((pat_phase >= phase_lower) & (pat_phase <= phase_upper))
    phase_is_in = (~phase_is_in).astype(int)

    # Unravel m x 3 data into m x 1 dataframe
    phase_Aff_RB_check = _healthyData.unravel(phase_Aff_RB_check)
    phase_UnAff_RB_check = _healthyData.unravel(phase_UnAff_RB_check)

    phase_merged = pd.concat(
        [
            phase_is_in, 
            phase_Aff_RB_check, 
            phase_UnAff_RB_check
        ], axis=0
    ).stack().reset_index(level=1, drop=True)

    return phase_merged

