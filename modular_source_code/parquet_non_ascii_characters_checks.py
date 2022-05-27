# Function to Verify the Presence of Non-ASCII Characters in the String Type Data Attributes of the Parquet File

# Importing the Python Libraries

import os

import csv

import pandas as pd

# Function Definition

def parquet_non_ascii_characters_checks(output_directory, pfile_s3_path, pfile_df):
    
    pfile_name = pfile_s3_path.split('/')[-1]
    #print("Parquet File Name: \n{}\n".format(pfile_name))
    
    pfile_dataset_name = pfile_s3_path.split('/')[-2]
    #print("Parquet File Dataset Name: \n{}\n".format(pfile_dataset_name))
    
    # Writing the Data Quality Test Results to a Text File
    with open(os.path.join(output_directory, '{0}_DQReport_{1}.csv'.format(pfile_dataset_name, pfile_name)), 'a') as f:
        f.write("-----------------------------------------------------------------------------------------------------\n")
        f.write("***** DATA QUALITY TEST 4 - NON-ASCII CHARACTERS CHECKS AND VALIDATIONS *****\n")
        f.write("-----------------------------------------------------------------------------------------------------\n")
        
        # Creating an Empty List to Store the String Data Type Attributes
        string_attributes = []
        
        # Creating an Empty List to Store the Non-ASCII Text Count for Each String Type Attribute
        non_ascii_count_list = []
        
        # Creating an Empty List to Store the Individual Filtered DataFrames (that Contain Non-ASCII Text) for Each String Type Attribute
        non_ascii_df_list = []
        
        # Extracting the List of String Data Type Attributes from the Parquet DataFrame
        for col in pfile_df.columns:
            if (pfile_df[col].dtypes == 'O') and (col != 'date'):
                string_attributes.append(col)
                
        for str_col in string_attributes:
            non_ascii_count = 0
            for text in pfile_df[str_col]:
                if text == None:
                    rev_text = 'nonetext'
                else:
                    rev_text = text
                if rev_text.isascii() == False:
                    non_ascii_count += 1
            if non_ascii_count == 0:
                f.write("Attribute '{}':\n".format(str_col))
                revised_pfile_df = pfile_df[~pfile_df[str_col].isnull()]
                non_ascii_df = revised_pfile_df[revised_pfile_df[str_col].apply(lambda text: text.isascii() == False)]
                f.write("There are no Non-ASCII String Values found for the Attribute '{0}' in the Parquet File '{1}'.\n\n".format(str_col, pfile_name))
                f.write("{}".format(non_ascii_df))
                f.write('\n\n')
            else:
                f.write("Attribute '{}':\n".format(str_col))
                revised_pfile_df = pfile_df[~pfile_df[str_col].isnull()]
                non_ascii_df = revised_pfile_df[revised_pfile_df[str_col].apply(lambda text: text.isascii() == False)]
                f.write("Total Number of Non-ASCII String Values: {}\n\n".format(non_ascii_count))
                f.write("Below are the Filtered Data Instances of the {0} Non-ASCII String Values found for the Attribute '{1}' in the Parquet File '{2}'.\n\n". 
                        format(non_ascii_count, str_col, pfile_name))
                f.write("{}".format(non_ascii_df))
                f.write('\n\n')
            
            non_ascii_count_list.append(non_ascii_count)
            non_ascii_df_list.append(non_ascii_df)
            
        f.write("-----------------------------------------------------------------------------------------------------\n\n")
        f.close()
            
    return non_ascii_count_list, non_ascii_df_list
        
    

            
        
        
                