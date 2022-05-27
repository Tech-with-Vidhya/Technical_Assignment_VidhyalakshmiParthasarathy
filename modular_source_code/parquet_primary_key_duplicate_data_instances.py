# Function to Detect the Presence of Duplicate Data Instances for the Combination of the Data Attributes Pre-Defined as Unique Primary Key in Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition

def parquet_primary_key_duplicate_data_instances(output_directory, pfile_s3_path, pfile_df, unique_primary_key_list):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("---------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 5 - UNIQUE PRIMARY KEY COMBINATION - DUPLICATE DATA CHECKS AND VALIDATIONS *****\n")
        f.write("---------------------------------------------------------------------------------------------------------------------------------\n")
        
        duplicate_data_instances_df = pfile_df[pfile_df.duplicated(subset=unique_primary_key_list, keep=False)]
        duplicate_data_instances_count = duplicate_data_instances_df.shape[0]
        
        if duplicate_data_instances_count == 0:
            f.write("There are no Duplicate Data Instances found for the Combination of the Unique Primary Key Data Attributes '{0}' in the Parquet File'{1}'.\n\n".                       format(unique_primary_key_list, pfile_name))      
            f.write("{}".format(duplicate_data_instances_df))
            f.write('\n\n')
            
        else:
            f.write("Total Number of Duplicate Data Instances: {}\n\n".format(duplicate_data_instances_count))
            f.write("Below are the {0} Duplicate Data Instances found for the Combination of the Unique Primary Key Data Attributes '{1}' in the Parquet File '{2}'.                       \n\n".format(duplicate_data_instances_count, unique_primary_key_list, pfile_name))                                                                 
            f.write("{}".format(duplicate_data_instances_df))
            f.write('\n\n')
                
        
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
        
    return duplicate_data_instances_count, duplicate_data_instances_df