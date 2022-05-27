# Function to Generate the Schema from the Parquet File

# Importing the Python Libraries

import os

import pyarrow.parquet as pq

# Function Definition

def parquet_file_schema_generator(output_directory, pfile_s3_path):
    
    # Reading the Parquet File in a Python Variable
    #pfile = pq.ParquetFile(pfile_s3_path)
    
    # Creating an Instance of the Parquet Table for the Parquet File 
    pfile_table = pq.read_table(pfile_s3_path)
    
    #print("Parquet File S3 Path: \n{}\n".format(pfile_s3_path))
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Extracting the Data Attributes from the Pre-Defined Schema of the Parquet File
    pfile_attributes = pfile_table.column_names
    #print("Parquet File - Data Attributes: \n{}\n".format(pfile_attributes))
        
    # Extracting the Pre-Defined Schema of the Parquet File
    pfile_schema = pfile_table.schema
    #print("Parquet File - Data Schema: \n{}\n".format(pfile_schema))
    
    # Extracting the Metadata from the Pre-Defined Schema of the Parquet File
    #pfile_metadata = pq.read_metadata(pfile)
    #pfile_metadata = pfile.metadata
    #print("Parquet File - Metadata: \n{}\n".format(pfile_metadata))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'w') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 1 - SCHEMA VALIDATIONS *****\n\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("Parquet File S3 Path: \n{}\n\n".format(pfile_s3_path))
        f.write("Parquet File Dataset Name: \n{}\n\n".format(pfile_dataset_name))
        f.write("Parquet File - Data Attributes: \n{}\n\n".format(pfile_attributes))
        f.write("Parquet File - Data Schema: \n{}\n\n".format(pfile_schema))
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
    
    return pfile_table, pfile_name, pfile_attributes, pfile_schema