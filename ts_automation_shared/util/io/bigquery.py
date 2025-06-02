from typing import Dict
from google.cloud import bigquery
from google.oauth2 import service_account


class BigQueryClient:
    def __init__(self, credentials_info: Dict[str, str], project_id: str):
        """
        Initialize the BigQuery client using service account credentials.

        :param credentials_info: Dictionary containing service account keys.
        :param project_id: GCP project ID.
        """
        self.credentials = service_account.Credentials.from_service_account_info(credentials_info)
        self.project_id = project_id
        self.client = bigquery.Client(credentials=self.credentials, project=project_id)

    def get_data_from_bq(self, query: str):
        """
        Run a SQL query and return the result as a DataFrame.

        :param query: SQL query string.
        :return: pandas.DataFrame with query results.
        """
        job = self.client.query(query)
        return job.to_dataframe()
