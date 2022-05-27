# Main Program - Parameters Configuration

# Importing the Python Libraries

import os
import math

# AWS Parameters Configuration

AWS_S3_BUCKET_URI = 'adthena.data.qa.test'
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")

# Datasets Key Configuration

scrape_key = 'scrape_appearances'
competitor_key = 'competitor_appearances'

# Output Files Parameter Configuration

output_directory = "/Users/vidhyalakshmiparthasarathy/.CMVolumes/Google-Drive-pbvidhyauk/Technical_Assignment_VidhyalakshmiParthasarathy/output_final/"

# Primary Key Parameters Configuration

scrape_unique_primary_key_list = ['search_term', 'date', 'device']
comptt_unique_primary_key_list = ['search_term', 'date', 'device', 'domain']

# Data Format Parameters Configuration

format = "%Y-%m-%d"

# Device Supported Values Parameter Configuration

device_supported_values_list = ['desktop', 'mobile']

# Search Term Maximum Characters Parameter Configuration

search_term_max_char = 400

# Domain Maximum Characters Parameter Configuration

domain_max_char = 100

# Scrape Count Minimum Count Parameter Configuration

scrape_count_min_int = 1

# Sponsored Appearances Minimum Count and Maximum Count Parameters Configuration

spon_appr_min_count = 0
spon_appr_max_count = 26      # Calculated as 25 from Scrape Appearances Consolidated Dataset Including all 20 Parquet Files. 
                              # But Set as 26 for Evaluating the Maximum Value Deviation in the Corresponding Modular Programming Function

# Natural Appearances and Pla Appearances Minimum Count and Maximum Count Parameters Configuration

appr_min_count = 0
appr_max_count = math.inf

# ctr (Probability that Someone will Click an Advert) Minimum Count and Maximum Count Parameters Configuration

ctr_min_prob = 0.0
ctr_max_prob = 1.0

