@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION

IF "%1"=="" GOTO Usage
IF NOT EXIST "%1" GOTO NotExists

SET owd=%CD%

CD %1
SET cwd=%CD%
SET cp=%CLASSPATH%
FOR %%i IN (*.*) DO set cp=!cp!;%cwd%\%%i
ECHO %cp%
CD %owd%
GOTO End

:Usage
ECHO "Usage: cp.bat <GeoTools Directory>"
GOTO End

:NotExists
ECHO "Error: No such directory %1" 

:End
