# About the Repository:

Licy is a Software License chatbot written with the Rasa Python framework that assists users to find the appropriate Open Source Software (OSS) license for their software based on their requirements, while it also provides users with information on specifc OSS licenses.


# Technologies used:


## Frontend

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

For the user interface html was used for the structure, CSS combined with the bootstrap framework was used to style the interface and Javascript for the dynamic functionality of the interface.

## Backend
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase)

 - Flask microframework was used providing routing capabilities, request handling, session management, and other essential functionalities for building and running the web-based chatbot application.
 - Firebase was used to store some user data during the conversation with the chatbot.

## Chatbot NLU and Logic
![Rasa Logo](https://assets-global.website-files.com/62b47d61d86f711fb67c73ce/63e7d3977c60db242ac49c9e_Rasa.webp)

Rasa is an open-source framework for building conversational AI chatbots and virtual assistants. It allows developers to create sophisticated, natural language understanding (NLU)-powered bots capable of engaging in text-based conversations with users.

Here are some key components and features of the Rasa framework:

1.  **Natural Language Understanding (NLU)**: Rasa includes components for NLU, which enable the chatbot to understand and extract intents (the user's goal or intention) and entities (relevant pieces of information) from user messages. Rasa NLU uses machine learning algorithms to perform intent classification and entity recognition.
    
2.  **Dialogue Management**: Rasa provides tools for managing the dialogue flow of the conversation. This includes defining the dialogue structure, managing context, handling multi-turn conversations, and deciding how the bot should respond based on the current state of the conversation.
    
3.  **Customizable Machine Learning Models**: Rasa allows developers to customize and train machine learning models for NLU and dialogue management based on their specific use cases and data. This flexibility enables developers to create chatbots tailored to their domain and requirements.
    
4.  **Integration with Existing Platforms**: Rasa can be integrated with various messaging platforms and channels, such as Facebook Messenger, Slack, WhatsApp, and custom web interfaces. This allows developers to deploy their chatbots across multiple platforms and reach users wherever they are.
    
5.  **Open-Source and Community-Driven**: Rasa is open-source software, which means it is freely available for anyone to use, modify, and contribute to. The Rasa community actively develops new features, improves existing functionality, and provides support to users through forums, documentation, and other resources.
    
6.  **Scalability and Extensibility**: Rasa is designed to be scalable and extensible, allowing developers to build complex conversational experiences and integrate with external systems and APIs. It supports the development of custom components and plugins to extend its functionality as needed.
    

Overall, Rasa provides a powerful platform for building AI-driven chatbots and virtual assistants that can understand user input, carry out conversations, and perform tasks or provide information based on user requests. Its flexibility, customizability, and open-source nature make it a popular choice for developers looking to create conversational AI solutions.

# How to create the environment and install the chatbot (Guide)

## Install Anaconda on your machine.

Anaconda is a popular open-source distribution of Python and R programming languages that is used for scientific computing, data science, and machine learning tasks. It provides a comprehensive suite of tools, libraries, and packages that are commonly used in these fields, making it easier for users to set up and manage their development environments.

You can find the installation process: 

### On windows:
https://docs.anaconda.com/free/anaconda/install/windows/

### On macOS:
https://docs.anaconda.com/free/anaconda/install/mac-os/

### On linux:
https://docs.anaconda.com/free/anaconda/install/linux/

> From Terminal: https://phoenixnap.com/kb/install-anaconda-ubuntu.

## Create a virtual environment with anaconda.
You need to create a virtual environment using Python 3.9 which is compatible with the Rasa framework:

**conda create -n envname python**=**3.9**

## Install tensorflow which is used for Rasa training.

command:
**pip install tensorflow**

## Install Rasa python framework
command:
**pip install rasa**

## Clone the repository from Github.
command:
**git clone https://github.com/giorgosshittasCS/License_Chatbot_V2**

## Start services

You need to run a bash script so we can enable the rasa api, run the Flask server in Python and run the rasa action server to handle some custom actions written. Create the file in the **src** folder.

### For windows('start_services.bat' file):

```bat
*@echo off
rem Command 1: Run  the rasa action server in the background
start "" rasa run actions
rem Command 2: Run another Rasa process with API enabled
start "" rasa run --enable-api
rem Command 3: Change directory and run the Flask server in the background
cd backend && start "" python chatbot.py*
```
#### To run the bat script: 
./start_services.bat


### For MacOS and Linux('start_services.sh' file):
```bash
*#!/bin/bash
#Command 1: Run  the rasa action server in the background
rasa run actions &
#Command 2: Run another Rasa process with API enabled
rasa run --enable-api &
#Command 3: Change directory and run the Flask server in the background
cd backend && python chatbot.py &*
```

#### To run the bash script: 
./start_services.sh

### You can interfere with the chatbot on localhost address written in chatbot.py file: 

http://127.0.0.1:5000/

**You can change the address inside the chatbot.py file.**
