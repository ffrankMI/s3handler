import boto3
import pandas 

"""
Class that interacts with an s3 bucket

Attributes:
    bucket (str): The bucket to interact with
    s3 (boto3.client): The boto3 client to interact with s3

Methods:
    get_string_from_s3(subfolder): Get an object from an s3 folder
    push_df_to_s3_csv(subfolder,df): Upload a dataframe to s3 as csv
    object_exists_s3(subfolder): Check if a subfolder exists in s3
    delete_from_s3(subfolder): Delete a subfolder from s3
"""

class S3Handler:
    def __init__(self,bucket):
        self.bucket = bucket
        self.s3 = boto3.client('s3')

    """
    Get an object from an s3 folder

    Args:
        subfolder (str): The subfolder to get the report from

    Returns:
        str: The report as a string
    """
    def get_string_from_s3(self,subfolder) -> str:
        s3 = boto3.resource('s3')
        obj = s3.Object(self.bucket, subfolder)
        return obj.get()['Body'].read().decode('utf-8')

    """
    Upload a dataframe to S3 as csv

    Args:
        df (pandas.DataFrame): The dataframe to upload
        subfolder (str): The subfolder to upload to

    Returns:
        bool: True if the dataframe was uploaded, False otherwise
    """
    def push_df_to_s3_csv(self,subfolder,df) -> bool:
        s3 = boto3.resource('s3')
        response = s3.Object(self.bucket, subfolder).put(Body=df.to_csv(index=False))
        return response['ResponseMetadata']['HTTPStatusCode'] == 200

    """
    Check if a subfolder exists in S3

    Args:
        subfolder (str): The subfolder to check

    Returns:
        bool: True if the subfolder exists, False otherwise
    """
    def object_exists_s3(self,subfolder) -> bool:
        response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=subfolder)
        return response['KeyCount'] > 0

    """
    Delete a subfolder from S3

    Args:
        subfolder (str): The subfolder to delete

    Returns:
        bool: True if the subfolder was deleted, False otherwise
    """
    def delete_from_s3(self,subfolder) -> bool:
        response = self.s3.delete_object(Bucket=self.bucket, Key=(subfolder + '/'))
        return response['ResponseMetadata']['HTTPStatusCode'] == 200