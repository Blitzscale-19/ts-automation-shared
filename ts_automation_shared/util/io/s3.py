# Modules
import io
import boto3
import pandas as pd

# Exceptions
from exceptions.exceptions import InternalError


class S3:
    def __init__(self, s3_client):
        s3_config = s3_client

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=s3_config["accessKeyId"],
            aws_secret_access_key=s3_config["secretAccessKey"],
            region_name=s3_config["region"],
        )

        self.region = s3_config["region"]
        self.bucket = s3_config["nushop_ops_assets"]

    def get_file_url_path(self, bucket: str = None) -> str:
        """
        Returns the file URL path for an S3 bucket.

        :param bucket: Bucket name
        :type bucket: str, optional
        """

        if not bucket:
            bucket = self.bucket

        return f"https://s3.{self.region}.amazonaws.com/{bucket}"

    def upload_df_to_s3(self, data_frame: pd.DataFrame, file_name: str, bucket: str = None):
        """
        Converts a data frame to CSV and uploads to an S3 bucket.

        :param file_name: File name
        :type file_name: str

        :param bucket: Bucket name
        :type bucket: str, optional

        :return: S3 link to the CSV file.
        """

        if not bucket:
            bucket = self.bucket

        buffer = io.StringIO()  # text buffer for CSV
        data_frame.to_csv(buffer, index=False)
        buffer.seek(0)

        file_url = self.upload_file_to_s3_by_buffer(
            io.BytesIO(buffer.getvalue().encode()),
            file_name,
            bucket,  # convert to byte stream
        )

        return file_url

    def upload_file_to_s3_by_buffer(self, buffer, file_name, bucket=None):
        """
        Takes a buffer and uploads to S3 bucket under given file name.

        :param buffer: File buffer

        :param bucket: Bucket name
        :type bucket: str, optional
        """

        if not bucket:
            bucket = self.bucket

        # Get the file URL path
        file_url = self.get_file_url_path(bucket) + "/" + file_name

        # Upload file to S3 using 'upload_fileobj'
        try:
            self.s3.upload_fileobj(buffer, bucket, file_name, ExtraArgs={"ACL": "public-read"})

        except Exception as exc:
            # Catch any other exception and log it
            raise InternalError(f"An unexpected error occurred while uploading the file: {exc}") from exc

        return file_url
