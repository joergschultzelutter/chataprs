#!/opt/local/bin/python
#
# ChatPARS: utility functions
# Author: Joerg Schultze-Lutter, 2026
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Shorten and abbreviate the original input text which - unfortunately - is
# usually provided by the BBK site in epic proportions. We try to shorten the
# text as much as possible, thus rendering the output text to a format that is
# more compatible with e.g. SMS devices.
#
from chap_logger import logger
import os

def get_modification_time(filename: str):
    timestamp = None
    if os.path.isfile(filename):
        timestamp = os.path.getmtime(filename)
    return timestamp


def does_file_exist(file_name: str):
    """
    Checks if the given file exists. Returns True/False.

    Parameters
    ==========
    file_name: str
                    our file name
    Returns
    =======
    status: bool
        True /False
    """
    return os.path.isfile(file_name)

def read_prompt_file_from_disk(filename: str):
    """
    Reads a prompt file and returns its contents.

    Parameters
    ==========
    filename: str
        Name of the external prompt file

    Returns
    =======
    success: bool
        True / False, depending on whether the file was read
    data: str
        User prompt
    """
    __success = False
    data = ""

    if not does_file_exist(file_name=filename):
        logger.error(f"Configuration file '{filename}' does not exist")
        # We simply return the pre-defined dictionary
        # so let's consider this a success
        __success = False
    else:
        try:
            with open(file=filename, mode="r") as prompt_file:
                data = prompt_file.read()
                logger.info(f"Configuration file '{filename}' was successfully read")

        except:
            logger.warning(f"Cannot read prompt file '{filename}'")
    return __success, data
