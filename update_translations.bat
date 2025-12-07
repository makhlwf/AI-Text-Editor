@echo off

set PROJECT_NAME=AI Text Editor
set PROJECT_VERSION=0.1beta
set AUTHOR_NAME=Makhlwf
set AUTHOR_EMAIL=Altrhwnyashrf1@gmail.com

echo === Extracting messages ===
pybabel extract ^
    -F babel.cfg ^
    -o locales/messages.pot ^
    --project="%PROJECT_NAME%" ^
    --version="%PROJECT_VERSION%" ^
    --copyright-holder="%AUTHOR_NAME%" ^
    --msgid-bugs-address="%AUTHOR_EMAIL%" ^
    --last-translator="%AUTHOR_NAME% <%AUTHOR_EMAIL%>" ^
    .

echo === Updating translations ===
pybabel update -d locales -i locales/messages.pot --update-header-comment

echo === Compiling ===
pybabel compile -d locales

echo === Done ===
pause
