@echo off
@rem A backup script of robocopy version.

set DRY_RUN=

@rem Back up %APPDATA% packages.

set TARGETS=GIMP/3.0 inkscape LibreOffice/4/user
set SRC_ROOT=%APPDATA%
set DEST_ROOT=E:\backup\AppData\Roaming
for %%i in (%TARGETS%) do (
    Robocopy "%SRC_ROOT%\%%i" "%DEST_ROOT%\%%i" %DRY_RUN% /MIR /E /ZB /COPYALL /DCOPY:t /XJ /R:0 /W:1
)

@rem Back up %USERPROFILE% without folders.

robocopy "%USERPROFILE%" "E:\backup" %DRY_RUN% /LEV:1 /R:1 /W:1 /ZB /XF "NTUSER*" "*.lnk"

@rem Back up %USERPROFILE% folders.

set TARGETS=devel Documents Music Pictures
for %%i in (%TARGETS%) do (
    Robocopy "%USERPROFILE%\%%i" "E:\backup\%%i" %DRY_RUN% /E /ZB /COPYALL /DCOPY:t /XJ /R:0 /W:1
)
