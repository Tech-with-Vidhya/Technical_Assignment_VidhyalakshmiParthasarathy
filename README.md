# Technical_Assignment_VidhyalakshmiParthasarathy

# <font color='#0E1478'><center><u>**Identificaton of Data Quality Issues in the Parquet Files of the Scrape Appearances Dataset and the Competitor Appearances Dataset**</u></center></font>

## <u>**INTRODUCTION**</u>

### This project assignment task involves using Python as a programming language to look and analyse the data created in the AWS S3 Buckets, by performing data quality checks on the data and producing a summary report about the data quality findings.

<br>

## <u>**DATASETS**</u>

### The project involves two datasets namely Scrape Appearances and Competitor Appearances stored in the AWS S3 Buckets. Each dataset includes multiple files in parquet format.

<br>

### <u>**AWS S3 Bucket URIs are as follows:**</u>
* ### <b>Scrape Appearances S3 Bucket</b> - 's3://adthena.data.qa.test/scrape_appearances'
* ### <b>Competitor Appearances S3 Bucket</b> - 's3://adthena.data.qa.test/competitor_appearances'

<br>

### **Below are the high-level stats about the two datasets.**
### <u><b>Scrape Appearances S3 Bucket:</b></u>
> ### 1. Includes 20 Parquet Files
> ### 2. Includes 4 unique data attributes namely 'date', 'device', 'search_term' and 'scrape_count'
> ### 3. Data Attributes - Data Types Details:
    > * date: Date (YYYY-MM-DD)
    > * device: String
    > * search_term: String
    > * scrape_count: Int
> ### 4. Data Attributes - Constraints Details:
    > * Primary Key (unique): date, device, search_term
    > * device (non-NULL): only mobile and desktop are supported
    > * search_term (non-NULL): maximum 400 characters long
    > * scrape_count (non-NULL): > 0

<br>

### <u><b>Competitor Appearances S3 Bucket:</b></u>
> ### 1. Includes 40 Parquet Files in 2-part file format
> ### 2. Includes 8 unique data attributes namely 'date', 'device', 'search_term', 'domain', 'sponsored_appearances', 'natural_appearances', 'pla_appearances', 'ctr'
> ### 3. Data Attributes - Data Types Details:
    > * date: Date (YYYY-MM-DD)
    > * device: String.
    > * search_term: String
    > * domain: String
    > * sponsored_appearances: Int
    > * natural_appearances: Int
    > * pla_appearances: Int
    > * ctr: Double
> ### 4. Data Attributes - Constraints Details:
    > * Primary Key (unique): date, device, search_term, domain
    > * device (non-NULL): only mobile and desktop are supported
    > * search_term (non-NULL): maximum 400 characters long
    > * domain (non-NULL): maximum 100 characters long
    > * sponsored_appearances (non-NULL): Minimum value: 0. Maximum value: the scrape_count value from scrape appearances for that search term, device and date
    > * natural_appearances (non-NULL): Minimum value: 0. Maximum value: unlimited
    > * pla_appearances (non-NULL): Minimum value: 0. Maximum value: unlimited
    > * ctr (optional - NULLable): Minimum value: 0. Maximum value: 1.0

<br>

### The dataset and it's corresponding parquet files are accessed via the AWS API Credentials.
### <b>NOTE: </b>AWS API Credentials are not provided in this README.md file for the data protection and security reasons.

<br>

### **Below are the domain related information of the data attributes in the two datasets.**
> * search_term is a search that has been performed on Google search. For example: “car insurance”
> * device is the device used to perform the search. For example “desktop” or “mobile”
> * scrape_count is the number of times that search was performed on a specific date and device
> * domain is an advertiser domain. For example “asos.com”
> * ctr: the probability that someone will click an advert
> * sponsored, natural, and pla appearances are the number of times a type of advert has appeared for a given search term / device / domain on a date

<br>

## <u>**PROJECT TASK OBJECTIVE**</u>

### In the provided datasets, there are some issues introduced that break the described constraints. The key objective of this project task is to identify the relevant tests that are able to find and uncover the issues introduced. The tests should also detect any other common issues that might be present in the datasets.

<br>

## <u>**ENVIRONMENT SET-UP AND INSTALL INSTRUCTIONS**</u>

### Below are the steps that must be completed to enable the environment set-up for the execution of the project's source code in the local machine environment.

#### 1. Python Installation
> #### **Python 3.8 Version** is used throughout the project execution. Please ensure that Python version 3 is installed in the local machine by executing the command "**pip3 install python==3.8**" in the terminal window.
> #### [Python Installation Official Documentation]('https://www.python.org/')

#### 2. AWS Command Line Interface (CLI) Version 2 Installation
> #### Please follow the instructions as per AWS Official Documentation to install CLI version 2 in the local machine: [AWS CLI Version 2 Installation Instructions]('https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html')

#### 3. Verify the Successful installation of the AWS CLI in the local machine by executing the command "**aws --version**" in the terminal.

#### 4. AWS API Credentials Set-up in the Local Machine to Access the S3 Buckets
> #### Execute the below 2 commands in the terminal window to set-up the "AWS_ACCESS_KEY_ID" and the "AWS_SECRET_ACCESS_KEY" (details provided in the assignment pdf file) in the local machine.
> #### "**aws configure set AWS_ACCESS_KEY_ID *GivenAccessKey***"
> #### "**aws configure set AWS_SECRET_ACCESS_KEY *GivenSecretKey***"
> #### This will set-up and configure the AWS "Access_Key" and the "Secret_Key" details, that will enable to further access the AWS resources via API.

#### 5. Verification of the AWS API Credentials Set-up in the Local Machine to Access the S3 Buckets
> #### Execute the below 2 commands in the terminal window to verify the "AWS_ACCESS_KEY_ID" and the "AWS_SECRET_ACCESS_KEY" set-up in the local machine
> #### "**aws configure get AWS_ACCESS_KEY_ID**"
> #### "**aws configure get AWS_SECRET_ACCESS_KEY**"
> #### This will return the "Access_Key" and the "Secret_Key" details set-up (as provided in the assignment pdf file).

#### 6. Python Packages Installation
> #### Install the mentioned python packages in the local machine by executing the "**pip3 install *PackageName==VersionNumber***" command (version numbers as applicable) in the terminal window.
    > #### "os"
    > #### "math"
    > #### "time"
    > #### "datetime"
    > #### "boto3" (Version = 1.22.9)
    > #### "pandas" (Version = 1.2.0)
    > #### "pyarrow" (Version = 8.0.0)
    
### Post successful completion of the above steps, we will have the environment ready for the project execution.
    
<br>

## <u>**PROJECT FOLDER STRUCTURE**</u>

### Below is the folder structure followed as part of this project's execution.

> #### Project Base Directory "**Technical_Assignment_VidhyalakshmiParthasarathy**"
    > * #### "**README.md**" File - This includes all the steps and instructions to execute the project in the local machine
    > * #### "**modular_source_code**" Sub-Directory - This includes the parameters congiguration file and all the modular source code python files
    > * #### "**output**" Sub-Directory - This is the sub-directory where the output test summary reports for all the tests executed for each parquet input data file will be saved as individual "**.csv**" Data Quality Report files

<br>

## <u>**PROJECT IMPLEMENTATION APPROACH OVERVIEW**</u>

### This project's implementation follows a "**Modular Programming Apprach in Python**" achieving the below key points:

> * #### Each Modular Source Code written in Python represents a data quality test scenario to be executed, to uncover and spot the quality issues introducted in the individual parquet input data files of the "scrape_appearances" and the "competitor_appearances" datasets.
> * #### There is a re-usability capability of the modular source codes between "scrape_appearances" and the "competitor_appearances" datasets as applicable, as coding best practices.

<br>

## <u>**PROJECT EXECUTION INSTRUCTIONS**</u>

### Please follow the below steps to execute the project's modular source codes in the local machine.

> #### 1. Copy the project's base directory and its sub-contents into the directory of the local machine.
> #### 2. Please ensure that the Python software and the other Python packages set-up and installations as mentioned in the above "**ENVIRONMENT SET-UP AND INSTALL INSTRUCTIONS**" section are successfully installed and completed.
> #### 3. Update the "**output_directory**" parameter in the "**config.py**" file within the project's "**modular_source_code**" sub-directory "**Technical_Assignment_VidhyalakshmiParthasarathy/modular_source_code/**", to reflect the local machine's full-qualified directory path where the output "**.csv**" summary report files must be saved.
> #### 4. Open a new terminal window at the project's "**modular_source_code**" sub-directory "**Technical_Assignment_VidhyalakshmiParthasarathy/modular_source_code/**" and execute the "**main.py**" modular source code file using the command "**python3 main.py**".
> #### 5. By executing the above Step-4, will start the project's execution and will write the output test summary reports as "**.csv**" files into the "**output_directory**" path as mentioned in the "**config.py**" file.
> #### 6. Upon successful completion of the main program, the overall execution time in seconds will be displayed in the terminal window.
> #### 7. We can proceed verifying the individual "**.csv**" Data Quality Test Summary Report files corresponding to each of the parquet input data file stored in the "**output**" sub-directory "**Technical_Assignment_VidhyalakshmiParthasarathy/output/**".
