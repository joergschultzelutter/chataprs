#
# ChatAPRS
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
from CoreAprsClient import CoreAprsClient

# Your custom input parser and output generator code
from chap_input_parser import parse_input_message
from chap_output_generator import generate_output_message

import argparse
import os
import sys
import logging
import chap_shared

from chap_logger import logger
from chap_utils import get_modification_time, read_prompt_file_from_disk


def get_command_line_params():
    """
    Gets and returns the command line arguments

    Parameters
    ==========

    Returns
    =======
    cfg: str
        name of the configuration file
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--configfile",
        default="chataprs.cfg",
        type=argparse.FileType("r"),
        help="APRS framework config file name (default is 'chataprs.cfg')",
    )

    args = parser.parse_args()
    cfg = args.configfile.name

    if not os.path.isfile(cfg):
        print("Config file does not exist; exiting")
        sys.exit(0)

    return cfg


if __name__ == "__main__":

    logger.debug(msg="Starting ChatAPRS")

    # Get the configuration file name
    configfile = get_command_line_params()

    # Create the CoreAprsClient object. Supply the
    # following parameters:
    #
    # - configuration file name
    # - log level (from Python's 'logging' package)
    # - function names for both input processor and output generator
    #
    client = CoreAprsClient(
        config_file=configfile,
        log_level=logging.DEBUG,
        input_parser=parse_input_message,
        output_generator=generate_output_message,
    )

    # Save the command config filename - we may need to re-read the file
    # in case its content has changed during runtime
    chap_shared.user_prompt_filename = client.config_data["chataprs"][
        "chap_user_prompt_filename"
    ]

    # Verify if the Command Config file exists
    if not os.path.isfile(chap_shared.user_prompt_filename):
        logger.error(
            msg=f"User prompt file '{chap_shared.user_prompt_filename}' does not exist; exiting"
        )
        sys.exit(0)

    # Read the config file from disk
    success, chap_shared.user_prompt = read_prompt_file_from_disk(
        filename=chap_shared.user_prompt_filename
    )
    if not success:
        logger.error(
            msg=f"Unable to read user prompt file '{chap_shared.user_prompt_filename}'; exiting"
        )
        sys.exit(0)

    # remember the prompt file's initial timestamp, thus allowing us to
    # detect any changes to the file during runtime (and re-read the file
    # into memory, if necessary)
    chap_shared.user_prompt_initial_timestamp = get_modification_time(
        filename=chap_shared.user_prompt_filename
    )

    # Finally, activate the APRS client and connect to APRS-IS
    client.activate_client()
