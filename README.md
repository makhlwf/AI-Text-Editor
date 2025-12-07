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

## Translations

This application supports multiple languages. You can change the language in the settings menu.

### How to Add a New Language

If you would like to contribute by adding a new language, follow these steps:

1.  **Add the language to the settings dialog:**
    *   Open `ui/settings_dialog.py`.
    *   Add the new language to `self.language_map` and `self.reverse_language_map`. Use the two-letter ISO 639-1 code for the language.

2.  **Generate the `.po` file:**
    *   Open a terminal in the root directory of the project.
    *   Run the following command, replacing `[lang]` with the two-letter language code:
        ```
        pybabel init -i locales/messages.pot -d locales -l [lang]
        ```

3.  **Translate the text:**
    *   Open the newly created `.po` file at `locales/[lang]/LC_MESSAGES/messages.po`.
    *   For each `msgid`, add the translation in the `msgstr` field.

4.  **Compile the translations:**
    *   Run the following command in the terminal:
        ```
        pybabel compile -d locales
        ```

5.  **Submit a pull request:**
    *   Once you have completed the translation, please submit a pull request with your changes.
