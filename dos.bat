@echo off
setlocal EnableDelayedExpansion

rem ===== CONFIG =====
set "BASEDIR=%~dp0VIRTUAL_DRIVE"
set "TRASH=%BASEDIR%\$TRASH"
set "PROMPT=$P$G"
set "VERSION=Mini-OS Emu 1.0"
set "COMPUTERNAME=MY-PC"
set "OSNAME=Mini-OS Simulation"
set "OWNER=User"
rem ==================

rem ===== RESERVED NAMES =====
set "RESERVED=CON PRN AUX NUL COM1 COM2 COM3 COM4 LPT1 LPT2 LPT3"

rem ===== INIT VIRTUAL DRIVE =====
if not exist "%BASEDIR%" (
    md "%BASEDIR%" >nul 2>&1
    md "%TRASH%" >nul 2>&1
    md "%BASEDIR%\FILES" >nul 2>&1
    echo Note: this isnt emualating anything, just simulating. this .bat uses only VIRTUAL_DRIVE, doesnt touch your main drive  > "%BASEDIR%\FILES\README.TXT"
)

title %OSNAME% - %VERSION%
color 0a
cls
echo %OSNAME% [Version %VERSION%]
echo (C) 2025 %OWNER%. All rights reserved.
echo Type "help" for a list of commands.
echo.
cd /d "%BASEDIR%"

:mainloop
set /p "INPUT=%PROMPT%" || goto :eof
if "!INPUT!"=="" goto mainloop

for /f "tokens=1* delims= " %%A in ("!INPUT!") do (
    set "CMD=%%A"
    set "ARGS=%%B"
)

rem --- COMMAND HANDLER ---
if /i "!CMD!"=="exit" goto :eof
if /i "!CMD!"=="cls" cls & goto mainloop
if /i "!CMD!"=="help" goto cmd_help
if /i "!CMD!"=="dir" goto cmd_dir
if /i "!CMD!"=="cd" goto cmd_cd
if /i "!CMD!"=="md" goto cmd_md
if /i "!CMD!"=="mkdir" goto cmd_md
if /i "!CMD!"=="rd" goto cmd_rd
if /i "!CMD!"=="rmdir" goto cmd_rd
if /i "!CMD!"=="type" goto cmd_type
if /i "!CMD!"=="copy" goto cmd_copy
if /i "!CMD!"=="del" goto cmd_del
if /i "!CMD!"=="erase" goto cmd_del
if /i "!CMD!"=="ren" goto cmd_ren
if /i "!CMD!"=="rename" goto cmd_ren
if /i "!CMD!"=="date" goto cmd_date
if /i "!CMD!"=="time" goto cmd_time
if /i "!CMD!"=="ver" goto cmd_ver
if /i "!CMD!"=="prompt" goto cmd_prompt
if /i "!CMD!"=="sysinfo" goto cmd_sysinfo
if /i "!CMD!"=="trash" goto cmd_trash
if /i "!CMD!"=="cleartrash" goto cmd_cleartrash
if /i "!CMD!"=="calc" goto cmd_calc
if /i "!CMD!"=="notepad" goto cmd_notepad
if /i "!CMD!"=="game" goto cmd_game

echo Unknown command: !CMD!
goto mainloop

:cmd_help
echo.
echo Available commands:
echo  DIR [path]       - List directory contents
echo  CD [path]        - Change directory
echo  MD|MKDIR name    - Create directory
echo  RD|RMDIR name    - Remove directory (empty only)
echo  TYPE file        - Display text file
echo  COPY src dst     - Copy file
echo  DEL|ERASE file   - Move file to trash
echo  REN|RENAME a b   - Rename file/folder
echo  CLS              - Clear screen
echo  DATE             - Show date (simulated)
echo  TIME             - Show time (simulated)
echo  VER              - Show version
echo  PROMPT text      - Set command prompt
echo  SYSINFO          - Show system info
echo  TRASH            - List trash contents
echo  CLEARTRASH       - Empty trash
echo  CALC             - Mini calculator
echo  NOTEPAD <file>   - Open text file
echo  GAME             - Play mini game
echo  EXIT             - Quit emulator
goto mainloop

:cmd_dir
if "!ARGS!"=="" (
    dir /b /a "%BASEDIR%" 2>nul || echo Directory empty.
) else (
    if exist "%BASEDIR%\!ARGS!" (
        dir /b /a "%BASEDIR%\!ARGS!" 2>nul
    ) else echo Path not found: !ARGS!
)
goto mainloop

:cmd_cd
if "!ARGS!"=="" (
    echo %CD%
    goto mainloop
)
set "TARGET=%BASEDIR%\!ARGS!"
if exist "!TARGET!" (
    cd /d "!TARGET!"
) else echo Path not found: !ARGS!
goto mainloop

:cmd_md
if "!ARGS!"=="" (
    echo Syntax: MD folder
    goto mainloop
)
rem check reserved names
for %%R in (%RESERVED%) do (
    if /i "!ARGS!"=="%%R" (
        echo Cannot create reserved name: !ARGS!
        goto mainloop
    )
)
if exist "%CD%\!ARGS!" (
    echo Folder already exists: !ARGS!
    goto mainloop
)
md "%CD%\!ARGS!" >nul 2>&1 && echo Directory created: !ARGS! || echo Could not create directory.
goto mainloop

:cmd_rd
if "!ARGS!"=="" (
    echo Syntax: RD folder
    goto mainloop
)
if exist "%CD%\!ARGS!" (
    rd "%CD%\!ARGS%" 2>nul && echo Directory removed: !ARGS! || echo Could not remove (maybe not empty).
) else echo Folder not found: !ARGS!
goto mainloop

:cmd_type
if "!ARGS!"=="" (
    echo Syntax: TYPE file
    goto mainloop
)
if exist "%CD%\!ARGS!" (
    type "%CD%\!ARGS%"
) else echo File not found: !ARGS!
goto mainloop

:cmd_copy
for /f "tokens=1,2*" %%X in ("!ARGS!") do (
    set "SRC=%%X"
    set "DST=%%Y"
)
if not defined DST (
    echo Syntax: COPY source destination
    goto mainloop
)
if exist "%CD%\!SRC!" (
    copy "%CD%\!SRC!" "%CD%\!DST%" >nul && echo File copied.
) else echo Source file not found: !SRC!
goto mainloop

:cmd_del
if "!ARGS!"=="" (
    echo Syntax: DEL file
    goto mainloop
)
if exist "%CD%\!ARGS!" (
    if not exist "%TRASH%" md "%TRASH%" >nul 2>&1
    copy "%CD%\!ARGS!" "%TRASH%\!ARGS!" >nul
    del "%CD%\!ARGS!" >nul
    echo File moved to trash.
) else echo File not found: !ARGS!
goto mainloop

:cmd_ren
for /f "tokens=1,2*" %%X in ("!ARGS!") do (
    set "OLD=%%X"
    set "NEW=%%Y"
)
if exist "%CD%\!OLD!" (
    rem prevent reserved names
    for %%R in (%RESERVED%) do (
        if /i "!NEW!"=="%%R" (
            echo Cannot rename to reserved name: !NEW!
            goto mainloop
        )
    )
    ren "%CD%\!OLD!" "!NEW!" >nul 2>&1 && echo Renamed: !OLD! -> !NEW! || echo Rename failed.
) else echo File not found: !OLD!
goto mainloop

:cmd_date
echo Current date (simulated): %date%
goto mainloop

:cmd_time
echo Current time (simulated): %time%
goto mainloop

:cmd_ver
echo %VERSION%
goto mainloop

:cmd_prompt
if "!ARGS!"=="" (
    echo Current prompt: %PROMPT%
    goto mainloop
)
set "PROMPT=!ARGS!"
goto mainloop

:cmd_sysinfo
echo Computer Name: %COMPUTERNAME%
echo OS: %OSNAME%
echo Version: %VERSION%
echo Directory: %CD%
goto mainloop

:cmd_trash
echo Trash contents:
dir "%TRASH%" 2>nul || echo Trash is empty.
goto mainloop

:cmd_cleartrash
del /q "%TRASH%\*" >nul 2>&1
echo Trash emptied.
goto mainloop

:cmd_calc
echo Mini Calculator (type 'exit' to leave)
:calcloop
set /p "EXPR=> " || goto mainloop
if /i "!EXPR!"=="exit" goto mainloop
set /a RESULT=!EXPR! 2>nul
if defined RESULT (
    echo Result: !RESULT!
) else (
    echo Invalid expression
)
goto calcloop

:cmd_notepad
if "!ARGS!"=="" (
    echo Syntax: NOTEPAD filename
    goto mainloop
)
start notepad "%CD%\!ARGS!"
goto mainloop

:cmd_game
set /a TARGET=%RANDOM% %% 100 +1
echo Guess a number between 1 and 100. Type 'exit' to quit.
:game_loop
set /p "GUESS=> " || goto mainloop
if /i "!GUESS!"=="exit" goto mainloop
set /a GUESSNUM=!GUESS! 2>nul
if !GUESSNUM! lss !TARGET! (
    echo Too low!
    goto game_loop
)
if !GUESSNUM! gtr !TARGET! (
    echo Too high!
    goto game_loop
)
echo Congratulations! You guessed the number !TARGET! 🎉
goto mainloop

:eof
echo Goodbye!
endlocal
exit /b 0
