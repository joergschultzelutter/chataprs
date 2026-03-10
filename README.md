# chataprs

`chataprs` is an APRS-based AI bot that supports a variety of AI platforms (provided you have API keys for each AI provider). It delivers the AI's response in a multi-message format, allowing the user to receive even long AI messages via APRS. The AI provider can be switched during runtime via special APRS command sequence.

## Table of Contents
<!--ts-->
* [Introduction](#introduction)
* [Installation instructions](#installation-instructions)
* [Usage](#usage)
* [FAQ](#faq)
* [The fine print](#the-fine-print)
<!--te-->

## Introduction
APRS users can use `chataprs` to query shorter requests to AIs such as OpenAI, Google, etc. The length of the query from the APRS user to the AI is determined by the maximum length of an APRS message (67 characters). Responses from the AI to the APRS user are transmitted as short as possible in terms of content, but due to their transmission as numbered messages, they can contain up to 5.7kb (aka 99 separate APRS messages, each containing up to 59 characters) in case a longer answer is deemed necessary. You can limit a maximum message length in each AI's individual user prompt file.

## Installation instructions
The installation and configuration instructions can be found [here](/docs/installation-instructions.md).

## Usage

The bot only knows only one command (`switchai`). Any messages with different content are interpreted as a query to the AI. Information on the `switchai` keyword can be found [here](/docs/usage.md).

## Technical details

`chataprs` acts as a showcase application for my [`core-aprs-client`](https://www.github.com/joergschultzelutter/core-aprs-client) APRS bot framework. 

## The fine print

- If you intend to host an instance of this program, you must be a licensed radio amateur. BYOP: Bring your own (APRS-IS) passcode. If you don't know what this is, then this program is not for you.
- APRS is a registered trademark of APRS Software and Bob Bruninga, WB4APR.
