# chataprs

`chataprs` is an APRS-based AI bot that supports a variety of AI platforms (provided you have API keys for each AI provider). It delivers the AI's response in a multi-message format, allowing the user to receive even long AI messages via APRS.

## Table of Contents
<!--ts-->
* [Introduction](#introduction)
* [Installation instructions](#installation-instructions)
* [Usage](#usage)
* [FAQ](#faq)
* [The fine print](#the-fine-print)
<!--te-->

## Introduction
APRS users can use `chataprs` to query shorter requests to AIs such as OpenAI, Google, etc. The length of the query from the APRS user to the AI is determined by the maximum length of an APRS message (67 characters). Responses from the AI to the APRS user are transmitted as short as possible in terms of content, but due to their transmission as numbered messages, they can contain up to 5,800 bytes in extreme cases.

## Installation instructions

- clone repository
- `pip install -r requirements.txt`
- ...

## Usage

The bot only knows one command. Any messages with different content are interpreted as a query to the AI.

Using the command `llm`, a switch from, for example, the OpenAI API to Google can be forced during runtime. A successful switch requires two things:
- The corresponding API key exists in the configuration file.
- An external file with the content of the AI-specific user prompt exists.

## Technical details

`secure-aprs-bastion-bot` relies on my [`core-aprs-client`](https://www.github.com/joergschultzelutter/core-aprs-client) APRS messaging framework. 

## The fine print

- If you intend to host an instance of this program, you must be a licensed radio amateur. BYOP: Bring your own (APRS-IS) passcode. If you don't know what this is, then this program is not for you.
- APRS is a registered trademark of APRS Software and Bob Bruninga, WB4APR.
