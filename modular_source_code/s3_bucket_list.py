# Function to Extract the List of Objects (Parquet Files) from the S3 Bucket

# Importing the Python Libraries

import boto3

# Function Definition

def s3_bucket_list(AWS_S3_BUCKET_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, key):

    # Creating a boto3 Client Instance to access the S3 Bucket
    s3_client = boto3.client('s3')
    
    # Creating a boto3 S3 Resource Instance to access the S3 Bucket and its Objects
    s3 = boto3.resource(
                        's3',
                        aws_access_key_id = AWS_ACCESS_KEY_ID,
                        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )
    
    # Specifying the S3 Bucket Name
    s3_bucket_name = AWS_S3_BUCKET_URI
    #s3_bucket_name = 'adthena.data.qa.test'

    # Extracting the Name of the S3 Bucket
    my_bucket = s3.Bucket(s3_bucket_name)
    #print("S3 Bucket URI: '{}'".format(my_bucket.name))
    
    # Specifying the Key of the S3 Bucket
    bucket_key = key
    
    # Displaying the S3 Bucket Fully Qualified URI
    s3_bucket_full_uri = f"s3://{my_bucket.name}/{bucket_key}"
    #print("S3 Bucket Fully Qualified URI: {}".format(s3_bucket_full_uri))
    
    # Creating an Empty List to Store the Objects (Parquet Files) within the S3 Bucket
    bucket_files_list = []
    
    for file in my_bucket.objects.filter(Prefix = bucket_key):
        file_name = file.key.split('/')[1]
        if file_name.find(".parquet") != -1:
            bucket_files_list.append(file_name)
    bucket_list_length = len(bucket_files_list)
    #print("Total Number of Files in the Bucket: {}".format(bucket_list_length))
    
    return s3_bucket_full_uri, bucket_list_length, bucket_files_list
    
        
    