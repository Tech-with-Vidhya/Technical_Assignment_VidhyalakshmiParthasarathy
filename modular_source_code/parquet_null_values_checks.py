# Function to Verify the Presence of Null (NaN and None) Values in the Data Attributes of the Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition

def parquet_null_values_checks(output_directory, pfile_s3_path, pfile_df):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 3 - NULL (NaN and None) VALUES CHECKS AND VALIDATIONS *****\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        
        # Creating an Empty List to Store the Null Values Count for Each Data Attribute
        attribute_null_values_count_list = []
        
        # Creating an Empty List to Store the Individual Filtered DataFrames (that Contain Null Values) for Each Data Attribute
        null_values_df_list = []
        
        for col in pfile_df.columns:
            attribute_null_values_count = pfile_df[col].isna().sum()
            if attribute_null_values_count == 0:
                f.write("Attribute '{}':\n".format(col))
                null_values_df = pfile_df[pfile_df[col].isnull()]
                f.write("There are no Null Values found for the Attribute '{0}' in the Parquet File '{1}'.\n\n".format(col, pfile_name))
                f.write("{}".format(null_values_df))
                
                '''
                with open(os.path.join(output_directory, '{0}_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as fw:
                    csv_writer = csv.writer(fw, delimiter=',')
                    for line in null_values_df:
                        csv_writer.writerow(line)
                '''
                f.write('\n\n')
            else:
                f.write("Attribute '{}':\n".format(col))
                null_values_df = pfile_df[pfile_df[col].isnull()]
                f.write("\nTotal Number of Null Values: {}\n\n".format(attribute_null_values_count))
                f.write("Below are the Filtered Data Instances of the {0} Null Values found for the Attribute '{1}' in the Parquet File '{2}'.\n\n". 
                        format(attribute_null_values_count, col, pfile_name))                                                                                         
                f.write("{}\n\n".format(null_values_df))
                if col == 'ctr':
                    f.write("There are No Data Quality Issues as Null Values are Acceptable for the Attribute 'ctr'\n")
                
                '''
                with open(os.path.join(output_directory, '{0}_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as fw:
                    csv_writer = csv.writer(fw, delimiter=',')
                    for line in null_values_df:
                        csv_writer.writerow(line)
                '''
                f.write('\n\n')
                
            attribute_null_values_count_list.append(attribute_null_values_count)
            null_values_df_list.append(null_values_df)
            
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
            
    return attribute_null_values_count_list, null_values_df_list
    