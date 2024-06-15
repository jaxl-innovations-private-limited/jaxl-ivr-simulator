# Jaxl IVR Project

Welcome to Jaxl IVR Project.

# Table of Contents

- [Project structure](#project-structure)
- [Create Python Virtual Environment](#create-python-virtual-environment)
- [Create IVR](#create-ivr)
- [Jaxl API Credentials](#jaxl-api-credentials)
- [Run IVR](#run-ivr)
- [Test IVR using Web Simulator](#test-ivr-using-web-simulator)
  - [IVR States](#ivr-states)
  - [Mock IVR State for Simulation](#mock-ivr-state-for-simulation)
  - [Developing for Parallel Calls](#developing-for-parallel-calls)

## Project structure

Generated IVR project contains following important files & directories:

1. `webhooks`: This directory will contain your IVR webhook code in Python language.
2. `schemas`: This directory will contain your IVR definitions in JSON format.
3. `ivr.json`: Jaxl IVR schema definition. All IVR definitions under `schemas` must adhere to `ivr.json` definition. If you are using `VSCode`, we have already configured `VSCode` settings to provide autocomplete when editing your JSON `schemas`.

## Create Python Virtual Environment

Open terminal in `VSCode` and run following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make sure `VSCode` is now using our Python virtual environment as default interpreter.

## Create IVR

1. Choose an appropriate name for your IVR. In this tutorial, we'll build an IVR `calculator`.
2. Generate skeleton schema and webhook code file using following command:

   On Mac & Linux:

   ```bash
   docker run \
       -it --rm \
       -v ${PWD}:/jaxl/ivr \
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator create calculator
   ```

   On Windows using cmd.exe

   ```bash
   docker run ^
       -it --rm ^
       -v %cd%:/jaxl/ivr ^
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator create calculator
   ```

   On Windows using PowerShell

   ```bash
   docker run `
       -it --rm `
       -v ${PWD}:/jaxl/ivr `
       jaxlinnovationsprivatelimited/jaxl-ivr-simulator create calculator
   ```

## Jaxl API Credentials

1. You will need `jaxl-api-credentials.json` file to run your IVRs
2. Download and place the credentials file at the root of your IVR project directory

## Run IVR

Execute following command to simulate your IVR flow using Jaxl IVR Simulator:

On Mac & Linux:

```bash
docker run \
    -it --rm \
    -v ~/.jaxl:/jaxl/.jaxl \
    -v ~/.proxy:/jaxl/.proxy \
    -v ${PWD}:/jaxl/ivr \
    jaxlinnovationsprivatelimited/jaxl-ivr-simulator run calculator
```

On Windows using cmd.exe

```bash
docker run ^
    -it --rm ^
    -v C:\Users\YourUsername\.jaxl:/jaxl/.jaxl ^
    -v C:\Users\YourUsername\.proxy:/jaxl/.proxy ^
    -v %cd%:/jaxl/ivr ^
    jaxlinnovationsprivatelimited/jaxl-ivr-simulator run calculator
```

On Windows using PowerShell

```bash
docker run `
    -it --rm `
    -v C:\Users\YourUsername\.jaxl:/jaxl/.jaxl `
    -v C:\Users\YourUsername\.proxy:/jaxl/.proxy `
    -v ${PWD}:/jaxl/ivr `
    jaxlinnovationsprivatelimited/jaxl-ivr-simulator run calculator
```

## Test IVR using Web Simulator

1. NOTICE the following line printed on your terminal:

   `Visit https://transport.jaxl.app/ivr/simulator/?..., your device_id is XXXX`

2. Open the URL _(printed on your terminal)_ in a browser to start interacting and testing your IVR.

3. Read [IVR.md](./IVR.md) for further documentation on how schemas and webhooks can be used together to create variety of dynamic IVR flows.

### IVR States

When an IVR is executed within a real phone call, your webhook received certain metadata about the call. Example:

1. call_id
2. from_number
3. to_number

### Mock IVR State for Simulation

By default state values are missing when IVR is running under simulation. However, during development you can easily pass custom state variables via query parameters. Example:

`http://localhost:29876/?call_id=1234&from_number=+919999999999&to_number=+919199999999`

Above, we mocked state to express an incoming call from `+919999999999` with `call_id=1234`.

### Developing for Parallel Calls

You can open the web simulator URL multiple times _(across different browser)_ to simulate parallel calls interacting with your IVR code.

NOTE: You SHOULD pass different values for `call_id` and `from_number` when testing parallel calls. After all, in real life scenario, each call will have a unique `call_id` and likely come from different `from_number`s.
