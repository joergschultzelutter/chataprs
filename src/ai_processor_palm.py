#
# AI module (Google PaLM)
# Author: Joerg Schultze-Lutter, 2023
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
#
import google.generativeai as palm
from client_logger import logger


def _process_ai_request(
    model: str, content: str, temp: float, max_output_tokens: int, api_key: str
):
    palm.configure(api_key=api_key)

    response = palm.generate_text(
        model=model,
        prompt=content,
        temperature=temp,
        max_output_tokens=max_output_tokens,
    )
    return response.result


def ai_prompt_palm(user_prompt: str, input_text: str, api_key: str, **kwargs):
    """
    Summarize and abbreviate text via Google PaLM
    ==========
    user_prompt: 'str'
        User prompt used for processing the input text
    input_text: 'str'
        The text that we want to process
    api_key: 'str'
        Google PaLM API Key

    Returns
    =======
    response: 'str'
        Our abbreviated text
    """

    temp = 0.7
    max_output_tokens = 1000
    model = "models/text-bison-001"

    objective = user_prompt

    user_content = f"{input_text}"

    response = _process_ai_request(
        model=model,
        content=f"{objective} {user_content}",
        temp=temp,
        max_output_tokens=max_output_tokens,
        api_key=api_key,
    )
    return response


if __name__ == "__main__":
    pass
