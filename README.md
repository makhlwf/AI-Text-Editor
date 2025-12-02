# this app is a work in progress
Its not readdy for full use.

# AI Text Editor

AI Text Editor is a Windows application that brings the power of AI to any text field on your system. With a simple hotkey, you can instantly fix grammar, change the writing style of your text, or give it a direct instruction.

## Features

*   **Universal Compatibility:** Works in any application that supports text selection.
*   **Grammar Correction:** Instantly fix grammar and spelling mistakes in your text.
*   **Style Transformation:** Change the writing style of your text to be more professional, casual, or any other style you can imagine.
*   **Direct Instruction:** Give a direct instruction to the AI to modify your text in any way you want.
*   **Customizable Hotkey:** Set your own hotkey to trigger the AI assistant.
*   **System Tray Application:** Runs quietly in the background and is accessible from the system tray.

## How to Use

1.  Select any text in any application.
2.  Press the configured hotkey (default is `Ctrl+Alt+X`).
3.  A dialog will appear with the following options:
    *   **Fix Grammar:** Corrects grammar and spelling.
    *   **Change Style:** Prompts you to enter a new writing style.
    *   **Direct Instruction:** Allows you to give a specific instruction to the AI.
4.  The selected text will be replaced with the AI-generated text.

## Installation

1.  Clone this repository.
2.  Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3.  Run the `main.py` file:
    ```
    python main.py
    ```

## Configuration

The application settings can be configured by right-clicking the tray icon and selecting "Settings".

*   **API Key:** You need to provide your own Google AI API key. You can get one from [Google AI Studio](https://aistudio.google.com/).
*   **Shortcut:** You can change the hotkey that triggers the application.

The configuration is saved in `%APPDATA%\AITextEditor\config.json`.

## Dependencies

look in requirements.txt file for an uptodated list

## Disclaimer

This application sends your selected text to the Google AI API to provide its features. Please be mindful of the data you are sending and ensure you are not violating any privacy policies or terms of service.
