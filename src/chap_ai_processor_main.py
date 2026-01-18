#
# ChatAPRS
# AI processor selector module
# Author: Joerg Schultze-Lutter, 2025
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
# This module tries to shorten the given input text whereas possible. It
# acts as a decision tree on which post processor is about to get called.
# The actual post-processing is done in the various subsections

from chap_ai_processor_openai import ai_prompt_openai
from chap_ai_processor_palm import ai_prompt_palm

ai_processors = {
    "openai": ai_prompt_openai,
    "googlepalm": ai_prompt_palm,
}

ai_processors_qualifiers = list(ai_processors.keys())


def process_ai_content(
    user_prompt: str, input_text: str, ai_processor: str, api_key: str
):
    assert ai_processor in ai_processors
    return ai_processors[ai_processor](
        user_prompt=user_prompt, input_text=input_text, api_key=api_key
    )


if __name__ == "__main__":
    pass
