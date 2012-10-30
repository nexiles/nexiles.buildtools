@echo off

:: handle args
set js_file=%1
set file=%js_file:.js=%

:: change to the working directory to the script location
@cd /D %~dp0

:: shrinksafe
@cd ..\shrinksafe
java -jar shrinksafe.jar %js_file% >%file%.compressed.js

:: jspack
@cd ..\jspack
jspacker.pl -i %file%.compressed.js -o %file%.compressed.js -e62 -f
