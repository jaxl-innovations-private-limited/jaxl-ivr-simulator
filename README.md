# Amazon Order Tracking IVR

Welcome to the Amazon Order Tracking IVR project.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Running the IVR](#running-the-ivr)
- [Testing](#testing)

## Project Structure

The project contains the following files and directories:

- `schemas/`: Contains the IVR schema definitions.
- `tests/`: Contains unit tests for the webhook.
- `webhooks/`: Contains the webhook logic.
- `.gitignore`: Lists files and directories to be ignored by git.
- `requirements.txt`: Lists the Python dependencies.
- `ivr.json`: Defines the IVR schema for validation purposes.
- `IVR.md`: Provides documentation on creating and using the IVR system.
- `README.md`: This file.

## Setup

1. Create a Python virtual environment and install dependencies:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Make sure VSCode is using the Python virtual environment as the default interpreter.

## Running the IVR

1. Generate the IVR schema and webhook code:

    On Mac & Linux:

    ```bash
    docker run \
        -it --rm \
        -v ${PWD}:/jaxl/ivr \
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator create amazon_order_tracking
    ```

    On Windows using cmd.exe:

    ```bash
    docker run ^
        -it --rm ^
        -v %cd%:/jaxl/ivr ^
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator create amazon_order_tracking
    ```

    On Windows using PowerShell:

    ```bash
    docker run `
        -it --rm `
        -v ${PWD}:/jaxl/ivr `
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator create amazon_order_tracking
    ```

2. Run the IVR simulation:

    On Mac & Linux:

    ```bash
    docker run \
        -it --rm \
        -v ~/.jaxl:/jaxl/.jaxl \
        -v ~/.proxy:/jaxl/.proxy \
        -v ${PWD}:/jaxl/ivr \
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator run amazon_order_tracking
    ```

    On Windows using cmd.exe:

    ```bash
    docker run ^
        -it --rm ^
        -v %USERPROFILE%\.jaxl:/jaxl/.jaxl ^
        -v %USERPROFILE%\.proxy:/jaxl/.proxy ^
        -v %cd%:/jaxl/ivr ^
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator run amazon_order_tracking
    ```

    On Windows using PowerShell:

    ```bash
    docker run `
        -it --rm `
        -v ${HOME}\.jaxl:/jaxl/.jaxl `
        -v ${HOME}\.proxy:/jaxl/.proxy `
        -v ${PWD}:/jaxl/ivr `
        jaxlinnovationsprivatelimited/jaxl-ivr-simulator run amazon_order_tracking
    ```

## Testing

Run the tests to ensure your code is working correctly:

On Mac & Linux:

```bash
docker run \
    -it --rm \
    -v ~/.jaxl:/jaxl/.jaxl \
    -v ~/.proxy:/jaxl/.proxy \
    -v ${PWD}:/jaxl/ivr \
    jaxlinnovationsprivatelimited/jaxl-ivr-simulator check
