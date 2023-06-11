# Dictionary to map features to their more clearer semantical names (during base dataset generation)

# Note to self: This is rather unneccessary, please consider revising
feature_semanticalnames = {
    "hipJointAff_flexion.q": "AHip_FlexionQ",
    "hipJointAff_flexion.qd": "AHip_FlexionQD",
    "hipJointAff_adduction.q": "AHip_AdductionQ",
    "hipJointAff_adduction.qd": "AHip_AdductionQD",
    "hipJointAff_internalRotation.q": "AHip_IntRotationQ",
    "hipJointAff_internalRotation.qd": "AHip_IntRotationQD",

    "kneeJointAff_flexion.q": "AKnee_FlexionQ",
    "kneeJointAff_flexion.qd": "AKnee_FlexionQD",
    "kneeJointAff_varus/adduction.q": "AKnee_VarAdductionQ",
    "kneeJointAff_varus/adduction.qd": "AKnee_VarAdductionQD",
    "kneeJointAff_internalRotation.q": "AKnee_IntRotationQ",
    "kneeJointAff_internalRotation.qd": "AKnee_IntRotationQD",

    "ankleJointAff_dorsiflexion.q": "AAnkle_DorsiflexionQ",
    "ankleJointAff_dorsiflexion.qd": "AAnkle_DorsiflexionQD",
    "ankleJointAff_inversion/eversion.q": "AAnkle_InvEversionQ",
    "ankleJointAff_inversion/eversion.qd": "AAnkle_InvEversionQD",
    "ankleJointAff_internalRotation.q": "AAnkle_IntRotationQ",
    "ankleJointAff_internalRotation.qd": "AAnkle_IntRotationQD",

    "thoraxJointAff_xThorax.q": "AxThoraxQ",
    "thoraxJointAff_xThorax.qd": "AxThoraxQD",
    "thoraxJointAff_yThorax.q": "AyThoraxQ",
    "thoraxJointAff_yThorax.qd": "AyThoraxQD",
    "thoraxJointAff_zThorax.q": "AzThoraxQ",
    "thoraxJointAff_zThorax.qd": "AzThoraxQD",
    "thoraxJointAff_forwardTilt.q": "AThorax_ForwardTiltQ",
    "thoraxJointAff_forwardTilt.qd": "AThorax_ForwardTiltQD",
    "thoraxJointAff_sideTilt.q": "AThorax_SideTiltQ",
    "thoraxJointAff_sideTilt.qd": "AThorax_SideTiltQD",
    "thoraxJointAff_internalRotation.q": "AThorax_IntRotationQ",
    "thoraxJointAff_internalRotation.qd": "AThorax_IntRotationQD",
    "thoraxJointAff_rotation.q": "AThoraxJoint_IntRotationQ",
    "thoraxJointAff_rotation.qd": "AThoraxJoint_IntRotationQD",

    "thoraxJointUnAff_xThorax.q": "UnAxThoraxQ",
    "thoraxJointUnAff_xThorax.qd": "UnAxThoraxQD",
    "thoraxJointUnAff_yThorax.q": "UnAyThoraxQ",
    "thoraxJointUnAff_yThorax.qd": "UnAyThoraxQD",
    "thoraxJointUnAff_zThorax.q": "UnAzThoraxQ",
    "thoraxJointUnAff_zThorax.qd": "UnAzThoraxQD",
    "thoraxJointUnAff_forwardTilt.q": "UnAThorax_ForwardTiltQ",
    "thoraxJointUnAff_forwardTilt.qd": "UnAThorax_ForwardTiltQD",
    "thoraxJointUnAff_sideTilt.q": "UnAThorax_SideTiltQ",
    "thoraxJointUnAff_sideTilt.qd": "UnAThorax_SideTiltQD",
    "thoraxJointUnAff_internalRotation.q": "UnAThorax_IntRotationQ",
    "thoraxJointUnAff_internalRotation.qd": "UnAThorax_IntRotationQD",
    "thoraxJointUnAff_rotation.q": "UnAThoraxJoint_IntRotationQ",
    "thoraxJointUnAff_rotation.qd": "UnAThoraxJoint_IntRotationQD",

    "pelvisJointAff_xPelvis.q": "AxPelvisQ",
    "pelvisJointAff_xPelvis.qd": "AxPelvisQD",
    "pelvisJointAff_yPelvis.q": "AyPelvisQ",
    "pelvisJointAff_yPelvis.qd": "AyPelvisQD",
    "pelvisJointAff_zPelvis.q": "AzPelvisQ",
    "pelvisJointAff_zPelvis.qd": "AzPelvisQD",
    "pelvisJointAff_forwardTilt.q": "APelvis_ForwardTiltQ",
    "pelvisJointAff_forwardTilt.qd": "APelvis_ForwardTiltQD",
    "pelvisJointAff_sideTilt.q": "APelvis_SideTiltQ",
    "pelvisJointAff_sideTilt.qd": "APelvis_SideTiltQD",
    "pelvisJointAff_rotation.q": "APelvis_IntRotationQ",
    "pelvisJointAff_rotation.qd": "APelvis_IntRotationQD",

    "pelvisJointUnAff_xPelvis.q": "UnAxPelvisQ",
    "pelvisJointUnAff_xPelvis.qd": "UnAxPelvisQD",
    "pelvisJointUnAff_yPelvis.q": "UnAyPelvisQ",
    "pelvisJointUnAff_yPelvis.qd": "UnAyPelvisQD",
    "pelvisJointUnAff_zPelvis.q": "UnAzPelvisQ",
    "pelvisJointUnAff_zPelvis.qd": "UnAzPelvisQD",
    "pelvisJointUnAff_forwardTilt.q": "UnAPelvis_ForwardTiltQ",
    "pelvisJointUnAff_forwardTilt.qd": "UnAPelvis_ForwardTiltQD",
    "pelvisJointUnAff_sideTilt.q": "UnAPelvis_SideTiltQ",
    "pelvisJointUnAff_sideTilt.qd": "UnAPelvis_SideTiltQD",
    "pelvisJointUnAff_rotation.q": "UnAPelvis_IntRotationQ",
    "pelvisJointUnAff_rotation.qd": "UnAPelvis_IntRotationQD",

    "upperBodyTiltAngleAff.q": "AUpperBodyTiltAngleQ",
    "upperBodyTiltAngleUnAff.q": "UnAUpperBodyTiltAngleQ",

    "footFloorDistanceAff.q": "AFootFloorDistanceQ",
    "normalizedFunctionalLegLengthAff.q": "ANormalizedFunctionalLegLengthQ",
    "normalizedAnkleFloorDistanceAff.q": "ANormalizedAnkleFloorDistanceQ",
    "footProgressionAnglesAff_1.q": "AFootProgressionAngles_1Q",
    "footProgressionAnglesAff_2.q": "AFootProgressionAngles_2Q",
    "footProgressionAnglesAff_3.q": "AFootProgressionAngles_3Q",

    "footFloorDistanceUnAff.q": "UnAFootFloorDistanceQ",
    "normalizedFunctionalLegLengthUnAff.q": "UnANormalizedFunctionalLegLengthQ",
    "normalizedAnkleFloorDistanceUnAff.q": "UnANormalizedAnkleFloorDistanceQ",
    "footProgressionAnglesUnAff_1.q": "UnAFootProgressionAngles_1Q",
    "footProgressionAnglesUnAff_2.q": "UnAFootProgressionAngles_2Q",
    "footProgressionAnglesUnAff_3.q": "UnAFootProgressionAngles_3Q",

    "shoulderJointAff_flexion.q": "AShoulder_FlexionQ",
    "shoulderJointAff_flexion.qd": "AShoulder_FlexionQD",
    "shoulderJointAff_abduction.q": "AShoulder_AbductionQ",
    "shoulderJointAff_abduction.qd": "AShoulder_AbductionQD",
    "shoulderJointAff_internalRotation.q": "AShoulder_IntRotationQ",
    "shoulderJointAff_internalRotation.qd": "AShoulder_IntRotationQD",

    "elbowJointAff_flexion.q": "AElbow_FlexionQ",
    "elbowJointAff_flexion.qd": "AElbow_FlexionQD",
    "elbowJointAff_abduction.q": "AElbow_AbductionQ",
    "elbowJointAff_abduction.qd": "AElbow_AbductionQD",
    "elbowJointAff_internalRotation.q": "AElbow_IntRotationQ",
    "elbowJointAff_internalRotation.qd": "AElbow_IntRotationQD",

    "wristJointAff_flexion.q": "AWrist_FlexionQ",
    "wristJointAff_flexion.qd": "AWrist_FlexionQD",
    "wristJointAff_radialUlnarDeviation.q": "AWrist_RadUlnarDevQ",
    "wristJointAff_radialUlnarDeviation.qd": "AWrist_RadUlnarDevQD",
    "wristJointAff_pronation/supination.q": "AWrist_ProSupinationQ",
    "wristJointAff_pronation/supination.qd": "AWrist_ProSupinationQD",

    "hipJointUnAff_flexion.q": "UnAHip_FlexionQ",
    "hipJointUnAff_flexion.qd": "UnAHip_FlexionQD",
    "hipJointUnAff_adduction.q": "UnAHip_AdductionQ",
    "hipJointUnAff_adduction.qd": "UnAHip_AdductionQD",
    "hipJointUnAff_internalRotation.q": "UnAHip_IntRotationQ",
    "hipJointUnAff_internalRotation.qd": "UnAHip_IntRotationQD",

    "kneeJointUnAff_flexion.q": "UnAKnee_FlexionQ",
    "kneeJointUnAff_flexion.qd": "UnAKnee_FlexionQD",
    "kneeJointUnAff_varus/adduction.q": "UnAKnee_VarAdductionQ",
    "kneeJointUnAff_varus/adduction.qd": "UnAKnee_VarAdductionQD",
    "kneeJointUnAff_internalRotation.q": "UnAKnee_IntRotationQ",
    "kneeJointUnAff_internalRotation.qd": "UnAKnee_IntRotationQD",

    "ankleJointUnAff_dorsiflexion.q": "UnAAnkle_DorsiflexionQ",
    "ankleJointUnAff_dorsiflexion.qd": "UnAAnkle_DorsiflexionQD",
    "ankleJointUnAff_inversion/eversion.q": "UnAAnkle_InvEversionQ",
    "ankleJointUnAff_inversion/eversion.qd": "UnAAnkle_InvEversionQD",
    "ankleJointUnAff_internalRotation.q": "UnAAnkle_IntRotationQ",
    "ankleJointUnAff_internalRotation.qd": "UnAAnkle_IntRotationQD",

    "shoulderJointUnAff_flexion.q": "UnAShoulder_FlexionQ",
    "shoulderJointUnAff_flexion.qd": "UnAShoulder_FlexionQD",
    "shoulderJointUnAff_abduction.q": "UnAShoulder_AbductionQ",
    "shoulderJointUnAff_abduction.qd": "UnAShoulder_AbductionQD",
    "shoulderJointUnAff_internalRotation.q": "UnAShoulder_IntRotationQ",
    "shoulderJointUnAff_internalRotation.qd": "UnAShoulder_IntRotationQD",

    "elbowJointUnAff_flexion.q": "UnAElbow_FlexionQ",
    "elbowJointUnAff_flexion.qd": "UnAElbow_FlexionQD",

    "wristJointUnAff_flexion.q": "UnAWrist_FlexionQ",
    "wristJointUnAff_flexion.qd": "UnAWrist_FlexionQD",
    "wristJointUnAff_radialUlnarDeviation.q": "UnAWrist_RadUlnarDevQ",
    "wristJointUnAff_radialUlnarDeviation.qd": "UnAWrist_RadUlnarDevQD",
    "wristJointUnAff_pronation/supination.q": "UnAWrist_ProSupinationQ",
    "wristJointUnAff_pronation/supination.qd": "UnAWrist_ProSupinationQD"
}

# Dictionary mapping the kinematical data to the appropriate name and SI Units
KinData_Dict = {
    "pelvisJoint_xPelvis.q": r"Pelvis Joint xPelvis $[m]$",
    "pelvisJoint_xPelvis.qd": r"Pelvis Joint xPelvis Gradient",
    "pelvisJoint_yPelvis.q": r"Pelvis Joint yPelvis $[m]$",
    "pelvisJoint_yPelvis.qd": r"Pelvis Joint yPelvis Gradient",
    "pelvisJoint_zPelvis.q": r"Pelvis Joint zPelvis $[m]$",
    "pelvisJoint_zPelvis.qd": r"Pelvis Joint zPelvis Gradient",
    "pelvisJoint_forwardTilt.q": r"Pelvis Joint Forward Tilt $[°]$",
    "pelvisJoint_forwardTilt.qd": r"Pelvis Joint Forward Tilt Gradient",
    "pelvisJoint_sideTilt.q": r"Pelvis Joint Side Tilt $[°]$",
    "pelvisJoint_sideTilt.qd": r"Pelvis Joint Side Tilt Gradient",
    "pelvisJoint_rotation.q": r"Pelvis Joint Rotation $[°]$",
    "pelvisJoint_rotation.qd": r"Pelvis Joint Rotation Gradient",

    "upperBodyTiltAngle.q": r"Upper Body Tilt Angle $[°]$",

    "footFloorDistanceRight.q": r"(R) Foot Floor Distance $[m]$",
    "normalizedFunctionalLegLengthRight.q": r"(R) Normalized Functional Leg Length",
    "normalizedAnkleFloorDistanceRight.q": r"(R) Normalized Ankle Floor Distance",
    "footProgressionAnglesRight_1.q": r"(R) Foot Progression Angles 1 $[°]$",
    "footProgressionAnglesRight_2.q": r"(R) Foot Progression Angles 2 $[°]$",
    "footProgressionAnglesRight_3.q": r"(R) Foot Progression Angles 3 $[°]$",

    "footFloorDistanceLeft.q": r"(L) Foot Floor Distance $[m]$",
    "normalizedFunctionalLegLengthLeft.q": r"(L) Normalized Functional Leg Length",
    "normalizedAnkleFloorDistanceLeft.q": r"(L) Normalized Ankle Floor Distance",
    "footProgressionAnglesLeft_1.q": r"(L) Foot Progression Angles 1 $[°]$",
    "footProgressionAnglesLeft_2.q": r"(L) Foot Progression Angles 2 $[°]$",
    "footProgressionAnglesLeft_3.q": r"(L) Foot Progression Angles 3 $[°]$",

    "hipJointRight_flexion.q": r"(R) Hip Joint Flexion $[°]$",
    "hipJointRight_flexion.qd": r"(R) Hip Joint Flexion Gradient",
    "hipJointRight_adduction.q": r"(R) Hip Joint Adduction $[°]$",
    "hipJointRight_adduction.qd": r"(R) Hip Joint Adduction Gradient",
    "hipJointRight_internalRotation.q": r"(R) Hip Joint Internal Rotation $[°]$",
    "hipJointRight_internalRotation.qd": r"(R) Hip Joint Internal Rotation Gradient",

    "kneeJointRight_flexion.q": r"(R) Knee Joint Flexion $[°]$",
    "kneeJointRight_flexion.qd": r"(R) Knee Joint Flexion Gradient",
    "kneeJointRight_varus/adduction.q": r"(R) Knee Joint Varus/Adduction $[°]$",
    "kneeJointRight_varus/adduction.qd": r"(R) Knee Joint Varus/Adduction Gradient",
    "kneeJointRight_internalRotation.q": r"(R) Knee Joint Internal Rotation $[°]$",
    "kneeJointRight_internalRotation.qd": r"(R) Knee Joint Internal Rotation Gradient",

    "ankleJointRight_dorsiflexion.q": r"(R) Ankle Joint Dorsiflexion $[°]$",
    "ankleJointRight_dorsiflexion.qd": r"(R) Ankle Joint Dorsiflexion Gradient",
    "ankleJointRight_inversion/eversion.q": r"(R) Ankle Joint Inversion/Eversion $[°]$",
    "ankleJointRight_inversion/eversion.qd": r"(R) Ankle Joint Inversion/Eversion Gradient",
    "ankleJointRight_internalRotation.q": r"(R) Ankle Joint Internal Rotation $[°]$",
    "ankleJointRight_internalRotation.qd": r"(R) Ankle Joint Internal Rotation Gradient",

    "hipJointLeft_flexion.q": r"(L) Hip Joint Flexion $[°]$",
    "hipJointLeft_flexion.qd": r"(L) Hip Joint Flexion Gradient",
    "hipJointLeft_adduction.q": r"(L) Hip Joint Adduction $[°]$",
    "hipJointLeft_adduction.qd": r"(L) Hip Joint Adduction Gradient",
    "hipJointLeft_internalRotation.q": r"(L) Hip Joint Internal Rotation $[°]$",
    "hipJointLeft_internalRotation.qd": r"(L) Hip Joint Internal Rotation Gradient",

    "kneeJointLeft_flexion.q": r"(L) Knee Joint Flexion $[°]$",
    "kneeJointLeft_flexion.qd": r"(L) Knee Joint Flexion Gradient",
    "kneeJointLeft_varus/adduction.q": r"(L) Knee Joint Varus/Adduction $[°]$",
    "kneeJointLeft_varus/adduction.qd": r"(L) Knee Joint Varus/Adduction Gradient",
    "kneeJointLeft_internalRotation.q": r"(L) Knee Joint Internal Rotation $[°]$",
    "kneeJointLeft_internalRotation.qd": r"(L) Knee Joint Internal Rotation Gradient",

    "ankleJointLeft_dorsiflexion.q": r"(L) Ankle Joint Dorsiflexion $[°]$",
    "ankleJointLeft_dorsiflexion.qd": r"(L) Ankle Joint Dorsiflexion Gradient",
    "ankleJointLeft_inversion/eversion.q": r"(L) Ankle Joint Inversion/Eversion $[°]$",
    "ankleJointLeft_inversion/eversion.qd": r"(L) Ankle Joint Inversion/Eversion Gradient",
    "ankleJointLeft_internalRotation.q": r"(L) Ankle Joint Internal Rotation $[°]$",
    "ankleJointLeft_internalRotation.qd": r"(L) Ankle Joint Internal Rotation Gradient",

    "headJoint_xHead.q": r"Head Joint xHead $[m]$",
    "headJoint_xHead.qd": r"Head Joint xHead Gradient",
    "headJoint_yHead.q": r"Head Joint yHead $[m]$",
    "headJoint_yHead.qd": r"Head Joint yHead Gradient",
    "headJoint_zHead.q": r"Head Joint zHead $[m]$",
    "headJoint_zHead.qd": r"Head Joint zHead Gradient",
    "headJoint_forwardTilt.q": r"Head Joint Forward Tilt $[°]$",
    "headJoint_forwardTilt.qd": r"Head Joint Forward Tilt Gradient",
    "headJoint_sideTilt.q": r"Head Joint Side Tilt $[°]$",
    "headJoint_sideTilt.qd": r"Head Joint Side Tilt Gradient",
    "headJoint_internalRotation.q": r"Head Joint Internal Rotation $[°]$",
    "headJoint_internalRotation.qd": r"Head Joint Internal Rotation Gradient",

    "shoulderJointRight_flexion.q": r"(R) Shoulder Joint Flexion $[°]$",
    "shoulderJointRight_flexion.qd": r"(R) Shoulder Joint Flexion Gradient",
    "shoulderJointRight_abduction.q": r"(R) Shoulder Joint Abduction $[°]$",
    "shoulderJointRight_abduction.qd": r"(R) Shoulder Joint Abduction Gradient",
    "shoulderJointRight_internalRotation.q": r"(R) Shoulder Joint Internal Rotation $[°]$",
    "shoulderJointRight_internalRotation.qd": r"(R) Shoulder Joint Internal Rotation Gradient",

    "elbowJointRight_flexion.q": r"(R) Elbow Joint Flexion $[°]$",
    "elbowJointRight_flexion.qd": r"(R) Elbow Joint Flexion Gradient",
    "elbowJointRight_abduction.q": r"(R) Elbow Joint Abduction $[°]$",
    "elbowJointRight_abduction.qd": r"(R) Elbow Joint Abduction Gradient",
    "elbowJointRight_internalRotation.q": r"(R) Elbow Joint Internal Rotation $[°]$",
    "elbowJointRight_internalRotation.qd": r"(R) Elbow Joint Internal Rotation Gradient",

    "wristJointRight_flexion.q": r"(R) Wrist Joint Flexion $[°]$",
    "wristJointRight_flexion.qd": r"(R) Wrist Joint Flexion Gradient",
    "wristJointRight_radialUlnarDeviation.q": r"(R) Wrist Joint Radial/Ulnar Deviation $[°]$",
    "wristJointRight_radialUlnarDeviation.qd": r"(R) Wrist Joint Radial/Ulnar Deviation Gradient",
    "wristJointRight_pronation/supination.q": r"(R) Wrist Joint Pronation/Supination $[°]$",
    "wristJointRight_pronation/supination.qd": r"(R) Wrist Joint Pronation/Supination Gradient",

    "shoulderJointLeft_flexion.q": r"(L) Shoulder Joint Flexion $[°]$",
    "shoulderJointLeft_flexion.qd": r"(L) Shoulder Joint Flexion Gradient",
    "shoulderJointLeft_abduction.q": r"(L) Shoulder Joint Abduction $[°]$",
    "shoulderJointLeft_abduction.qd": r"(L) Shoulder Joint Abduction Gradient",
    "shoulderJointLeft_internalRotation.q": r"(L) Shoulder Joint Internal Rotation $[°]$",
    "shoulderJointLeft_internalRotation.qd": r"(L) Shoulder Joint Internal Rotation Gradient",

    "elbowJointLeft_flexion.q": r"(L) Elbow Joint Flexion $[°]$",
    "elbowJointLeft_flexion.qd": r"(L) Elbow Joint Flexion Gradient",

    "elbowJointLeft_abduction.q": r"(L) Elbow Joint Abduction $[°]$",
    "elbowJointLeft_abduction.qd": r"(L) Elbow Joint Abduction Gradient",
    "elbowJointLeft_internalRotation.q": r"(L) Elbow Joint Internal Rotation $[°]$",
    "elbowJointLeft_internalRotation.qd": r"(L) Elbow Joint Internal Rotation Gradient",

    "wristJointLeft_flexion.q": r"(L) Wrist Joint Flexion $[°]$",
    "wristJointLeft_flexion.qd": r"(L) Wrist Joint Flexion Gradient",
    "wristJointLeft_radialUlnarDeviation.q": r"(L) Wrist Joint Radial/Ulnar Deviation $[°]$",
    "wristJointLeft_radialUlnarDeviation.qd": r"(L) Wrist Joint Radial/Ulnar Deviation Gradient",
    "wristJointLeft_pronation/supination.q": r"(L) Wrist Joint Pronation/Supination $[°]$",
    "wristJointLeft_pronation/supination.qd": r"(L) Wrist Joint Pronation/Supination Gradient",

    "thoraxJoint_xThorax.q": r"Thorax Joint xThorax $[m]$",
    "thoraxJoint_xThorax.qd": r"Thorax Joint xThorax Gradient",
    "thoraxJoint_yThorax.q": r"Thorax Joint yThorax $[m]$",
    "thoraxJoint_yThorax.qd": r"Thorax Joint yThorax Gradient",
    "thoraxJoint_zThorax.q": r"Thorax Joint zThorax $[m]$",
    "thoraxJoint_zThorax.qd": r"Thorax Joint zThorax Gradient",
    "thoraxJoint_forwardTilt.q": r"Thorax Joint Forward Tilt $[°]$",
    "thoraxJoint_forwardTilt.qd": r"Thorax Joint Forward Tilt Gradient",
    "thoraxJoint_sideTilt.q": r"Thorax Joint Side Tilt $[°]$",
    "thoraxJoint_sideTilt.qd": r"Thorax Joint Side Tilt Gradient",
    "thoraxJoint_internalRotation.q": r"Thorax Joint Internal Rotation $[°]$",
    "thoraxJoint_internalRotation.qd": r"Thorax Joint Internal Rotation Gradient",
    "thoraxJoint_rotation.q": r"Thorax Joint Internal Rotation $[°]$",
    "thoraxJoint_rotation.qd": r"Thorax Joint Internal Rotation Gradient"
}

# Dictionary mapping the kinematical data to the appropriate name and SI Units (Old)
KinData_DictOld = {
    "pelvisJoint_xPelvis.q": r"Pelvis Joint xPelvis $[m]$",
    "pelvisJoint_xPelvis.qd": r"Pelvis Joint xPelvis Velocity $[\frac{m}{s}]$",
    "pelvisJoint_yPelvis.q": r"Pelvis Joint yPelvis $[m]$",
    "pelvisJoint_yPelvis.qd": r"Pelvis Joint yPelvis Velocity $[\frac{m}{s}]$",
    "pelvisJoint_zPelvis.q": r"Pelvis Joint zPelvis $[m]$",
    "pelvisJoint_zPelvis.qd": r"Pelvis Joint zPelvis Velocity $[\frac{m}{s}]$",
    "pelvisJoint_forwardTilt.q": r"Pelvis Joint Forward Tilt $[rad]$",
    "pelvisJoint_forwardTilt.qd": r"Pelvis Joint Forward Tilt Velocity$[\frac{rad}{s}]$",
    "pelvisJoint_sideTilt.q": r"Pelvis Joint Side Tilt $[rad]$",
    "pelvisJoint_sideTilt.qd": r"Pelvis Joint Side Tilt Velocity $[\frac{rad}{s}]$",
    "pelvisJoint_rotation.q": r"Pelvis Joint Rotation $[rad]$",
    "pelvisJoint_rotation.qd": r"Pelvis Joint Rotation Velocity $[\frac{rad}{s}]$",

    "upperBodyTiltAngle.q": r"Upper Body Tilt Angle $[rad]$",

    "footFloorDistanceRight.q": r"(R) Foot Floor Distance $[m]$",
    "normalizedFunctionalLegLengthRight.q": r"(R) Normalized Functional Leg Length",
    "normalizedAnkleFloorDistanceRight.q": r"(R) Normalized Ankle Floor Distance",
    "footProgressionAnglesRight_1.q": r"(R) Foot Progression Angles 1 $[rad]$",
    "footProgressionAnglesRight_2.q": r"(R) Foot Progression Angles 2 $[rad]$",
    "footProgressionAnglesRight_3.q": r"(R) Foot Progression Angles 3 $[rad]$",

    "footFloorDistanceLeft.q": r"(L) Foot Floor Distance $[m]$",
    "normalizedFunctionalLegLengthLeft.q": r"(L) Normalized Functional Leg Length",
    "normalizedAnkleFloorDistanceLeft.q": r"(L) Normalized Ankle Floor Distance",
    "footProgressionAnglesLeft_1.q": r"(L) Foot Progression Angles 1 $[rad]$",
    "footProgressionAnglesLeft_2.q": r"(L) Foot Progression Angles 2 $[rad]$",
    "footProgressionAnglesLeft_3.q": r"(L) Foot Progression Angles 3 $[rad]$",

    "hipJointRight_flexion.q": r"(R) Hip Joint Flexion $[rad]$",
    "hipJointRight_flexion.qd": r"(R) Hip Joint Flexion Velocity $[\frac{rad}{s}]$",
    "hipJointRight_adduction.q": r"(R) Hip Joint Adduction $[rad]$",
    "hipJointRight_adduction.qd": r"(R) Hip Joint Adduction Velocity $[\frac{rad}{s}]$",
    "hipJointRight_internalRotation.q": r"(R) Hip Joint Internal Rotation $[rad]$",
    "hipJointRight_internalRotation.qd": r"(R) Hip Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "kneeJointRight_flexion.q": r"(R) Knee Joint Flexion $[rad]$",
    "kneeJointRight_flexion.qd": r"(R) Knee Joint Flexion Velocity $[\frac{rad}{s}]$",
    "kneeJointRight_varus/adduction.q": r"(R) Knee Joint Varus/Adduction $[rad]$",
    "kneeJointRight_varus/adduction.qd": r"(R) Knee Joint Varus/Adduction Velocity $[\frac{rad}{s}]$",
    "kneeJointRight_internalRotation.q": r"(R) Knee Joint Internal Rotation $[rad]$",
    "kneeJointRight_internalRotation.qd": r"(R) Knee Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "ankleJointRight_dorsiflexion.q": r"(R) Ankle Joint Dorsiflexion $[rad]$",
    "ankleJointRight_dorsiflexion.qd": r"(R) Ankle Joint Dorsiflexion Velocity $[\frac{rad}{s}]$",
    "ankleJointRight_inversion/eversion.q": r"(R) Ankle Joint Inversion/Eversion $[rad]$",
    "ankleJointRight_inversion/eversion.qd": r"(R) Ankle Joint Inversion/Eversion Velocity $[\frac{rad}{s}]$",
    "ankleJointRight_internalRotation.q": r"(R) Ankle Joint Internal Rotation $[rad]$",
    "ankleJointRight_internalRotation.qd": r"(R) Ankle Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "hipJointLeft_flexion.q": r"(L) Hip Joint Flexion $[rad]$",
    "hipJointLeft_flexion.qd": r"(L) Hip Joint Flexion Velocity $[\frac{rad}{s}]$",
    "hipJointLeft_adduction.q": r"(L) Hip Joint Adduction $[rad]$",
    "hipJointLeft_adduction.qd": r"(L) Hip Joint Adduction Velocity $[\frac{rad}{s}]$",
    "hipJointLeft_internalRotation.q": r"(L) Hip Joint Internal Rotation $[rad]$",
    "hipJointLeft_internalRotation.qd": r"(L) Hip Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "kneeJointLeft_flexion.q": r"(L) Knee Joint Flexion $[rad]$",
    "kneeJointLeft_flexion.qd": r"(L) Knee Joint Flexion Velocity $[\frac{rad}{s}]$",
    "kneeJointLeft_varus/adduction.q": r"(L) Knee Joint Varus/Adduction $[rad]$",
    "kneeJointLeft_varus/adduction.qd": r"(L) Knee Joint Varus/Adduction Velocity $[\frac{rad}{s}]$",
    "kneeJointLeft_internalRotation.q": r"(L) Knee Joint Internal Rotation $[rad]$",
    "kneeJointLeft_internalRotation.qd": r"(L) Knee Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "ankleJointLeft_dorsiflexion.q": r"(L) Ankle Joint Dorsiflexion $[rad]$",
    "ankleJointLeft_dorsiflexion.qd": r"(L) Ankle Joint Dorsiflexion Velocity $[\frac{rad}{s}]$",
    "ankleJointLeft_inversion/eversion.q": r"(L) Ankle Joint Inversion/Eversion $[rad]$",
    "ankleJointLeft_inversion/eversion.qd": r"(L) Ankle Joint Inversion/Eversion Velocity $[\frac{rad}{s}]$",
    "ankleJointLeft_internalRotation.q": r"(L) Ankle Joint Internal Rotation $[rad]$",
    "ankleJointLeft_internalRotation.qd": r"(L) Ankle Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "headJoint_xHead.q": r"Head Joint xHead $[m]$",
    "headJoint_xHead.qd": r"Head Joint xHead Velocity $[\frac{m}{s}]$",
    "headJoint_yHead.q": r"Head Joint yHead $[m]$",
    "headJoint_yHead.qd": r"Head Joint yHead Velocity $[\frac{m}{s}]$",
    "headJoint_zHead.q": r"Head Joint zHead $[m]$",
    "headJoint_zHead.qd": r"Head Joint zHead Velocity $[\frac{m}{s}]$",
    "headJoint_forwardTilt.q": r"Head Joint Forward Tilt $[rad]$",
    "headJoint_forwardTilt.qd": r"Head Joint Forward Tilt Velocity $[\frac{rad}{s}]$",
    "headJoint_sideTilt.q": r"Head Joint Side Tilt $[rad]$",
    "headJoint_sideTilt.qd": r"Head Joint Side Tilt Velocity $[\frac{rad}{s}]$",
    "headJoint_internalRotation.q": r"Head Joint Internal Rotation $[rad]$",
    "headJoint_internalRotation.qd": r"Head Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "shoulderJointRight_flexion.q": r"(R) Shoulder Joint Flexion $[rad]$",
    "shoulderJointRight_flexion.qd": r"(R) Shoulder Joint Flexion Velocity $[\frac{rad}{s}]$",
    "shoulderJointRight_abduction.q": r"(R) Shoulder Joint Abduction $[rad]$",
    "shoulderJointRight_abduction.qd": r"(R) Shoulder Joint Abduction Velocity $[\frac{rad}{s}]$",
    "shoulderJointRight_internalRotation.q": r"(R) Shoulder Joint Internal Rotation $[rad]$",
    "shoulderJointRight_internalRotation.qd": r"(R) Shoulder Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "elbowJointRight_flexion.q": r"(R) Elbow Joint Flexion $[rad]$",
    "elbowJointRight_flexion.qd": r"(R) Elbow Joint Flexion Velocity $[\frac{rad}{s}]$",
    "elbowJointRight_abduction.q": r"(R) Elbow Joint Abduction $[rad]$",
    "elbowJointRight_abduction.qd": r"(R) Elbow Joint Abduction Velocity $[\frac{rad}{s}]$",
    "elbowJointRight_internalRotation.q": r"(R) Elbow Joint Internal Rotation $[rad]$",
    "elbowJointRight_internalRotation.qd": r"(R) Elbow Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "wristJointRight_flexion.q": r"(R) Wrist Joint Flexion $[rad]$",
    "wristJointRight_flexion.qd": r"(R) Wrist Joint Flexion Velocity $[\frac{rad}{s}]$",
    "wristJointRight_radialUlnarDeviation.q": r"(R) Wrist Joint Radial/Ulnar Deviation $[rad]$",
    "wristJointRight_radialUlnarDeviation.qd": r"(R) Wrist Joint Radial/Ulnar Deviation Velocity $[\frac{rad}{s}]$",
    "wristJointRight_pronation/supination.q": r"(R) Wrist Joint Pronation/Supination $[rad]$",
    "wristJointRight_pronation/supination.qd": r"(R) Wrist Joint Pronation/Supination Velocity $[\frac{rad}{s}]$",

    "shoulderJointLeft_flexion.q": r"(L) Shoulder Joint Flexion $[rad]$",
    "shoulderJointLeft_flexion.qd": r"(L) Shoulder Joint Flexion Velocity $[\frac{rad}{s}]$",
    "shoulderJointLeft_abduction.q": r"(L) Shoulder Joint Abduction $[rad]$",
    "shoulderJointLeft_abduction.qd": r"(L) Shoulder Joint Abduction Velocity $[\frac{rad}{s}]$",
    "shoulderJointLeft_internalRotation.q": r"(L) Shoulder Joint Internal Rotation $[rad]$",
    "shoulderJointLeft_internalRotation.qd": r"(L) Shoulder Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "elbowJointLeft_flexion.q": r"(L) Elbow Joint Flexion $[rad]$",
    "elbowJointLeft_flexion.qd": r"(L) Elbow Joint Flexion Velocity $[\frac{rad}{s}]$",

    "elbowJointLeft_abduction.q": r"(L) Elbow Joint Abduction $[rad]$",
    "elbowJointLeft_abduction.qd": r"(L) Elbow Joint Abduction Velocity $[\frac{rad}{s}]$",
    "elbowJointLeft_internalRotation.q": r"(L) Elbow Joint Internal Rotation $[rad]$",
    "elbowJointLeft_internalRotation.qd": r"(L) Elbow Joint Internal Rotation Velocity $[\frac{rad}{s}]$",

    "wristJointLeft_flexion.q": r"(L) Wrist Joint Flexion $[rad]$",
    "wristJointLeft_flexion.qd": r"(L) Wrist Joint Flexion Velocity $[\frac{rad}{s}]$",
    "wristJointLeft_radialUlnarDeviation.q": r"(L) Wrist Joint Radial/Ulnar Deviation $[rad]$",
    "wristJointLeft_radialUlnarDeviation.qd": r"(L) Wrist Joint Radial/Ulnar Deviation Velocity $[\frac{rad}{s}]$",
    "wristJointLeft_pronation/supination.q": r"(L) Wrist Joint Pronation/Supination $[rad]$",
    "wristJointLeft_pronation/supination.qd": r"(L) Wrist Joint Pronation/Supination Velocity $[\frac{rad}{s}]$",

    "thoraxJoint_xThorax.q": r"Thorax Joint xThorax $[m]$",
    "thoraxJoint_xThorax.qd": r"Thorax Joint xThorax Velocity $[\frac{m}{s}]$",
    "thoraxJoint_yThorax.q": r"Thorax Joint yThorax $[m]$",
    "thoraxJoint_yThorax.qd": r"Thorax Joint yThorax Velocity $[\frac{m}{s}]$",
    "thoraxJoint_zThorax.q": r"Thorax Joint zThorax $[m]$",
    "thoraxJoint_zThorax.qd": r"Thorax Joint zThorax Velocity $[\frac{m}{s}]$",
    "thoraxJoint_forwardTilt.q": r"Thorax Joint Forward Tilt $[rad]$",
    "thoraxJoint_forwardTilt.qd": r"Thorax Joint Forward Tilt Velocity $[\frac{rad}{s}]$",
    "thoraxJoint_sideTilt.q": r"Thorax Joint Side Tilt $[rad]$",
    "thoraxJoint_sideTilt.qd": r"Thorax Joint Side Tilt Velocity $[\frac{rad}{s}]$",
    "thoraxJoint_internalRotation.q": r"Thorax Joint Internal Rotation $[rad]$",
    "thoraxJoint_internalRotation.qd": r"Thorax Joint Internal Rotation Velocity $[\frac{rad}{s}]$",
    "thoraxJoint_rotation.q": r"Thorax Joint Internal Rotation $[rad]$",
    "thoraxJoint_rotation.qd": r"Thorax Joint Internal Rotation Velocity $[\frac{rad}{s}]$"
}

# Dictionary mapping the kinematical data to the appropriate name for file name
KinData_SaveFig_Dict = {
    "hipJointRight_flexion.q": "hipFlexionR_q",
    "hipJointRight_flexion.qd": "hipFlexionR_qd",
    "hipJointRight_adduction.q": "hipAdductionR_q",
    "hipJointRight_adduction.qd": "hipAdductionR_qd",
    "hipJointRight_internalRotation.q": "hipIntRotationR_q",
    "hipJointRight_internalRotation.qd": "hipIntRotationR_qd",
    "kneeJointRight_flexion.q": "kneeFlexionR_q",
    "kneeJointRight_flexion.qd": "kneeFlexionR_qd",
    "kneeJointRight_varus/adduction.q": "kneeVarusAdductionR_q",
    "kneeJointRight_varus/adduction.qd": "kneeVarusAdductionR_qd",
    "kneeJointRight_internalRotation.q": "kneeIntRotationR_q",
    "kneeJointRight_internalRotation.qd": "kneeIntRotationR_qd",
    "ankleJointRight_dorsiflexion.q": "ankleDorsiflexionR_q",
    "ankleJointRight_dorsiflexion.qd": "ankleDorsiflexionR_qd",
    "ankleJointRight_inversion/eversion.q": "ankleInEversionR_q",
    "ankleJointRight_inversion/eversion.qd": "ankleInEversionR_qd",
    "ankleJointRight_internalRotation.q": "ankleIntRotationR_q",
    "ankleJointRight_internalRotation.qd": "ankleIntRotationR_qd",
    "hipJointLeft_flexion.q": "hipFlexionL_q",
    "hipJointLeft_flexion.qd": "hipFlexionL_qd",
    "hipJointLeft_adduction.q": "hipAdductionL_q",
    "hipJointLeft_adduction.qd": "hipAdductionL_qd",
    "hipJointLeft_internalRotation.q": "hipIntRotationL_q",
    "hipJointLeft_internalRotation.qd": "hipIntRotationL_qd",
    "kneeJointLeft_flexion.q": "kneeFlexionL_q",
    "kneeJointLeft_flexion.qd": "kneeFlexionL_qd",
    "kneeJointLeft_varus/adduction.q": "kneeVarusAdductionL_q",
    "kneeJointLeft_varus/adduction.qd": "kneeVarusAdductionL_qd",
    "kneeJointLeft_internalRotation.q": "kneeIntRotationL_q",
    "kneeJointLeft_internalRotation.qd": "kneeIntRotationL_qd",
    "ankleJointLeft_dorsiflexion.q": "ankleDorsiflexionL_q",
    "ankleJointLeft_dorsiflexion.qd": "ankleDorsiflexionL_qd",
    "ankleJointLeft_inversion/eversion.q": "ankleInEversionL_q",
    "ankleJointLeft_inversion/eversion.qd": "ankleInEversionL_qd",
    "ankleJointLeft_internalRotation.q": "ankleIntRotationL_q",
    "ankleJointLeft_internalRotation.qd": "ankleIntRotationL_qd",
    "headJoint_xHead.q": "headX_q",
    "headJoint_xHead.qd": "headX_qd",
    "headJoint_yHead.q": "headY_q",
    "headJoint_yHead.qd": "headY_qd",
    "headJoint_zHead.q": "headZ_q",
    "headJoint_zHead.qd": "headZ_qd",
    "headJoint_forwardTilt.q": "headForwardTilt_q",
    "headJoint_forwardTilt.qd": "headForwardTilt_qd",
    "headJoint_sideTilt.q": "headSideTilt_q",
    "headJoint_sideTilt.qd": "headSideTilt_qd",
    "headJoint_internalRotation.q": "headIntRotation_q",
    "headJoint_internalRotation.qd": "headIntRotation_qd",
    "thoraxJoint_xThorax.q": "thoraxX_q",
    "thoraxJoint_xThorax.qd": "thoraxX_qd",
    "thoraxJoint_yThorax.q": "thoraxY_q",
    "thoraxJoint_yThorax.qd": "thoraxY_qd",
    "thoraxJoint_zThorax.q": "thoraxZ_q",
    "thoraxJoint_zThorax.qd": "thoraxZ_qd",
    "thoraxJoint_forwardTilt.q": "thoraxForwardTilt_q",
    "thoraxJoint_forwardTilt.qd": "thoraxForwardTilt_qd",
    "thoraxJoint_sideTilt.q": "thoraxSideTilt_q",
    "thoraxJoint_sideTilt.qd": "thoraxSideTilt_qd",
    "thoraxJoint_internalRotation.q": "thoraxIntRotation_q",
    "thoraxJoint_internalRotation.qd": "thoraxIntRotation_qd",
    "shoulderJointRight_flexion.q": "shoulderFlexionR_q",
    "shoulderJointRight_flexion.qd": "shoulderFlexionR_qd",
    "shoulderJointRight_abduction.q": "shoulderAbductionR_q",
    "shoulderJointRight_abduction.qd": "shoulderAbductionR_qd",
    "shoulderJointRight_internalRotation.q": "shoulderIntRotationR_q",
    "shoulderJointRight_internalRotation.qd": "shoulderIntRotationR_qd",
    "elbowJointRight_flexion.q": "elbowFlexionR_q",
    "elbowJointRight_flexion.qd": "elbowFlexionR_qd",
    "elbowJointRight_abduction.q": "elbowAbductionR_q",
    "elbowJointRight_abduction.qd": "elbowAbductionR_qd",
    "elbowJointRight_internalRotation.q": "elbowIntRotationR_q",
    "elbowJointRight_internalRotation.qd": "elbowIntRotationR_qd",
    "wristJointRight_flexion.q": "wristFlexionR_q",
    "wristJointRight_flexion.qd": "wristFlexionR_qd",
    "wristJointRight_radialUlnarDeviation.q": "wristRadialUlnarR_q",
    "wristJointRight_radialUlnarDeviation.qd": "wristRadialUlnarR_qd",
    "wristJointRight_pronation/supination.q": "wristProSupinationR_q",
    "wristJointRight_pronation/supination.qd": "wristProSupinationR_qd",
    "shoulderJointLeft_flexion.q": "shoulderFlexionL_q",
    "shoulderJointLeft_flexion.qd": "shoulderFlexionL_qd",
    "shoulderJointLeft_abduction.q": "shoulderAbductionL_q",
    "shoulderJointLeft_abduction.qd": "shoulderAbductionL_qd",
    "shoulderJointLeft_internalRotation.q": "shoulderIntRotation_q",
    "shoulderJointLeft_internalRotation.qd": "shoulderIntRotation_qd",
    "elbowJointLeft_flexion.q": "elbowFlexionL_q",
    "elbowJointLeft_flexion.qd": "elbowFlexionL_qd",
    "elbowJointLeft_abduction.q": "elbowAbductionL_q",
    "elbowJointLeft_abduction.qd": "elbowAbductionL_qd",
    "elbowJointLeft_internalRotation.q": "elbowIntRotationL_q",
    "elbowJointLeft_internalRotation.qd": "elbowIntRotationL_qd",
    "wristJointLeft_flexion.q": "wristFlexionL_q",
    "wristJointLeft_flexion.qd": "wristFlexionL_qd",
    "wristJointLeft_radialUlnarDeviation.q": "wristRadialUlnarL_q",
    "wristJointLeft_radialUlnarDeviation.qd": "wristRadialUlnarL_qd",
    "wristJointLeft_pronation/supination.q": "wristProSupinationL_q",
    "wristJointLeft_pronation/supination.qd": "wristProSupinationL_qd"
}

HipData_Labels = [
    "hipJointRight_flexion.q",
    "hipJointRight_flexion.qd",
    "hipJointRight_adduction.q",
    "hipJointRight_adduction.qd",
    "hipJointLeft_flexion.q",
    "hipJointLeft_flexion.qd",
    "hipJointLeft_adduction.q",
    "hipJointLeft_adduction.qd"
]

HipDataQ_Labels = [
    "hipJointRight_flexion.q",
    "hipJointRight_adduction.q",
    "hipJointLeft_flexion.q",
    "hipJointLeft_adduction.q"
]

HipDataQD_Labels = [
    "hipJointRight_flexion.qd",
    "hipJointRight_adduction.qd",
    "hipJointLeft_flexion.qd",
    "hipJointLeft_adduction.qd"
]

KneeData_Labels = [
    "kneeJointRight_flexion.q",
    "kneeJointRight_flexion.qd",
    "kneeJointRight_varus/adduction.q",
    "kneeJointRight_varus/adduction.qd",
    "kneeJointLeft_flexion.q",
    "kneeJointLeft_flexion.qd",
    "kneeJointLeft_varus/adduction.q",
    "kneeJointLeft_varus/adduction.qd"
]

KneeDataQ_Labels = [
    "kneeJointRight_flexion.q",
    "kneeJointRight_varus/adduction.q",
    "kneeJointLeft_flexion.q",
    "kneeJointLeft_varus/adduction.q"
]

KneeDataQD_Labels = [
    "kneeJointRight_flexion.qd",
    "kneeJointRight_varus/adduction.qd",
    "kneeJointLeft_flexion.qd",
    "kneeJointLeft_varus/adduction.qd"
]

AnkleData_Labels = [
    "ankleJointRight_dorsiflexion.q",
    "ankleJointRight_dorsiflexion.qd",
    "ankleJointRight_inversion/eversion.q",
    "ankleJointRight_inversion/eversion.qd",
    "ankleJointLeft_dorsiflexion.q",
    "ankleJointLeft_dorsiflexion.qd",
    "ankleJointLeft_inversion/eversion.q",
    "ankleJointLeft_inversion/eversion.qd"
]

AnkleDataQ_Labels = [
    "ankleJointRight_dorsiflexion.q",
    "ankleJointRight_inversion/eversion.q",
    "ankleJointLeft_dorsiflexion.q",
    "ankleJointLeft_inversion/eversion.q"
]

AnkleDataQD_Labels = [
    "ankleJointRight_dorsiflexion.qd",
    "ankleJointRight_inversion/eversion.qd",
    "ankleJointLeft_dorsiflexion.qd",
    "ankleJointLeft_inversion/eversion.qd"
]

HeadData_Labels = [
    "headJoint_xHead.q",
    "headJoint_xHead.qd",
    "headJoint_yHead.q",
    "headJoint_yHead.qd",
    "headJoint_zHead.q",
    "headJoint_zHead.qd",
    "headJoint_forwardTilt.q",
    "headJoint_forwardTilt.qd",
    "headJoint_sideTilt.q",
    "headJoint_sideTilt.qd",
    "headJoint_internalRotation.q",
    "headJoint_internalRotation.qd"
]

ThoraxData_Labels = [
    "thoraxJoint_xThorax.q",
    "thoraxJoint_xThorax.qd",
    "thoraxJoint_yThorax.q",
    "thoraxJoint_yThorax.qd",
    "thoraxJoint_zThorax.q",
    "thoraxJoint_zThorax.qd",
    "thoraxJoint_forwardTilt.q",
    "thoraxJoint_forwardTilt.qd",
    "thoraxJoint_sideTilt.q",
    "thoraxJoint_sideTilt.qd",
    "thoraxJoint_internalRotation.q",
    "thoraxJoint_internalRotation.qd"
]

ThoraxDataQ_Labels = [
    "thoraxJoint_xThorax.q",
    "thoraxJoint_yThorax.q",
    "thoraxJoint_zThorax.q",
    "thoraxJoint_forwardTilt.q",
    "thoraxJoint_sideTilt.q",
    "thoraxJoint_internalRotation.q"
]

ThoraxDataQD_Labels = [
    "thoraxJoint_xThorax.qd",
    "thoraxJoint_yThorax.qd",
    "thoraxJoint_zThorax.qd",
    "thoraxJoint_forwardTilt.qd",
    "thoraxJoint_sideTilt.qd",
    "thoraxJoint_internalRotation.qd"
]

ShoulderData_Labels = [
    "shoulderJointRight_flexion.q",
    "shoulderJointRight_flexion.qd",
    "shoulderJointRight_abduction.q",
    "shoulderJointRight_abduction.qd",
    "shoulderJointRight_internalRotation.q",
    "shoulderJointRight_internalRotation.qd",
    "shoulderJointLeft_flexion.q",
    "shoulderJointLeft_flexion.qd",
    "shoulderJointLeft_abduction.q",
    "shoulderJointLeft_abduction.qd",
    "shoulderJointLeft_internalRotation.q",
    "shoulderJointLeft_internalRotation.qd"
]

ShoulderDataQ_Labels = [
    "shoulderJointRight_flexion.q",
    "shoulderJointRight_abduction.q",
    "shoulderJointRight_internalRotation.q",
    "shoulderJointLeft_flexion.q",
    "shoulderJointLeft_abduction.q",
    "shoulderJointLeft_internalRotation.q"
]

ShoulderDataQD_Labels = [
    "shoulderJointRight_flexion.qd",
    "shoulderJointRight_abduction.qd",
    "shoulderJointRight_internalRotation.qd",
    "shoulderJointLeft_flexion.qd",
    "shoulderJointLeft_abduction.qd",
    "shoulderJointLeft_internalRotation.qd"
]

ElbowData_Labels = [
    "elbowJointRight_flexion.q",
    "elbowJointRight_flexion.qd",
    "elbowJointLeft_flexion.q",
    "elbowJointLeft_flexion.qd"
]

ElbowDataQ_Labels = [
    "elbowJointRight_flexion.q",
    "elbowJointLeft_flexion.q"
]

ElbowDataQD_Labels = [
    "elbowJointRight_flexion.qd",
    "elbowJointLeft_flexion.qd"
]

WristData_Labels = [
    "wristJointRight_flexion.q",
    "wristJointRight_flexion.qd",
    "wristJointRight_radialUlnarDeviation.q",
    "wristJointRight_radialUlnarDeviation.qd",
    "wristJointRight_pronation/supination.q",
    "wristJointRight_pronation/supination.qd",
    "wristJointLeft_flexion.q",
    "wristJointLeft_flexion.qd",
    "wristJointLeft_radialUlnarDeviation.q",
    "wristJointLeft_radialUlnarDeviation.qd",
    "wristJointLeft_pronation/supination.q",
    "wristJointLeft_pronation/supination.qd"
]

WristDataQ_Labels = [
    "wristJointRight_flexion.q",
    "wristJointRight_radialUlnarDeviation.q",
    "wristJointRight_pronation/supination.q",
    "wristJointLeft_flexion.q",
    "wristJointLeft_radialUlnarDeviation.q",
    "wristJointLeft_pronation/supination.q"
]

WristDataQD_Labels = [
    "wristJointRight_flexion.qd",
    "wristJointRight_radialUlnarDeviation.qd",
    "wristJointRight_pronation/supination.qd",
    "wristJointLeft_flexion.qd",
    "wristJointLeft_radialUlnarDeviation.qd",
    "wristJointLeft_pronation/supination.qd"
]


if __name__ == "__main__":
    print("Number of total features: {0}".format(len(KinData_Dict)))
    print(" > Hip        : {0}".format(len(HipData_Labels)))
    print(" > Knee       : {0}".format(len(KneeData_Labels)))
    print(" > Ankle      : {0}".format(len(AnkleData_Labels)))
    print(" > Head       : {0}".format(len(HeadData_Labels)))
    print(" > Thorax     : {0}".format(len(ThoraxData_Labels)))
    print(" > Shoulder   : {0}".format(len(ShoulderData_Labels)))
    print(" > Elbow      : {0}".format(len(ElbowData_Labels)))
    print(" > Wrist      : {0}".format(len(WristData_Labels)))
