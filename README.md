# Jaxl IVR Simulator

Welcome to Jaxl IVR Simulator.

# Table of Contents

- [What is an IVR?](#what-is-an-ivr)
- [Prompt](#prompts)
  - [Prompt Strings](#prompt-strings)
  - [Prompt Audio](#prompt-audios)
- [About Jaxl IVR Simulator](#about-jaxl-ivr-simulator)
- [Try Jaxl IVR Simulator](#try-jaxl-ivr-simulator)
- [Initialize your IVR Project Directory](#initialize-your-ivr-project-directory)
- [Create your First IVR](#create-your-first-ivr)

## What is an IVR?

```
Press 1 to confirm the transaction,
Press 2 to block the card and talk to our customer representation,
Press 3 to repeat the options
```

If you have ever experienced a call where the system is asking for your inputs like above, you already understand how an [IVR](https://en.wikipedia.org/wiki/Interactive_voice_response) works.

## Prompts

### Prompt Strings

Sentences spoken out by the system are referred to as **"Prompt Strings"**.

During a call, Jaxl IVR Infrastructure convert prompt strings into audio files and playback to the user over the call.

Some examples of prompt string includes:

1. Welcome to My Company.
2. Welcome to Jaxl. Press 1 for customer care. Press 2 for HR department.
3. Thank you for calling us. One of our customer representative will call you back soon. Bye
4. Welcome to Jaxl Payments. Your total amount due is 51 rupee. To make a payment please enter your credit card number followed by star.

### Prompt Audios

Your IVR can also playback custom audio files. Example, playing out a music while the user waits. Such custom audio files are referred to as **"Prompt Audios"**.

A prompt string can also be followed by a prompt audio. Example:

1. Hello. You have reached Jaxl customer support. Please wait while we connect your call. "Prompt Audio playing music".

A prompt audio alone works too. Example:

1. "Prompt audio playing music"

## About Jaxl IVR Simulator

Jaxl IVR Simulator is available as a Docker container. It allows you to quickly build and test your custom IVRs.

In a nutshell, your IVR will be responsible for:

1. Returning [**"prompt strings"**](#prompt-strings) and/or [**"prompt audios"**](#prompt-audios) that will be spoken out to the user
2. Handle user inputs and return [**prompts**](#prompts) in reply to the user

At any point, IVRs can also return prompts followed by hangup to terminate the call.

## Try Jaxl IVR Simulator

Lets give it a try by passing `-h` flag to it:

On Mac & Linux:

```bash
docker run \
  -it --rm \
  jaxlinnovationsprivatelimited/jaxl-ivr-simulator -h
```

On Windows using cmd.exe

```bash
docker run ^
  -it --rm ^
  jaxlinnovationsprivatelimited/jaxl-ivr-simulator -h
```

On Windows using PowerShell

```bash
docker run `
  -it --rm `
  jaxlinnovationsprivatelimited/jaxl-ivr-simulator -h
```

You should see following usage information:

```console
Jaxl IVR Simulator Command Line Interface

positional arguments:
  {login,init,create,check,run,call,logout}
    login               Login
    init                Initialize the IVR project directory
    create              Create a new IVR with the given name
    check               Perform code level checks before submission
    run                 Run an IVR with the given name
    call                Make an outgoing call and control it through your Jaxl IVR application
    logout              Logout

options:
  -h, --help            show this help message and exit
```

## Initialize your IVR Project Directory

1. Create a new directory that will contain your IVR code. For documentation purposes, let's imagine have created a new directory at following path on your system `/path/to/ivr/playground/directory`

   > NOTE: Use a path appropriate for your system.

2. Within your IVR project directory, run the following command:

   On Mac & Linux:

   ```bash
   docker run \
       -it --rm \
       -v ${PWD}:/jaxl/ivr \
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator init
   ```

   On Windows using cmd.exe

   ```bash
   docker run ^
       -it --rm ^
       -v %cd%:/jaxl/ivr ^
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator init
   ```

   On Windows using PowerShell

   ```bash
   docker run `
       -it --rm `
       -v ${PWD}:/jaxl/ivr `
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator init
   ```

`init` command will guide you through the steps.  You can run `init` command multiple times in the same directory.  If any necessary files are missing, `init` will recreate them in your project directory.

You will see something like this:

```bash
[🗂️][❌] .vscode does not exist
[🗂️][❌] jaxl/ivr/frontend does not exist
[🗂️][❌] schemas does not exist
[🗂️][❌] tests does not exist
[🗂️][❌] webhooks does not exist
[📇][❌] .vscode/settings.json does not exist
[📇][❌] .gitignore does not exist
[📇][❌] .isort.cfg does not exist
[📇][❌] requirements.txt does not exist
[📇][❌] PROJECT.md does not exist
[📇][❌] IVR.md does not exist
[📇][❌] tests/__init__.py does not exist
[📇][❌] webhooks/__init__.py does not exist
[📇][❌] jaxl/ivr/frontend/__init__.py does not exist
[📇][❌] jaxl/ivr/frontend/base.py does not exist
[📇][❌] jaxl/ivr/frontend/ivr.json does not exist
Do you want to create missing files (11), update files (0) and folders (5)? [y/N]: y
Created 5 directories
Created 11 files
```

## Create your First IVR

`init` command has initialized your IVR project directory structure as expected by Jaxl IVR Simulator.

To create your first IVR:

1. Open your project directory in `VSCode`
2. Follow [`PROJECT.md`](./PROJECT.md) placed in your project directory for further instructions.
