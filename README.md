# Jaxl IVR Simulator

Welcome to Jaxl IVR Simulator. Build

1) Custom IVR solutions
2) AI/ML driven conversational bots
3) Schedule LLM driven outgoing pre-sales and post-sales calls

and much more, sky is the limit with Jaxl.

👉 Jaxl Developer Platform (early access form):
[https://forms.gle/71tP4YvruF4Py43J9](https://forms.gle/71tP4YvruF4Py43J9)

# Table of Contents

- [📂 Examples](#-examples)
- [❓ What is an IVR?](#-what-is-an-ivr)
- [🎛️ Prompt](#️-prompts)
  - [📝 Prompt Strings](#-prompt-strings)
  - [🔊 Prompt Audio](#-prompt-audios)
- [ℹ️ About Jaxl IVR Simulator](#ℹ️-about-jaxl-ivr-simulator)
- [🚀 Try Jaxl IVR Simulator](#-try-jaxl-ivr-simulator)
- [🛠️ Initialize your IVR Project Directory](#️-initialize-your-ivr-project-directory)
- [🧪 Create your First IVR](#-create-your-first-ivr)
- [🐳 Docker Image Tags](#-docker-image-tags)
- [💬 Need Help?](#-need-help)

## 📂 Examples

Explore existing examples to help you get started:

- [Calculator](https://github.com/jaxl-innovations-private-limited/jaxl-ivr-simulator/pull/1/): Think of this as the "Hello World" of the Jaxl IVR Simulator. It demonstrates the basic structure and usage.
  - Checkout out [calculator.py](https://github.com/jaxl-innovations-private-limited/jaxl-ivr-simulator/pull/1/files#diff-2719bcdf39b3bcf0f6999edca55c1be6981159fbe9391984b29f9c105b9e053b) for a simple example.
  - Refer to [test_calculator.py](https://github.com/jaxl-innovations-private-limited/jaxl-ivr-simulator/pull/1/files#diff-ea6153b9035bb3f8a3625f020cfce0853c589310ecb3ef30d7162a13ba776a26) to see how to apply Test-Driven Development (TDD) to IVR applications.

- [Conversational Bot](https://github.com/jaxl-innovations-private-limited/jaxl-ivr-confirmation-bot): A full-fledged working example on how to build a custom outgoing IVR flow. It simulates automated calls made to customers right after they place an order — either via your website or mobile app — allowing them to confirm or cancel with a single key press.


## ❓ What is an IVR?

```
Press 1 to confirm the transaction,
Press 2 to block the card and talk to our customer representation,
Press 3 to repeat the options
```

If you have ever experienced a call where the system is asking for your inputs like above, you already understand how an [IVR](https://en.wikipedia.org/wiki/Interactive_voice_response) works.

## 🎛️ Prompts

### 📝 Prompt Strings

Sentences spoken out by the system are referred to as **"Prompt Strings"**.

During a call, Jaxl IVR Infrastructure convert prompt strings into audio files and playback to the user over the call.

Some examples of prompt string includes:

1. Welcome to My Company.
2. Welcome to Jaxl. Press 1 for customer care. Press 2 for HR department.
3. Thank you for calling us. One of our customer representative will call you back soon. Bye
4. Welcome to Jaxl Payments. Your total amount due is 51 rupee. To make a payment please enter your credit card number followed by star.

### 🔊 Prompt Audios

Your IVR can also playback custom audio files. Example, playing out a music while the user waits. Such custom audio files are referred to as **"Prompt Audios"**.

A prompt string can also be followed by a prompt audio. Example:

1. Hello. You have reached Jaxl customer support. Please wait while we connect your call. "Prompt Audio playing music".

A prompt audio alone works too. Example:

1. "Prompt audio playing music"

## ℹ️ About Jaxl IVR Simulator

Jaxl IVR Simulator is available as a Docker container. It allows you to quickly build and test your custom IVRs.

In a nutshell, your IVR will be responsible for:

1. Returning [**"prompt strings"**](#prompt-strings) and/or [**"prompt audios"**](#prompt-audios) that will be spoken out to the user
2. Handle user inputs and return [**prompts**](#prompts) in reply to the user

At any point, IVRs can also return prompts followed by hangup to terminate the call.

## 🚀 Try Jaxl IVR Simulator

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

## 🛠️ Initialize your IVR Project Directory

1. Create a new directory that will contain your IVR code. For documentation purposes, let's imagine have created a new directory at following path on your system `/path/to/ivr/playground/directory`

   > NOTE: Use a path appropriate for your system.

2. Within your IVR project directory, run the following command:

   On Mac & Linux:

   ```bash
   docker run \
       -it --rm \
       -v ${PWD}:/jaxlivrsimulator/ivr \
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator init
   ```

   On Windows using cmd.exe

   ```bash
   docker run ^
       -it --rm ^
       -v %cd%:/jaxlivrsimulator/ivr ^
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator init
   ```

   On Windows using PowerShell

   ```bash
   docker run `
       -it --rm `
       -v ${PWD}:/jaxlivrsimulator/ivr `
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

## 🧪 Create your First IVR

`init` command has initialized your IVR project directory structure as expected by Jaxl IVR Simulator.

To create your first IVR:

1. Open your project directory in `VSCode`
2. Follow [`PROJECT.md`](./PROJECT.md) placed in your project directory for further instructions.

## 🐳 Docker Image Tags

Two variants of docker images are available.

| Base Image         | Image Size        | Tags           | Dynamic IVR | Realtime Audio & Transcription |
|--------------------|-------------------|----------------|-------------|--------------------------------|
| python:3.11-alpine | 6.2 GB (amd)      | latest, vN     | ✅          | ❌                             |
| python:3.11-alpine | 666.84 MB (arm)   | latest, vN     | ✅          | ❌                             |
| python:3.11-slim   | 58.91 MB (amd)    | realtime, vNr  | ✅          | ✅                             |
| python:3.11-slim   | 47.31 MB (amd)    | realtime, vNr  | ✅          | ✅                             |

Note the tag convention:

- Replace `N` with Docker release version you intend to use e.g. `v27`
- Suffix with `r` to run the realtime variant e.g. `v27r`
- Check available tags on [Docker Hub](https://hub.docker.com/r/jaxlinnovationsprivatelimited/jaxl-ivr-simulator/tags)

## 💬 Need Help?

This project is for client integrations only. For support or enterprise deployment, contact support@jaxl.com or write to us [jaxl.com/contact/](https://jaxl.com/contact/). Found a bug or have a feature request? [Open an issue on GitHub](https://github.com/jaxl-innovations-private-limited/jaxl-ivr-simulator/issues).
