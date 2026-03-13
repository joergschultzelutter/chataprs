# Usage

## Table of Contents
<!--ts-->
* [Changing the AI provider](#changing-the-ai-provider)
* [Examples](#examples)
<!--te-->

The bot knows only one command (`switchai`), followed by one of the valid AI processor qualifiers (see list below). Any messages with different content are interpreted as a query to the AI.

## Changing the AI provider
Using the command `switchai`, a switch from, for example, the `ollama` API to `openai` can be forced during runtime. A successful switch requires two things:
- The corresponding API key exists in the configuration file (assuming that your AI needs one).
- An external file with the content of the AI-specific persona exists.

All currently supported AI providers are declared in the [`chap_ai_processor_main.py`](https://github.com/joergschultzelutter/chataprs/blob/master/src/chap_ai_processor_main.py) file:

```python
ai_processors = {
    "ollama": ai_prompt_ollama,
    "openai": ai_prompt_openai,
}
```
Switching to a different AI processor can be done by sending the `awitchai` command plus AI processor name to the bot, e.g. `switchai openai`. If the switch was successful (*), you will receive an `AI processor change successful` message.

(*) The AI's API key is _not_ checked at this point in time, meaning that accessing the AI at a later stage still might fail.

## Examples

- `switchai ollama` --> switches to the `ollama` AI and uses the `chataprs_ai_persona_ollama.txt` persona input
- `switchai openai` --> switches to the `openai` AI and uses the `chataprs_ai_persona_openai.txt` persona input
- `switchai myveryspecialai` will be treated as regular request and is forwarded to the AI for processing. Reason: `myveryspecialai` is not part of the known AI processors. You can extend the list of known processors by enhancing the [`chap_ai_processor_main.py`](/src/chap_ai_processor_main.py) file.

