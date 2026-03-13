#
# AI module (OpenAI / ChatGPT module)
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
import openai
from openai import OpenAI
import json
from chap_logger import logger


def ai_prompt_openai(persona: str, user_prompt: str, api_key: str, model: str, **kwargs):
    """
    Summarize and abbreviate text via OpenAI
    ==========
    persona: 'str'
        Persona for inquiry
    user_prompt: 'str'
        The input text from the user that we want to process
    api_key: 'str'
        OpenAI API Key

    Returns
    =======
    response: 'str'
        Our processed text
    """

    client = OpenAI(api_key=api_key)
    result = None

    try:
        summary = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": persona,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model=model,
            temperature=0.7,
            max_tokens=1000,
        )
        result = summary.choices[0].message.content
    except openai.APIConnectionError as e:
        logger.error(msg="Unable to connect to OpenAI server")
        logger.error(e.__cause__)
        result = None
    except openai.RateLimitError as e:
        logger.error(msg="We have hit the API rate limit")
        result = None
    except openai.APIStatusError as e:
        logger.error(msg=f"HTTP{e.status_code}: {e.response}")
        result = None
    except Exception as e:
        logger.error(msg="Other exception occurred")
        logger.error(e.__cause__)
        result = None

    return result


if __name__ == "__main__":
    pass
