@ECHO OFF

REM SETLOCAL ENABLEDELAYEDEXPANSION

REM ensure JYTHON_HOME_DIR set
IF NOT DEFINED JYTHON_HOME_DIR (
  GOTO NO_JYTHON_HOME
)

REM ensure jython.bat can be found
SET JYTHON_EXE="%JYTHON_HOME_DIR%\jython.bat"
IF NOT EXIST %JYTHON_EXE% (
  GOTO NO_JYTHON
)

REM run geoscript-classpath script
FOR /f "tokens=*" %%X IN ('%JYTHON_EXE% %~dp0geoscript-py-classpath') DO (
    SET CLASSPATH=%%X
)

%JYTHON_EXE%
SET JYTHON_EXE=

:NO_JYTHON_HOME
ECHO Error, JYTHON_HOME_DIR is unset. Please set JYTHON_HOME_DIR to root of Jython installation.
GOTO DONE

:NO_JYTHON
ECHO Error, JYTHON_HOME_DIR was set but could not find 'jython' exe.
GOTO DONE

:DONE
