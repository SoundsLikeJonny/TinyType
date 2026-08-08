; TinyType NSIS Installer Script
; Passed in from build.py:
;   /DAPP_VERSION=x.y.z
;   /DBUILD_DIR=path\to\builds\TinyType_timestamp\TinyType

Unicode True

!ifndef APP_VERSION
  !define APP_VERSION "0.1.0"
!endif
!ifndef BUILD_DIR
  !define BUILD_DIR "dist\TinyType"
!endif

!define APP_NAME        "TinyType"
!define APP_PUBLISHER   "Jon Evans"
!define APP_URL         "https://github.com/SoundsLikeJonny/TinyType"
!define APP_EXE         "TinyType.exe"
!define UNINSTALL_KEY   "Software\Microsoft\Windows\CurrentVersion\Uninstall\TinyType"
!define STARTUP_KEY     "Software\Microsoft\Windows\CurrentVersion\Run"

Name "${APP_NAME} ${APP_VERSION}"
OutFile "builds\TinyType-Setup-${APP_VERSION}.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "${UNINSTALL_KEY}" "InstallLocation"
RequestExecutionLevel admin
ShowInstDetails show
ShowUninstDetails show

; ---------------------------------------------------------------
; Pages
; ---------------------------------------------------------------
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ---------------------------------------------------------------
; Launch TinyType unelevated after install.
; The installer itself runs elevated (RequestExecutionLevel admin),
; so a direct Run would make TinyType inherit elevation. An elevated
; process cannot receive PowerToys/AutoHotkey injected keys (UIPI),
; so we shell out through the unelevated explorer.exe instead.
; ---------------------------------------------------------------
!define MUI_FINISHPAGE_RUN ""
!define MUI_FINISHPAGE_RUN_FUNCTION "LaunchAppUnelevated"
Function LaunchAppUnelevated
  Exec '"$WINDIR\explorer.exe" "$INSTDIR\${APP_EXE}"'
FunctionEnd

; ---------------------------------------------------------------
; Installer section
; ---------------------------------------------------------------
Section "Install" SecInstall
  SetOutPath "$INSTDIR"
  File /r "${BUILD_DIR}\*.*"

  ; Uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"

  ; Add/Remove Programs registry
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayName"      "${APP_NAME}"
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "UninstallString"  '"$INSTDIR\uninstall.exe"'
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "InstallLocation"  "$INSTDIR"
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayVersion"   "${APP_VERSION}"
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "Publisher"        "${APP_PUBLISHER}"
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "URLInfoAbout"     "${APP_URL}"
  WriteRegStr   HKLM "${UNINSTALL_KEY}" "DisplayIcon"      "$INSTDIR\${APP_EXE}"
  WriteRegDWORD HKLM "${UNINSTALL_KEY}" "NoModify"         1
  WriteRegDWORD HKLM "${UNINSTALL_KEY}" "NoRepair"         1

  ; Start menu shortcut
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" \
                  "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}"
  CreateShortCut  "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk" \
                  "$INSTDIR\uninstall.exe"

  ; Desktop shortcut (optional — comment out to remove)
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}"

  ; Launch at Windows startup (system-tray app)
  WriteRegStr HKCU "${STARTUP_KEY}" "${APP_NAME}" '"$INSTDIR\${APP_EXE}"'
SectionEnd

; ---------------------------------------------------------------
; Uninstaller section
; ---------------------------------------------------------------
Section "Uninstall"
  ; Remove all installed files
  RMDir /r "$INSTDIR"

  ; Shortcuts
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall ${APP_NAME}.lnk"
  RMDir  "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"

  ; Registry
  DeleteRegKey  HKLM "${UNINSTALL_KEY}"
  DeleteRegValue HKCU "${STARTUP_KEY}" "${APP_NAME}"

  ; NOTE: user data in %APPDATA%\TinyType is intentionally left intact
  ;       so the user's config and stats survive a reinstall.
SectionEnd
