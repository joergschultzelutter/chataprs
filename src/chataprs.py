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
from chap_ai_processor_main import ai_processors_qualifiers


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

    parser.add_argument(
        "--ai",
        default=ai_processors_qualifiers[0],
        choices=ai_processors_qualifiers,
        help="Valid AI processors",
    )

    args = parser.parse_args()
    cfg = args.configfile.name
    ai = args.ai

    if not os.path.isfile(cfg):
        print("Config file does not exist; exiting")
        sys.exit(0)

    return cfg, ai


if __name__ == "__main__":

    logger.debug(msg="Starting ChatAPRS")

    # Get the configuration file name
    configfile, my_ai = get_command_line_params()

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

    # Get the default AI name from our config data
    chap_shared.ai_processor = client.config_data["chataprs"]["chap_default_ai"]

    # check if the user has specified a valid AI qualifier
    if _default_ai_processor not in chap_ai_processor_main.ai_processors_qualifiers:
        logger.error(f"The default AI processor '{chap_shared.ai_processor}' in your config file is unknown to me")
        sys.exit(0)

    # Check if the AI qualifier has an active API key
    if _default_ai_processor not in client.config_data["chataprs_api_keys"]:
        logger.error(f"The default AI processor '{chap_shared.ai_processor}' in your config file has no API key entry")
        sys.exit(0)
    else:
        if client.config_data["chataprs_api_keys"][chap_shared.ai_processor] is "NOT_CONFIGURED":
            logger.error(f"The default AI processor '{chap_shared.ai_processor}' in your config file is not configured")
            sys.exit(0)

    # Set our shared variables
    chap_shared.ai_api_key = client.config_data["chataprs_api_keys"][chap_shared.ai_processor]
    chap_shared.persona_filename = client.config_data["chataprs"][
        "chap_persona_filename"
    ].format(ai_processor=chap_shared.ai_processor)

    # Verify if the Command Config file exists
    if not os.path.isfile(chap_shared.persona_filename):
        logger.error(
            msg=f"User prompt file '{chap_shared.persona_filename}' does not exist; exiting"
        )
        sys.exit(0)

    # Read the config file from disk
    success, chap_shared.persona_data = read_prompt_file_from_disk(
        filename=chap_shared.persona_filename
    )
    if not success:
        logger.error(
            msg=f"Unable to read user prompt file '{chap_shared.persona_filename}'; exiting"
        )
        sys.exit(0)

    # remember the prompt file's initial timestamp, thus allowing us to
    # detect any changes to the file during runtime (and re-read the file
    # into memory, if necessary)
    chap_shared.persona_initial_timestamp = get_modification_time(
        filename=chap_shared.persona_filename
    )

    # Finally, activate the APRS client and connect to APRS-IS
    client.activate_client()
