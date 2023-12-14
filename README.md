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
- [References](#references)


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

* Model <br>
    This is the main layer, which defines the Configurator class, implementing its main methods and interacting with the other layers. Thus, it is the start entry of the component. It has the methods for configuring the other components (Simulator and Adapter), which is done after the Validator functions are executed successfully. After that, the Asserter functions are called to validate the adaptation strategies.

* Validator <br>
    It implements the functions to validate the syntax of the modelling.

* Asserter <br>
    It implements the functions to assert whether the strategies are valid or not for the given application scenarios.

* Utils <br>
    It has various functions that are useful for all other layers. 

### Simulator

* Simulator <br>
    This is the main layer, which defines the Simulator class, implementing its main methods and interacting with the other layers. It instatiates the resources of the application and has methods for interacting with each, such as to get/change status or send a message, where for this last it uses the Publisher layer.

* Resource <br>
    This layer defines the resources attributes and methods. It uses the Communication Service for setting the communication environment.

* Communication Service <br>
    This layer implements the functions for using RabbitMQ. 

* Publisher <br>
    This layer implements the functions for publishing messages. 

* Subscriber <br>
    This layer implements the functions for consuming messages. 

* Utils <br>
    It has various functions that are useful for all other layers.

### Adapter
    
This component is divided into two modules, where each has its own structure. <br>
    
#### **Observer**

* Observer <br>
    This is the main layer, which deifnes the Observer class, implementing its main methods and interaction with the other layers. It first connects with the communication broker using  the functions from the Communication Service. Next, it starts the thread of execution of this module, where, for each message received, the Monitor Analyse Service is called.

* Communication Service <br>
    This layer implements the functions for using RabbitMQ. 

* Monitor Analyse Service <br>
    This layer implements the MAPE activities that are due to this module, which are the Monitor and Analyse. It has the functions to analyse if a modeled scenario is occurring in the application.

* Utils <br>
    It has various functions that are useful for all other layers.

#### **Effector**

* Effector <br>
    This is the main layer, which defines the Effector class, implementing its main methods and interacting with the other layers. It first reads the strategies modeled using the Strategies Interpretation function. It has two main methods that are used by the Observer. First, the _adapt_ method, that receives the scenario and calls the Plan Execute Service. Next, it is the _return\_to\_previous_, where, when it is a Cautious Adaptation, reset the affected resource to its previous state. 

* Strategies Interpretation <br>
    This layer has the function of receiving the strategies modeled and convert it into a dictionary.

* Plan Execute Service <br>
    This layer implements the MAPE activities that are due to this module, which are the Plan and Execute. It has the functions to receive a scenario and choose the proper target/action to be applied. 

* Utils <br>
    It has various functions that are useful for all other layers.


## Running Examples
### Baby Monitor
#### **Description**
The Baby Monitor example is based on the work of Fonseca _et al._ (2021) and it consists of an IoT system including a baby monitor, a smart TV, a smart light, a digital assistant, and a smartphone. The system's objective is to increase the chance that users will get a notification from the baby monitor device when the baby needs assistance. Every signal from the baby monitor is sent to the smartphone and is either classified as "normal" or "notification", with the latter requiring visual confirmation. In the absence of a response for a notification from the parents, the message is sent to the smart TV. However, third-party apps cause the smart TV to lock the notification display, thus needing an adaptation to allow it to show the messages. Here, the request for the TV to unlock and show the notice is the adaption strategy. However, if for some reason this strategy fails, the message can be forwarded to either the smart lamp or the assistant. The first blinks to indicate the notification, and the latter enunciates the message received.

#### **Run**
The full modelling of this example can be found at ```scripts/models/bm_model.json```. To execute this example, run the following commands: 

```
cd scripts
python3 run_example.py baby-monitor
```

### Smart Home
#### **Description**
The Smart Home example is based on the systems mentioned in Park _et al._ (2007), Alisavath  _et al._ (2017) and  Lee _et al._ (2022). The system's goal is to maintain appropriate levels of temperature, humidity, and light. To achieve this, sensors continuously monitor the environment, and various gadgets are available to help meeting the necessary criteria.

The system has predetermined thresholds for each condition. For example, when people are present, the temperature should be between 20°C and 30°C, with good brightness and humidity. Given the system's goal, it is possible to identify circumstances that would make it difficult for the system to uphold it, _i.e._ scenarios in which the system needs an adaptation.

Therefore, three adaptation scenarios and the appropriate actions were specified for this system. First, if a human is detected and the temperature is 30ºC or higher while the air conditioner is off, it should be turned on. Second, if there is a human in the house and the temperature is 20°C or lower while the air conditioner is on, it should be turned off. The final scenario is to open the window if the brightness and humidity are below the satisfaction threshold. Such scenarios were adapted from the adaptation scenarios on the original works, where the first two are presented in Park _et al._ (2007) and the last is on Lee _et al._ (2022).

The system communicates with users through a Manager component. For the first two scenarios, if turning on/off the air conditioner is not possible, an alternative action would be alerting the user. As for the last scenario, switching on the lights and humidifier would be an alternative if opening the window is not possible. Therefore, the system components include a Manager who receives all sensor data from windows, a lamp, a humidifier, and an air conditioner. These elements are essential for preserving the system's objective and are used in adaptation actions/strategies.

#### **Run**
The full modelling of this example can be found at ```scripts/models/sh_model.json```. To execute this example, run the following commands: 

```
cd scripts
python3 run_example.py smart-home
```


### Driver Assistance

#### **Description**
The Autonomous Vehicle example is based on a cyber-physical system presented by Antonino _et al._ (2018). The system consists of an IoT-enabled vehicle, the traffic management centers, and the surrounding vehicles. The goal of the system is to maintain the driver's security. Driver fatigue can pose a risk to safety, as it can interfere with driving and be perceived through vehicle behavior such as the steering pattern and the position in the lane.%For that, there are situations that require the vehicle to adapt, such as driver fatigue. 

The authors already described two adaptation scenarios and their associated actions, which are depicted in Figure \ref{fig:av-example}. In the first scenario, the speed sensor detects high speed, and the system applies brake assistance to slow down. In the second scenario, the driver has heavily consumed alcohol, and the system requests steering assistance. In both cases, notifying an emergency contact is the contingency action, in case the actions mapped can not be applied. 

The system described in the scenarios consists of several resources, including two primary sensors for detecting alcohol levels and speed. Additionally, the system provides brake and steering assistance to support driver safety. To facilitate communication with the user or emergency contacts, the system includes a Manager.

#### **Run**
The full modelling of this example can be found at ```scripts/models/av_model.json```. To execute this example, run the following commands: 

```
cd scripts
python3 run_example.py autonomous-vehicle
```

## References

A. Fonseca et al., "Dealing with IoT Defiant Components," 2021 IEEE/ACM Joint 9th International Workshop on Software Engineering for Systems-of-Systems and 15th Workshop on Distributed Software Development, Software Ecosystems and Systems-of-Systems (SESoS/WDES), Madrid, Spain, 2021, pp. 24-31, doi: 10.1109/SESoS-WDES52566.2021.00009.

J. Park, M. Moon, S. Hwang and K. Yeom, "CASS: A Context-Aware Simulation System for Smart Home," 5th ACIS International Conference on Software Engineering Research, Management & Applications (SERA 2007), Busan, Korea (South), 2007, pp. 461-467, doi: 10.1109/SERA.2007.60.

K. Non-Alisavath, S. Kanthavong, K. Luangxaysana and X. Louangvilay, "Context-awareness application to control multiple sensors for monitoring smart environment," 2017 14th International Conference on Electrical Engineering/Electronics, Computer, Telecommunications and Information Technology (ECTI-CON), Phuket, Thailand, 2017, pp. 920-923, doi: 10.1109/ECTICon.2017.8096388.

E. Lee, Y. -D. Seo and Y. -G. Kim, "Self-Adaptive Framework With Master–Slave Architecture for Internet of Things," in IEEE Internet of Things Journal, vol. 9, no. 17, pp. 16472-16493, 1 Sept.1, 2022, doi: 10.1109/JIOT.2022.3150598.

P. O. Antonino, A. Morgenstern, B. Kallweit, M. Becker and T. Kuhn, "Straightforward Specification of Adaptation-Architecture-Significant Requirements of IoT-enabled Cyber-Physical Systems," 2018 IEEE International Conference on Software Architecture Companion (ICSA-C), Seattle, WA, USA, 2018, pp. 19-26, doi: 10.1109/ICSA-C.2018.00012.
