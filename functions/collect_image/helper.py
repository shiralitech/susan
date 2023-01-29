"""helper logic for collect image function"""

import os
import tempfile
from logging import Logger
from typing import Tuple

from iot.storage.client import CredentialType, LocationType, IoTStorageClient

STORAGE_ACCOUNT_NAME = os.getenv("STORAGE_ACCOUNT_NAME")
STORAGE_ACCOUNT_CNX_STR = os.getenv("STORAGE_ACCOUNT_CNX_STR")
STORAGE_ACCOUNT_INPUT_CONTAINER = os.getenv("STORAGE_ACCOUNT_INPUT_CONTAINER")
STORAGE_ACCOUNT_OUTPUT_CONTAINER = os.getenv("STORAGE_ACCOUNT_OUTPUT_CONTAINER")


def help(logger: Logger, blob_url: str) -> Tuple[int, str]:
    """collect image helper function"""
    status = 200
    message = "file copied successfully!"

    try:
        # get file name
        file_name = blob_url.split("/")[-1]
        logger.info(f"blob name: {file_name}")

        # instantiate client
        storage_client = IoTStorageClient(
            credential_type=CredentialType.CONNECTION_STRING,
            location_type=LocationType.CLOUD_BASED,
            account_name=STORAGE_ACCOUNT_NAME,
            credential=STORAGE_ACCOUNT_CNX_STR,
        )

        # print info w/ repr
        print(f"{storage_client.__repr__()}")

        # download blob to tempfile
        temp_file = tempfile.NamedTemporaryFile()
        download_result = storage_client.download_file(
            container_name=STORAGE_ACCOUNT_INPUT_CONTAINER,
            source=file_name,
            dest=temp_file.name,
        )
        if not download_result:
            print("unable to download file")
            temp_file.close()
            raise

        # upload tempfile to blob
        upload_result = storage_client.upload_file(
            container_name=STORAGE_ACCOUNT_OUTPUT_CONTAINER,
            source=temp_file.name,
            dest=file_name,
        )
        if not upload_result:
            print("unable to upload file")
            temp_file.close()
            raise

        # clean-up local memory
        temp_file.close()
    except Exception as ex:
        status = 500
        message = f"exception occurred during file copy: {ex}"
        logger.error(message)
        pass
    
    return status, message
