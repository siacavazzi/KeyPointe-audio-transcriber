

# KeyPointe Transcription Program
## Overview
KeyPointe is a program designed to transcribe spoken words into written text using advanced audio processing technologies. The program enables users to record, transcribe, and manage transcribed conversations, storing them in a database for easy retrieval and management.

## Modules & Features
1. Core Modules
title: The header or title of the program when run.
transcribe: Contains the main function to transcribe spoken words.
colorama: Provides styling for the CLI for a better user experience.
overview: Handles summaries of each conversation, providing a quick overview.
prettytable: Enables structured table displays in the CLI.
conversation: Provides functionality to manage and interface with the SQLite database storing conversations.
2. WhisperMic
This is an integral part of KeyPointe, interfacing with the microphone and transcribing user's speech:

## Setup

### 1. Dependencies Installation
KeyPointe utilizes a Pipfile for dependency management. Ensure you have pipenv installed. If not, you can install it using:
```
pip install pipenv
```

Once you have pipenv ready, navigate to the root directory of the KeyPointe project and run:
```
pipenv install
```
This will install all the necessary dependencies from the Pipfile.

### 2. API Key Config
For KeyPointe to work correctly, an API key is required. Follow the steps below to set it up:

1. Create a new file in the root directory of the project and name it apiKey.py.
2. Open apiKey.py in a text editor of your choice.
3. Insert the following content, replacing "YOUR API KEY" with your actual API key:
```
key = "YOUR API KEY"
```



speech_recognition
pydub
pynput
SQLite (for database operations)
