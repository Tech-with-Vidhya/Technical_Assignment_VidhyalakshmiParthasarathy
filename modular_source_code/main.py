# Identificaton of Data Quality Issues in the Parquet Files of the Scrape Appearances Dataset and the Competitor Appearances Dataset

# Importing the Python Libraries

import os

import boto3

import pyarrow.parquet as pq
import pandas as pd

import datetime
import time

import math

# Importing the Configuration Parameters

from config import AWS_S3_BUCKET_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
from config import scrape_key, competitor_key
from config import output_directory
from config import scrape_unique_primary_key_list, comptt_unique_primary_key_list
from config import format
from config import device_supported_values_list
from config import search_term_max_char, domain_max_char
from config import scrape_count_min_int
from config import spon_appr_min_count, spon_appr_max_count, appr_min_count, appr_max_count
from config import ctr_min_prob, ctr_max_prob

# Importing the Modular Source Codes

from s3_bucket_list import s3_bucket_list
from parquet_file_schema_generator import parquet_file_schema_generator
from parquet_file_dataframe_converter import parquet_file_dataframe_converter
from parquet_null_values_checks import parquet_null_values_checks
from parquet_non_ascii_characters_checks import parquet_non_ascii_characters_checks
from parquet_primary_key_duplicate_data_instances import parquet_primary_key_duplicate_data_instances
from parquet_device_supported_values_checks import parquet_device_supported_values_checks
from parquet_max_chars_deviation_checks import parquet_max_chars_deviation_checks
from parquet_date_format_checks import parquet_date_format_checks
from parquet_scrape_count_min_int_checks import parquet_scrape_count_min_int_checks
from parquet_min_max_deviation_checks import parquet_min_max_deviation_checks


# Defining the Main Function for the Program Execution

def main():
    print("Identificaton of Data Quality Issues in the Parquet Files of the Scrape Appearances Dataset and the Competitor Appearances Dataset\n")
    
    print("---------------------------Execution Started---------------------------")
    
    start_time = time.time()
    
    print("Execution Start Time: {}".format(start_time))
    
     # ---------------------------------------------EXTRACTION OF PARQUET FILES FROM SCRAPE APPEARANCES S3 BUCKET------------------------------------------------
    
    # Scrape Appearances S3 Bucket - Parquet Files Objects List
    #print("Scrape Appearances S3 Bucket Details")
    scrape_s3_bucket_full_uri, scrape_bucket_list_length, scrape_bucket_files_list = s3_bucket_list(AWS_S3_BUCKET_URI, AWS_ACCESS_KEY_ID,                                                                                                                  AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, scrape_key)                                                                                           
    #print(scrape_bucket_list)
    
    # Writing the Scrape Appearances S3 Bucket Details to a Text File
    with open(os.path.join(output_directory, 'scrape_appearances_s3_bucket_details.csv'), 'w') as f1:
        f1.write("Scrape Appearances S3 Bucket Details\n")
        f1.write("\nS3 Bucket Fully Qualified URI: {}\n".format(scrape_s3_bucket_full_uri))
        f1.write("\nTotal Number of Files in the Bucket: {}\n".format(str(scrape_bucket_list_length)))
        f1.write("\nList of Parquet Files:\n")
        for file in scrape_bucket_files_list:   
            f1.write(file)
            f1.write("\n")
        f1.close()
        
    # ---------------------------------------------EXTRACTION OF PARQUET FILES FROM COMPETITOR APPEARANCES S3 BUCKET------------------------------------------------
    
    # Competitor Appearances S3 Bucket - Parquet Files Objects List
    #print("\nCompetitor Appearances S3 Bucket Details")
    competitor_s3_bucket_full_uri, competitor_bucket_list_length, competitor_bucket_files_list = s3_bucket_list(AWS_S3_BUCKET_URI, AWS_ACCESS_KEY_ID,                                                                                                                  AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, competitor_key)
    #print(competitor_bucket_list)
    
    # Writing the Competitor Appearances S3 Bucket Details to a Text File
    with open(os.path.join(output_directory, 'competitor_appearances_s3_bucket_details.csv'), 'w') as f2:
        f2.write("Competitor Appearances S3 Bucket Details\n")
        f2.write("\nS3 Bucket Fully Qualified URI: {}\n".format(competitor_s3_bucket_full_uri))
        f2.write("\nTotal Number of Files in the Bucket: {}\n".format(str(competitor_bucket_list_length)))
        f2.write("\nList of Parquet Files:\n")
        for file in competitor_bucket_files_list:   
            f2.write(file)
            f2.write("\n")
        f2.close()
        
    # ---------------------------------------------SCRAPE APPEARANCES - DATA QUALITY TESTS EXECUTION------------------------------------------------
    
    # Execution of the Data Quality Tests for Scrape Appearances Parquet Files    
    for pfile in scrape_bucket_files_list:
        pfile_s3_path = f"{scrape_s3_bucket_full_uri}/{pfile}"
        
        # Data Quality Test 1 - Schema Validations
        scrape_pfile_table, scrape_pfile_name, scrape_pfile_attributes, scrape_pfile_schema = parquet_file_schema_generator(output_directory, pfile_s3_path)
        
        # Data Quality Test 2 - DataFrame Validations
        scrape_pfile_df = parquet_file_dataframe_converter(output_directory, pfile_s3_path, scrape_pfile_table)
        
        # Data Quality Test 3 - Null (NaN) Validations
        scrape_attribute_null_values_count_list, scrape_null_values_df_list = parquet_null_values_checks(output_directory, pfile_s3_path, scrape_pfile_df)
        
        # Data Quality Test 4 - Non-ASCII Characters Validations
        scrape_non_ascii_count_list, scrape_non_ascii_df_list = parquet_non_ascii_characters_checks(output_directory, pfile_s3_path, scrape_pfile_df)
        
        # Data Quality Test 5 - Unique Primary Key Combination - Duplicate Data Validations
        scrape_duplicate_data_instances_count, scrape_duplicate_data_instances_df = parquet_primary_key_duplicate_data_instances(output_directory, pfile_s3_path,                                                                                              scrape_pfile_df, unique_primary_key_list=scrape_unique_primary_key_list)
        
        # Data Quality Test 6 - Date Format Validations
        scrape_date_invalid_format_list, scrape_date_invalid_format_df_list, scrape_date_invalid_format_df_count_list = parquet_date_format_checks(output_directory,                                                                                                       pfile_s3_path, scrape_pfile_df, format, data_attribute='date')
        
        # Data Quality Test 7 - Device Supported Values Validations
        scrape_pfile_device_values_list, scrape_device_unsupported_df = parquet_device_supported_values_checks(output_directory, pfile_s3_path, scrape_pfile_df,                                                                                                                    device_supported_values_list) 
                                                                                          
        # Data Quality Test 8a - Search Term Maximum Allowable Characters Deviation Validations
        scrape_st_max_char_deviation_data_instances_count, scrape_st_max_char_deviation_data_instances_df = parquet_max_chars_deviation_checks(output_directory,                                                                         pfile_s3_path, scrape_pfile_df, max_char=search_term_max_char, data_attribute='search_term')
        
        # Data Quality Test 9 - Scrape Count Minimum Acceptable Values Deviation Validations
        scrape_min_scrape_count_deviation_data_instances_count, scrape_min_scrape_count_deviation_data_instances_df = parquet_scrape_count_min_int_checks(output_directory, pfile_s3_path, scrape_pfile_df, min_count=scrape_count_min_int, data_attribute='scrape_count')              
        
    
    # ---------------------------------------------COMPETITOR APPEARANCES - DATA QUALITY TESTS EXECUTION------------------------------------------------
        
    # Execution of the Data Quality Tests for Competitor Appearances Parquet Files 
    for pfile in competitor_bucket_files_list:
        pfile_s3_path = f"{competitor_s3_bucket_full_uri}/{pfile}"
        
        # Data Quality Test 1 - Schema Validations
        comptt_pfile_table, comptt_pfile_name, comptt_pfile_attributes, comptt_pfile_schema = parquet_file_schema_generator(output_directory, pfile_s3_path)
        
        # Data Quality Test 2 - DataFrame Validations
        comptt_pfile_df = parquet_file_dataframe_converter(output_directory, pfile_s3_path, comptt_pfile_table)
        
        # Data Quality Test 3 - Null (NaN) Validations
        comptt_attribute_null_values_count_list, comptt_null_values_df_list = parquet_null_values_checks(output_directory, pfile_s3_path, comptt_pfile_df)
        
        # Data Quality Test 4 - Non-ASCII Characters Validations
        comptt_non_ascii_count_list, comptt_non_ascii_df_list = parquet_non_ascii_characters_checks(output_directory, pfile_s3_path, comptt_pfile_df)
        
        # Data Quality Test 5 - Unique Primary Key Combination - Duplicate Data Validations
        comptt_duplicate_data_instances_count, comptt_duplicate_data_instances_df = parquet_primary_key_duplicate_data_instances(output_directory, pfile_s3_path,                                                                                              comptt_pfile_df, unique_primary_key_list=comptt_unique_primary_key_list)
        
        # Data Quality Test 6 - Date Format Validations
        comptt_date_invalid_format_list, comptt_date_invalid_format_df_list, comptt_date_invalid_format_df_count_list = parquet_date_format_checks(output_directory,                                                                                                       pfile_s3_path, comptt_pfile_df, format, data_attribute='date')
        
        # Data Quality Test 7 - Device Supported Values Validations
        comptt_pfile_device_values_list, comptt_device_unsupported_df = parquet_device_supported_values_checks(output_directory, pfile_s3_path, comptt_pfile_df,                                                                                                                    device_supported_values_list) 
                                                                                          
        # Data Quality Test 8a - Search Term Maximum Allowable Characters Deviation Validations
        comptt_st_max_char_deviation_data_instances_count, comptt_st_max_char_deviation_data_instances_df = parquet_max_chars_deviation_checks(output_directory,                                                                         pfile_s3_path, comptt_pfile_df, max_char=search_term_max_char, data_attribute='search_term')
        
        # Data Quality Test 8b - Domain Maximum Allowable Characters Deviation Validations
        comptt_dom_max_char_deviation_data_instances_count, comptt_dom_max_char_deviation_data_instances_df = parquet_max_chars_deviation_checks(output_directory,                                                                         pfile_s3_path, comptt_pfile_df, max_char=domain_max_char, data_attribute='domain')  
        
        
        # Data Quality Test 10a - Sponsored Appearances - Minimum and Maximum Values Deviation Validations
        comptt_spon_appr_min_int_deviation_data_instances_df, comptt_spon_appr_max_int_deviation_data_instances_df =               parquet_min_max_deviation_checks(output_directory, pfile_s3_path, comptt_pfile_df, min_count=spon_appr_min_count, max_count=spon_appr_max_count, 
                                                                                                         data_attribute='sponsored_appearances') 
        
        # Data Quality Test 10b - Natural Appearances - Minimum and Maximum Values Deviation Validations
        comptt_nat_appr_min_int_deviation_data_instances_df, comptt_nat_appr_max_int_deviation_data_instances_df =                   parquet_min_max_deviation_checks(output_directory, pfile_s3_path, comptt_pfile_df, min_count=appr_min_count, max_count=appr_max_count, 
                                                                                                 data_attribute='natural_appearances')   
                
        # Data Quality Test 10c - Pla Appearances - Minimum and Maximum Values Deviation Validations
        comptt_pla_appr_min_int_deviation_data_instances_df, comptt_pla_appr_max_int_deviation_data_instances_df =                         parquet_min_max_deviation_checks(output_directory, pfile_s3_path, comptt_pfile_df, min_count=appr_min_count, max_count=appr_max_count, 
                                                                                                     data_attribute='pla_appearances')
            
        # Data Quality Test 10d - ctr Probability - Minimum and Maximum Values Deviation Validations
        comptt_ctr_prob_min_deviation_data_instances_df, comptt_ctr_prob_max_deviation_data_instances_df =               parquet_min_max_deviation_checks(output_directory, pfile_s3_path, comptt_pfile_df, min_count=ctr_min_prob, max_count=ctr_max_prob, data_attribute='ctr') 
                                                                                                            
        
    print("---------------------------Execution Completed---------------------------")
    
    end_time = time.time()
    
    print("Execution End Time: {}".format(end_time))
    
    print("Total Execution Time: {} Seconds".format(end_time-start_time))
    
if __name__ == "__main__":
    main()