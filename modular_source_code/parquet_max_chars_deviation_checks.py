# Function to Verify the Deviation in the Maximum Allowable Characters Length of the Given Data Attribute in Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition

def parquet_max_chars_deviation_checks(output_directory, pfile_s3_path, pfile_df, max_char, data_attribute):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("--------------------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 8 - DEVIATIONS IN THE MAXIMUM ALLOWABLE CHARACTERS LENGTH OF THE GIVEN DATA ATTRIBUTE - VALIDATIONS *****\n")
        f.write("--------------------------------------------------------------------------------------------------------------------------------------------\n")
        
        f.write("Attribute '{}':\n".format(data_attribute))
        
        max_char_deviation_data_instances_df = pfile_df[pfile_df[data_attribute].apply(lambda attribute: len(str(attribute)) > max_char)]
        max_char_deviation_data_instances_count = max_char_deviation_data_instances_df.shape[0]
        
        if max_char_deviation_data_instances_count == 0:
            f.write("There are no Data Instances for the Data Attribute '{0}' that Deviated the Maximum Allowable Characters Length of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, max_char, pfile_name))      
            f.write("{}".format(max_char_deviation_data_instances_df))
            f.write('\n\n')
            
        else:
            f.write("Total Number of Data Instances for the Data Attribute '{0}' that Deviated the Maximum Allowable Characters Length of {1}:\n{2}\n\n". 
                    format(data_attribute, max_char, max_char_deviation_data_instances_count))                                                                         
            f.write("Below are the {0} Data Instances that Deviated the Maximum Allowable Characters Length of {1} in the Parquet File '{2}'. \n\n". 
                    format(max_char_deviation_data_instances_count, max_char, pfile_name))                                                                 
            f.write("{}".format(max_char_deviation_data_instances_df))
            f.write('\n\n')
                
        
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
        
    return max_char_deviation_data_instances_count, max_char_deviation_data_instances_df
        
    
    