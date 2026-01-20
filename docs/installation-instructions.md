# Installation instructions

The following installation instructions assume that the user is using the default names for the configuration files. If you want to use your own configuration file names, the following assumptions apply:

- The file `chataprs.cfg` is the core configuration file for the actual APRS bot. Its name is also the only parameter that can be passed to the bot externally via a program argument if desired. All other bot-specific parameters are defined in this file.
- The name of the [Apprise](https://www.github.com/caronc/apprise) crash messaging handler file is also specified in the core configuration file of the actual bot. A valid Apprise configuration should be stored here in order to receive a notification in the event of a program crash. Alternatively, the crash handler can also be disabled - see instructions.

## Table of Contents
<!--ts-->
* [Initial steps](#initial-steps)
* [Create the callsign/command-code configuration file with `configure.py`](#create-the-callsigncommand-code-configuration-file-with-configurepy)
* [Create the `chataprs` configuration file](#create-the-chataprs-configuration-file)
* [Apprise config file](#apprise-config-file)
* [Start the bot](#start-the-bot)
<!--te-->


## Initial steps
- Clone this repository
- `pip install -r requirements.txt` (or use the `requirements.txt` file from the respective project's subdirectories in case you just want to install a single program)

## Create the `chataprs` configuration file

The following sections describe be bot's configuration. The first section focuses on the actual bot itself (e.g. callsign configuration) while the second section focuses on the configuration that is specific to `chataprs`.

### Basic bot configuration

- Configure the bot's core configuration file. This file contains configuration info on the bot's callsign and other config info such as beaconing and broadcasting.
  - Rename the preconfigured configuration file [chataprs.cfg.TEMPLATE](/src/chataprs.cfg.TEMPLATE) and remove the `.TEMPLATE` file extension. `chataprs.cfg` is the default configuration filename.
  - Amend the bot's [configuration file](/docs/chataprs.md#configuration-file). The bot is based on my `core-aprs-client` framework ([repository link](https://github.com/joergschultzelutter/core-aprs-client)) and comes preconfigured. The ABSOLUTE MINIMAL configuration changes require the following fields to get modified:
    - `aprsis_callsign` - your bot's future callsign, e.g. DF1JSL-13
    - `aprsis_passcode` - the APRS-IS passcode that matches your `aprsis_callsign`. If you don't know what this is, then this program is not for you.
    - `aprsis_server_filter` - the APRS-IS server filter. If e.g. your callsign is `DF1JSL-13`, you MUST go for the [group message filter](https://www.aprs-is.net/javAPRSFilter.aspx) that is specific to your callsign (`/g/DF1JSL-13`). Note that no additional callsign filtering is in place, meaning that `chataprs` relies on proper filter settings!
  - Set the [crash handler's config file name](https://github.com/joergschultzelutter/core-aprs-client/blob/master/docs/configuration_subsections/config_crash_handler.md) (field name in the config file is `apprise_config_file`) to `NOT_CONFIGURED` if you want to disable Apprise messaging. In any other case, configure the Apprise config file as shown in the next paragraph.

### `chataprs` specific configuration

The configuration that is specific to `chataprs` can be found at the end of the configuration file and consists of two sections:

```python
[chataprs]
#
# Configuration data that is specific to chataprs
#
# Filename for the llm prompt
chap_llm_prompt_filename = chataprs_ai_prompt_{llm}.txt

[ai_api_keys]
#
# API keys for each supported llm (see chap_ai_processor_main.py)
# Names MUST be identical to content from "chap_ai_qualifiers" list
# from the chap_ai_processor_main.py file
# Set value to NOT_CONFIGURED if you don't want to use the API key
#
openai = NOT_CONFIGURED
googlepalm = NOT_CONFIGURED
```

##### `chataprs` configuration section

- `chap_llm_prompt_filename` contains a template filename for the future AI-specific user prompt file.

##### `ai_api_keys` configuration section



## Apprise config file
- Configure the bot's Apprise messaging configuration file. If you want to disable the crash handler's Apprise messaging: see [basic bot configuration](/docs/installation-instructions.md#basic-bot-configuration). 
  - rename the provided [`apprise.yml.TEMPLATE`](/configuration_file_examples/apprise.yml.TEMPLATE) configuration file and remove the `.TEMPLATE` file extension. `apprise.yml` is the file's default filename.
  - Configure the file as illustrated in Apprise's [YAML Configuration Documentation](https://github.com/caronc/apprise/wiki/config_yaml)

## Start the bot

- Start the bot

```python
nohup python chataprs.py >nohup.out &
```
