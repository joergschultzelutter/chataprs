#
# AI module (locale ollama instance module)
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

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from urllib import response

from chap_logger import logger



def ollama_generate(
    base_url: str,
    model: str,
    persona_system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    stream: bool = False,
    timeout_s: int = 600,
) -> str:
    """
    Retrieve content from ollama

    Parameters
    ==========
    base_url: str
        ollama docker base url
    model: str
        ollama model name
    persona_system_prompt: str
        Persona system prompt
    user_prompt: str
        user query
    temperature: float
        inquiry temperature
    stream: bool
        false: return (finalized) JSON response
        true: stream response
    timeout_s: int
        timeout in seconds

    Returns
    =======
    output: str or None


    """
    endpoint = base_url.rstrip("/") + "/api/generate"

    payload = {
        "model": model,
        "prompt": user_prompt,
        "system": persona_system_prompt,
        "stream": stream,
        "options": {
            "temperature": temperature,
        },
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        raise RuntimeError(f"HTTPError {e.code}: {e.reason}\n{body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}") from e

    # stream=false => retrieve JSON object
    try:
        obj = json.loads(raw)
        return obj.get("response", "")
    except json.JSONDecodeError:
        # Exception handler for those cases where streaming is returned:
        out = []
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                j = json.loads(line)
                if "response" in j:
                    out.append(j["response"])
            except json.JSONDecodeError:
                continue
        return "".join(out)


def ai_processor_ollama_local(
    persona: str, user_prompt: str, **kwargs
):
    """
    Summarize and abbreviate text via ollama

    Parameters
    ==========
    persona: 'str'
        Persona for inquiry
    user_promcpt: 'str'
        The input text from the user that we want to process

    Returns
    =======
    response: 'str'
        Our processed text
    """

    try:
        output = ollama_generate(
            base_url="http://localhost:11434",
            model="llama3.1",
            persona_system_prompt=persona,
            user_prompt=user_prompt,
            temperature=0.2,
            stream=False,
        )
    except Exception as e:
        logger.debug(msg="Error during ollama call")
        output = None

    return output


if __name__ == "__main__":
    pass


