"""
Uploader Module for Blob Creator

Author: Mike Kohlegger
Date: 2021/09
"""

from shutil import copyfile
from os import remove
from os.path import join
from uuid import uuid4
from urllib import parse
from urllib.error import HTTPError
from re import findall
from requests import get
from owncloud import Client

from .const import DROP_LINK


def shorten_url(url_long) -> str:
    """Can be used to shorten a long url with tiny-url

    :param url_long: The URL that shoul be shortened
    :return: Shortened URL as string
    """
    url = "http://tinyurl.com/api-create.php" + "?" \
        + parse.urlencode({"url": url_long})
    res = get(url)
    return res.text


def upload_file(file) -> str:
    """Can be used to upload a file to our open repository

    :param file: The file name of the file to upload
    :return: The files final URL after upload
    """

    unique_file = create_guid_named_file(file)

    try:
        cloud_end = Client.from_public_link(DROP_LINK)
        cloud_end.drop_file(unique_file)
    except HTTPError as exception:
        print(exception)

    base_url = "https://owncloud.fh-kufstein.ac.at/index.php/s/Y45bGDArPzFO3Lg/"
    file_url = f"download?path=%2F&files={unique_file}"

    remove(unique_file)

    long_url = base_url + file_url
    return shorten_url(long_url)


def create_guid_named_file(file, path=None) -> str:
    """Can be used to create a copy of a file with a unique name

    :param file: The file that should be copied
    :return: The name of the unique-named copy
    """

    assert len(findall("\\.", file)) == 1, "file must only contain one ."
    ending = file.split(".")[1]
    new_name = str(uuid4())
    destination_file = f"{new_name}.{ending}"
    copyfile(
        src=join(path, file),
        dst=join(path, destination_file)
    )
    return destination_file
