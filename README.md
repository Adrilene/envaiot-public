# EnvAIoT

The **Env**ironment for modeling and simulating **A**daptive **I**nternet **o**f **T**hings applications is a tool that may assist IoT system designers, engineers, architects, and developers in the design phase of an IoT system, focusing on the system's self-adaptation features and providing an approach to model and validate if their adaptation strategies are effective in the presence of known and unknown uncertain contexts. 

## Topics
- [Getting Started](#getting-started)
    - [Requirements](#requirements)
    - [Running EnvAIoT](#running-envaiot)
- [Architecture](#architecture)
    - [Configurator](#configurator)
    - [Simulator](#simulator)
    - [Adapter](#adapter)
- [Running Examples](#running-examples)
    - [Baby Monitor](#baby-monitor)
    - [Smart Home](#smart-home)
    - [Driver Assistance](#driver-assistance)

## Getting Started

### Requirements
- Python 3.x
- Postman (Non-Mandatory)
- Internet Access

### Running EnvAIoT

1. After cloning this project, let's first prepare the environment.<br>
    1.1 Creating a virtual environment <br>
    *On Windows:*
    ```
    python -m venv env
    ```

    *On Linux distributions:*
    ```
    virtualenv env
    ```
    <br>

    1.2 Activating the virtual environment. <br>
    *On Windows:*
    ```
    cd env
    Scripts\activate
    cd ..
    ```

    *On Linux distributions:*
    ```
    source env/bin/activate
    ```

    <br>
    1.3 Installing the dependencies: <br>
    
    ```
    pip install -r requirements.txt
    ```

2. Running the application <br>
    *On Windows:*
    ```
    python application.py
    ```

    *On Linux distributions:*
    ```
    python3 application.py
    ```

Now, EnvAIoT is ready to receive and model an IoT application. In the following, let's run the pre-ready three examples we have by running the scripts. Each example is defined in the section 

## Architecture
This tool consits of an Application Programming Interface, which receives modelling of IoT applications and return an evaluation of whether the adaptation strategies are able to deal with the adaptation scenarios defined. It was all implemented using Flask, a python framework for web applications. It is composed of three main components: *Configurator, Simulator, and Adapter*. The architecture of each will be described next:

### Configurator
This component is implemented using a layer architecture, which are the following:

* Controller <br>

* Validator
* Asserter
* Utils


### Simulator

### Adapter


## Running Examples
### Baby Monitor

### Smart Home

### Driver Assistance
