@echo off
@rem A backup script for Sleipnir.
@rem Usage: backup-sleipnir.bat
@rem Reference: <https://w.atwiki.jp/fenrirsleipnir/pages/207.html>

@rem Note: To perform a real backup, comment out the DRY_RUN line.
set DRY_RUN=/L

set SLEIPNIR=Fenrir Inc\Sleipnir5
set SRC_ROOT=%APPDATA%\%SLEIPNIR%
set DEST_ROOT=E:\backup\AppData\Roaming\%SLEIPNIR%
set ITEMS_TO_BACKUP=^
    ~temp\chrome\skins\default\widget\module\SearchEngine ^
    setting\override ^
    setting\modules\superdrag
    setting\client\favorite3.json ^
    setting\client\lastvisited.json ^
    setting\client\recently-tab.json ^
    setting\client\rebar.xml ^
    setting\client\tab.json ^
    setting\uri-action.json ^
    setting\client\user.ini ^
    setting\modules\ChromiumViewer\Default\Login Data ^
    setting\modules\ChromiumViewer\Default

for %%i in (%ITEMS_TO_BACKUP%) do (
    robocopy "%SRC_ROOT%\%%i" "%DEST_ROOT%\%%i" %DRY_RUN% /MIR /E /ZB /COPYALL /DCOPY:t /XJ /R:0 /W:1
)
