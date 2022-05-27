# Function to Convert the Parquet Table to a Pandas DataFrame

# Importing the Python Libraries

import os

import pyarrow.parquet as pq
import pandas as pd

# Function Definition

def parquet_file_dataframe_converter(output_directory, pfile_s3_path, pfile_table):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Converting the Parquet Table into a Pandas DataFrame
    pfile_df = pfile_table.to_pandas()
    #print("Parquet File - DataFrame: \n{}\n".format(pfile_df))
    
    # DataFrame Exploration and Statistics
    pfile_df_total_data_attributes = pfile_df.shape[1]
    pfile_df_total_data_instances = pfile_df.shape[0]
    pfile_df_datatypes = pfile_df.dtypes
    pfile_df_statistics = pfile_df.describe()
    
    #print("Total Number of Data Attributes in the Parquet DataFrame: \n{}\n".format(pfile_df_total_data_attributes))
    #print("Total Number of Data Instances in the Parquet DataFrame: \n{}\n".format(pfile_df_total_data_instances))
    #print("Data Types of the Attributes in the Parquet DataFrame: \n{}\n".format(pfile_df_datatypes))
    #print("Descriptive Statistics of the Parquet DataFrame: \n{}\n".format(pfile_df_statistics))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 2 - DATAFRAME VALIDATIONS *****\n\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("Parquet File - DataFrame: \n{}\n\n".format(pfile_df))
        f.write("Total Number of Data Attributes in the Parquet DataFrame: \n{}\n\n".format(pfile_df_total_data_attributes))
        f.write("Total Number of Data Instances in the Parquet DataFrame: \n{}\n\n".format(pfile_df_total_data_instances))
        f.write("Data Types of the Attributes in the Parquet DataFrame: \n{}\n\n".format(pfile_df_datatypes))
        f.write("Descriptive Statistics of the Parquet DataFrame: \n{}\n\n".format(pfile_df_statistics))
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
    
    return pfile_df
    