@echo off
echo === Extracting messages ===
pybabel extract -F babel.cfg -o locales/messages.pot .

echo === Updating existing translations ===
pybabel update -d locales -i locales/messages.pot

echo === Done ===
pause
