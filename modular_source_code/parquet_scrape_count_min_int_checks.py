# Function to Verify the Deviation in the Minimum Allowable Integer Count of the Scrape Count Attribute in Each Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition


def parquet_scrape_count_min_int_checks(output_directory, pfile_s3_path, pfile_df, min_count, data_attribute):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 9 - DEVIATIONS IN THE MINIMUM ALLOWABLE INTEGER COUNT OF THE SCRAPE COUNT DATA ATTRIBUTE - VALIDATIONS *****\n")
        f.write("-----------------------------------------------------------------------------------------------------------------------------------------------\n")
        
        min_scrape_count_deviation_data_instances_df = pfile_df[pfile_df[data_attribute] < min_count]
        min_scrape_count_deviation_data_instances_count = min_scrape_count_deviation_data_instances_df.shape[0]
        
        if min_scrape_count_deviation_data_instances_count == 0:
            f.write("There are no Data Instances for the Data Attribute '{0}' that Deviated the Minimum Allowable Scrape Count of {1} in the Parquet File '{2}'. \n\n".format(data_attribute, min_count, pfile_name))      
            f.write("{}".format(min_scrape_count_deviation_data_instances_df))
            f.write('\n\n')
            
        else:
            f.write("Total Number of Data Instances for the Data Attribute '{0}' that Deviated the Minimum Allowable Scrape Count of {1}:\n{2}\n\n". 
                    format(data_attribute, min_count, min_scrape_count_deviation_data_instances_count))                                                               
            f.write("Below are the {0} Data Instances that Deviated the Minimum Allowable Scrape Count of {1} in the Parquet File '{2}'. \n\n". 
                    format(min_scrape_count_deviation_data_instances_count, min_count, pfile_name))                                                                 
            f.write("{}".format(min_scrape_count_deviation_data_instances_df))
            f.write('\n\n')
                
        
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
        
    return min_scrape_count_deviation_data_instances_count, min_scrape_count_deviation_data_instances_df
        
        