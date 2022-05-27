# Function to Verify the Deviation in the Minimum and Maximum Allowable Count of the Given Data Attributes in Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition


def parquet_min_max_deviation_checks(output_directory, pfile_s3_path, pfile_df, min_count, max_count, data_attribute):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("---------------------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 10 - DEVIATIONS IN THE MINIMUM AND MAXIMUM ALLOWABLE COUNT OF THE GIVEN DATA ATTRIBUTE - VALIDATIONS *****\n")
        f.write("---------------------------------------------------------------------------------------------------------------------------------------------\n")
        
        f.write("Attribute '{}':\n".format(data_attribute))
        
        pfile_min_actual_value = pfile_df[data_attribute].min()
        pfile_max_actual_value = pfile_df[data_attribute].max()
        
        # Extracting the Data Instances and it's Count that Deviates the Actual Acceptable Minimum Value
        min_deviation_data_instances_df = pfile_df[pfile_df[data_attribute] < min_count]
        min_deviation_data_instances_count = min_deviation_data_instances_df.shape[0]
        
        # Extracting the Data Instances and it's Count that Deviates the Actual Acceptable Maximum Value
        max_deviation_data_instances_df = pfile_df[pfile_df[data_attribute] > max_count]
        max_deviation_data_instances_count = max_deviation_data_instances_df.shape[0]
        
        f.write("Actual Minimum Value of the Data Attribute '{0}' in the Parquet File '{1}:'\n{2}\n\n".format(data_attribute, pfile_name, pfile_min_actual_value))
        f.write("Actual Maximum Value of the Data Attribute '{0}' in the Parquet File '{1}:'\n{2}\n\n".format(data_attribute, pfile_name, pfile_max_actual_value))
        
        if min_deviation_data_instances_count == 0:
            f.write("There are no Data Instances for the Data Attribute '{0}' that Deviated the Minimum Allowable Count of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, min_count, pfile_name))      
            f.write("{}".format(min_deviation_data_instances_df))
            f.write('\n\n')
            
        else:
            f.write("Total Number of Data Instances for the Data Attribute '{0}' that Deviated the Minimum Allowable Count of {1} in the Parquet File '{2}':\n{3}\n\n" .format(data_attribute, min_count, pfile_name, min_deviation_data_instances_count))                                                                       
            f.write("Below are the {0} Data Instances that Deviated the Minimum Allowable Count of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, min_count, pfile_name))                                                                 
            f.write("{}".format(min_deviation_data_instances_df))
            f.write('\n\n')
            
        if max_deviation_data_instances_count == 0:
            f.write("There are no Data Instances for the Data Attribute '{0}' that Deviated the Maximum Allowable Count of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, max_count, pfile_name))      
            f.write("{}".format(max_deviation_data_instances_df))
            f.write('\n\n')
            
        else:
            f.write("Total Number of Data Instances for the Data Attribute '{0}' that Deviated the Maximum Allowable Count of {1} in the Parquet File '{2}':\n{3}\n\n".format(data_attribute, max_count, pfile_name, max_deviation_data_instances_count))                                                                   
            f.write("Below are the {0} Data Instances that Deviated the Maximum Allowable Count of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, max_count, pfile_name))                                                                 
            f.write("{}".format(max_deviation_data_instances_df))
            f.write('\n\n')
                
        
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
        
    return min_deviation_data_instances_df, max_deviation_data_instances_df