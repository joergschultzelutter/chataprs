# Usage

The bot knows only one command (`switchai`), followed by one of the valid AI processor qualifiers (see list below). Any messages with different content are interpreted as a query to the AI.

## Changing the AI provider
Using the command `switchai`, a switch from, for example, the OpenAI API to Google can be forced during runtime. A successful switch requires two things:
- The corresponding API key exists in the configuration file.
- An external file with the content of the AI-specific user prompt exists.

All supported AI providers are declared in the [`chap_ai_processor_main.py`](https://github.com/joergschultzelutter/chataprs/blob/master/src/chap_ai_processor_main.py) file:

```python
ai_processors = {
    "ollama_local": ai_prompt_ollama_local,
    "openai": ai_prompt_openai,
    "googlepalm": ai_prompt_palm,
}
```
Switching to a different AI processor can be done by sending the `awitchai` command plus AI processor name to the bot, e.g. `switchai openai`. If the switch was successful (*), you will receive an `AI processor change successful` message. 

(*) The AI's API key is _not_ checked at this point in time, meaning that accessing the AI at a later stage still might fail.