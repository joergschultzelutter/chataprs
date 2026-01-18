#
# ChatAPRS
# APRS input parser
# Author: Joerg Schultze-Lutter, 20256
#
# This input parser literally does nothing and just forwards the
# LLM query to the output generator
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

from CoreAprsClient import CoreAprsClient, CoreAprsClientInputParserStatus

import chap_ai_processor_main
from chap_ai_processor_main import ai_processors_qualifiers
import re


def parse_input_message(
    instance: CoreAprsClient, aprs_message: str, from_callsign: str, **kwargs
):
    """
    This is a stub for your custom APRS input parser.

    Parameters
    ==========
    instance: CoreAprsClient
        Instance of the core-aprs-client object.
    aprs_message: str
        The APRS message that the user has provided us with (1..67
        bytes in length). Parse the content and figure out what
        the user wants you to do.
    from_callsign: str
        Ham radio callsign that sent the message to us.
        Might be required by the input processor e.g. in case you
        have to determine the from_callsign's latitude/longitude.
    **kwargs: dict
        Optional keyword arguments

    Returns
    =======
    return_code: enum
        Appropriate return code value, originating from the
        CoreAprsClientInputParserStatus class
    input_parser_error_message: str
        if return_code is not PARSE_OK, this field can contain an optional
        error message (e.g. context-specific errors related to the
        keyword that was sent to the bot). If this field is empty AND
        return_code is NOT PARSE_OK, then the default error message will be returned.
    input_parser_response_object: dict | object
        Dictionary object where we store the data that is required
        by the 'output_generator' module for generating the APRS message.
        Note that you can also return other objects such as classes. Just ensure that
        both input_parser and output_generator share the very same
        structure for this variable.
    """

    success = True

    # try to determine if we are supposed to switch
    pattern = rf"^\s*llm\s+(?P<proc>{'|'.join(map(re.escape, chap_ai_processor_main.ai_processors_qualifiers))})\s*(?P<msg>.*)$"
    regex = re.compile(pattern, re.IGNORECASE)

    matches = regex.match(aprs_message)
    if matches:
        new_ai_processor = matches.group("proc")
        command_code = "llm_change"

    command_code = "llm_process"
    input_parser_error_message = ""
    return_code = CoreAprsClientInputParserStatus.PARSE_OK

    # our target dictionary that is going to be used by the output processor
    # for further processing.
    # You can (and have to) amend this dict object so that it contains all fields
    # relevant for output processing. Ensure that both input parser and output processor
    # use the same dictionary structure.
    input_parser_response_object = {
        "from_callsign": from_callsign,
        "command_code": command_code,
        "aprs_message": aprs_message,
    }

    return return_code, input_parser_error_message, input_parser_response_object


if __name__ == "__main__":
    pass
