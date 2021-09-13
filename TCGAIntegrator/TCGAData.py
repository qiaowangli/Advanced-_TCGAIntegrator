#!/usr/bin/python2
from tcgaintegrator.BuildDataset import BuildDataset
from scipy.io import loadmat
import pandas as pd
# from pandas.api.types import is_string_dtype
import numpy as np
import sys


################################################################################
# API functions.
################################################################################
def loadData(Disease_type=None,**mode):
    if(Disease_type is None):
        Disease_type = "LGG"
    try:
        mode_type=mode['Mode']
    except KeyError as err:
        mode_type='SURVIVAL'
    try:
        Sample_num=int(mode['Sample'])
    except KeyError as err:
        Sample_num=-1

    Output = './'
    FirehosePath = None
    CancerCensusFile = None
    MutsigQ = 0.1
    GisticQ = 0.1
    BuildDataset(Output, FirehosePath, Disease_type, CancerCensusFile, MutsigQ, GisticQ)

    mat_file=str(Disease_type)+".Data.mat"
    return convertData(mat_file,Mode=mode_type,Sample=Sample_num)
    

###############################################################################
# Application functions.
################################################################################
def convertData(file_mat,**mode):
    try:
        mat = loadmat(file_mat)
    except:
        raise SyntaxError("Fatal Error: fail to open file.")
    
    ## THIS IS USED TO ACCLERATE YOUR PROCESSING TIME, PLS REMOVE IT TO ACCESS THE FULL DATASET WHEN YOU ARE READY
    #
    if(mode['Sample'] != -1):
        mat['Features']=mat['Features'][:int(mode['Sample'])]
        mat['Symbols']=mat['Symbols'][:int(mode['Sample'])]
    #
    ##

    # the feature dataframe
    df_feature= pd.DataFrame(mat['Features'].T,columns = mat["Symbols"])
    # the label dataframe
    try:
        if(mode['Mode']=='SURVIVAL'):
            df_label= pd.DataFrame(mat['Survival'][0].T, columns = ["LABEL"])
        elif(mode['Mode']=='CENSOR'):
            df_label= pd.DataFrame(mat['Censored'][0].T, columns = ["LABEL"])
        elif(mode['Mode']=='HYBRID'):
            df_Survival= pd.DataFrame(mat['Survival'][0].T, columns = ["Survival"])
            df_Censored= pd.DataFrame(mat['Censored'][0].T, columns = ["Censored"])
            sum_df= pd.concat([df_Survival, df_Censored], axis=1)
            sum_df.loc[sum_df['Censored'] == 0, 'LABEL'] = - sum_df['Survival']
            sum_df.loc[sum_df['Censored'] == 1, 'LABEL'] = sum_df['Survival']
            df_label= sum_df['LABEL'].copy()

    except KeyError as err:
        # DEFAULT MODE
        df_label= pd.DataFrame(mat['Survival'][0].T, columns = ["LABEL"])

    # Combine those two together
    metadata_df= pd.concat([df_feature, df_label], axis=1)

    ## YOU MAY WANT TO UNCOMMENT THIS LOOP TO CHECKOUT IF YOUR DF IS ALL NUMERIC.
    #
    # for index in metadata_df.columns:
    #     if (is_string_dtype(metadata_df[index])):
    #         print("opp we get one")
    ##

    # output metadata_df to csv
    #metadata_df.to_csv(file_mat + ".csv", index=False)
    return metadata_df

def main(file,*args):
    """
    Convert .mat to .csv
    """
    for arg in args:
        Mode = arg.split("=")[0]
        Action = arg.split("=")[1]

    if(Mode!='Mode'):
        raise SyntaxError("Insufficient arguments key.")
    
    if(Action=='HYBRID' or Action=='SURVIVAL' or Action=='CENSOR' ):
        convertData(file,Mode=Action)
    else:
        raise SyntaxError("Insufficient arguments value.")
    

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        main(sys.argv[1],*sys.argv[2:])
    else:
        raise SyntaxError("Insufficient arguments.")
    