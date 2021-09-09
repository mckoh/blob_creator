"""
Uploader Module for Blob Creator

Author: Mike Kohlegger
Date: 2021/09
"""

from owncloud import Client

import requests
import urllib

from .const import DROP_LINK


def shorten_url(url_long) -> str:
    """Can be used to shorten a long url with tiny-url

    :param url_long: The URL that shoul be shortened
    :return: Shortened URL as string
    """
    url = "http://tinyurl.com/api-create.php" + "?" \
        + urllib.parse.urlencode({"url": url_long})
    res = requests.get(url)
    return res.text


def upload_file(file) -> str:
    """Can be used to upload a file to our open repository

    :param file: The file name of the file to upload
    :return: The files final URL after upload
    """
    oc = Client.from_public_link(DROP_LINK)
    oc.drop_file(file)
    base_url = "https://owncloud.fh-kufstein.ac.at/index.php/s/Y45bGDArPzFO3Lg/"
    file_url = f"download?path=%2F&files={file}"
    return base_url + file_url


def create_guid_named_file(file) -> str:
    """Can be used to create a copy of a file with a unique name

    :param file: The file that should be copied
    :return: The name of the unique-named copy
    """
    #TODO
    pass