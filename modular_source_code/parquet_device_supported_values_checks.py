# Function to Verify the Supported Values of the 'device' Data Attribute in Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition

def parquet_device_supported_values_checks(output_directory, pfile_s3_path, pfile_df, device_supported_values_list):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 7 - UNIQUE VALUES SUPPORTED BY THE DEVICE DATA ATTRIBUTE - VALIDATIONS *****\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        
        # Extracting the List of the Unique Values of the 'device' Data Attribute in the Parquet File
        pfile_device_values_list = [dev for dev in pfile_df['device'].unique()]
        
        # Extracting the Count of the Suported Values of the 'device' Data Attribute in the Parquet File
        pfile_device_supported_values_count = len(pfile_device_values_list)
        
        # Creating an Empty List to Store the Unsupported Device Values Identified in the Parquet File
        pfile_unsupported_device_values_list = []
        
        for dev in pfile_device_values_list:
            if dev not in device_supported_values_list:
                pfile_unsupported_device_values_list.append(dev)
                
        pfile_unsupported_device_values_count = len(pfile_unsupported_device_values_list)
        
        device_unsupported_list = ~pfile_df['device'].isin(device_supported_values_list)
        device_unsupported_df = pfile_df[device_unsupported_list]
        
        device_unsupported_data_instances_count = device_unsupported_df.shape[0]
                
        if pfile_unsupported_device_values_count == 0:
            f.write("There are no New UnSupported Device Values found for the Attribute 'device' in the Parquet File '{}'.\n\n".format(pfile_name))
            f.write("\nTotal Number of Existing Supported Device Values: {}\n\n".format(pfile_device_supported_values_count))
            f.write("\nList of Existing Supported Device Values: {}\n\n".format(pfile_device_values_list))
            f.write('\n\n')
        else:
            f.write("\nTotal Number of New UnSupported Device Values: {}\n\n".format(pfile_unsupported_device_values_count))
            f.write("\nList of New UnSupported Device Values: {}\n\n".format(pfile_unsupported_device_values_list))
            f.write("Below are the {0} Filtered Data Instances for the {1} New UnSupported Device Values found for the Attribute 'device' in the Parquet File '{2}'. \n\n".format(device_unsupported_data_instances_count, pfile_unsupported_device_values_count, pfile_name))
            f.write("{}".format(device_unsupported_df))
            f.write('\n\n')
            
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
        
    return pfile_device_values_list, device_unsupported_df
                