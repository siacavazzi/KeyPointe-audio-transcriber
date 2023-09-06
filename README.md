

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

## Libraries:
Whisper: The core model used to transcribe audio.
speech_recognition: Used to capture audio from the user's microphone.
torch: Provides deep learning capabilities, essential for the Whisper model.
WhisperMic Features:
Real-time transcription: Converts spoken words into written text on-the-fly.
English Transcription: Can be set to specifically transcribe English speech.
Energy Threshold Management: Dynamically adjusts the microphone's sensitivity to ambient noise.
Pause Detection: Determines the end of a user's statement based on pauses.
Temporary File Storage: If required, audio can be stored in temporary files.
3. Additional Modules
fuzzywuzzy: Assists in detecting similarity in strings, used for detecting end commands.
SQLite: A lightweight database management system used for storing transcriptions.

## Usage

Run KeyPointe.

A menu with options will be presented:

1 to start transcribing.
2 to view past transcriptions.
Type X to return to the main menu, a specific ID to view conversation details, or delete {id} to erase a conversation.
3 to reset or clear all saved conversations.
4 to terminate the program.
When transcribing, stating "end transcription" will signal the end of a recording session.

Remember that during transcription, background noises may influence accuracy, and KeyPointe's WhisperMic module might occasionally produce an inaccurate string, such as "Thanks for watching!" in quiet environments.

## Remarks & Considerations
Ensure that Torch and Whisper are compatible versions.
If running on macOS, MPS (Metal Performance Shaders) might not be compatible yet. Adjust settings accordingly.
Ensure the SQLite database is appropriately configured and accessible.
WhisperMic's listen function allows for transcription with a specified timeout, and listen_loop offers a continuous listening and transcription mode.
Future Developments
Implementation of the export feature for exporting transcriptions.
Finalizing the functionalities of the reset and exit methods.
Enhancements to the WhisperMic's microphone toggling capabilities.

## Dependencies
To run KeyPointe smoothly, ensure the following libraries are installed:

colorama
prettytable
fuzzywuzzy
whisper
torch
speech_recognition
pydub
pynput
SQLite (for database operations)
