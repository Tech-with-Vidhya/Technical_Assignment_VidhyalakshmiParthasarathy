# Function to Verify the Date Format of the Date Attribute for Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

import datetime

# Function Definition

def parquet_date_format_checks(output_directory, pfile_s3_path, pfile_df, format, data_attribute):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 6 - DATE ATTRIBUTE'S ACCEPTABLE DATE FORMAT - VALIDATIONS *****\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        
        # Extratcing the Unique Values of the Dates from the Parquet File
        date_array = pfile_df[data_attribute].unique()
        
        # Creating an Empty List to Store the Dates with the Valid Format in Each of the Parquet File
        date_valid_format_list = []
        
        # Creating an Empty List to Store the Dates with the Invalid Format in Each of the Parquet File
        date_invalid_format_list = []
        
        # Creating an Empty List to Store the Individual DataFrames of the Invalid Data Formats in Each of the Parquet File
        date_invalid_format_df_list = []
        
        # Creating an Empty List to Store the Count of the Data Instances with Invalid Date Format in the Individual DataFrames in Each of the Parquet File
        date_invalid_format_df_count_list = []
        
        for dt in date_array:
            dt_string = str(dt)
            try:
                datetime.datetime.strptime(dt_string, format)
                date_valid_format_list.append(dt_string)
                f.write("The Date '{0}' is in the Expected Format as '{1}' in the Parquet File '{2}'. \n\n".format(dt_string, format, pfile_name))
                f.write('\n\n')
            except ValueError:
                date_invalid_format_list.append(dt_string)
                
                if dt_string == 'None':
                    date_invalid_format_data_instances_df = pfile_df[pfile_df[data_attribute].isnull()]
                    date_invalid_format_data_instances_count = date_invalid_format_data_instances_df.shape[0]
                else:
                    date_invalid_format_data_instances_df = pfile_df[pfile_df[data_attribute] == dt]
                    date_invalid_format_data_instances_count = date_invalid_format_data_instances_df.shape[0]
                
                date_invalid_format_df_list.append(date_invalid_format_data_instances_df)
                date_invalid_format_df_count_list.append(date_invalid_format_data_instances_count)
                
                f.write("The Date '{0}' is Not in the Expected Format as '{1}' in the Parquet File '{2}'. \n\n".format(dt_string, format, pfile_name))
                f.write("Below are the {0} Data Instances where Date '{1}' is Not in the Expected Format as '{2}' in the Parquet File '{3}'. \n\n". 
                        format(date_invalid_format_data_instances_count, dt_string, format, pfile_name))                                                               
                f.write("{}".format(date_invalid_format_data_instances_df))
                f.write('\n\n')
            
        f.write("List of Dates with the Valid Format:\n{}\n\n".format(date_valid_format_list))
        f.write("List of Dates with the Invalid Format:\n{}\n\n".format(date_invalid_format_list))
                
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
                
    return date_invalid_format_list, date_invalid_format_df_list, date_invalid_format_df_count_list
            
            
    