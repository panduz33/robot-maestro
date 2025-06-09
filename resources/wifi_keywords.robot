*** Settings ***
Library    Process

*** Keywords ***
Check Wifi Module Exists
    ${result}=    Run Process    iw dev    shell=True
    Should Contain    ${result.stdout}    Interface

Check Wifi Interface UP
    ${result}=    Run Process    ip link show wlan0    shell=True
    Should Contain    ${result.stdout}    state UP

Scan Available Networks
    ${result}=    Run Process    sudo iwlist wlan0 scan | grep ESSID    shell=True
    Log    ${result.stdout}

Connect To Wifi
    [Arguments]    ${ssid}    ${password}
    ${result}=    Run Process    nmcli device wifi connect ${ssid} password ${password}    shell=True
    Log    ${result.stdout}
    Should Not Contain    ${result.stdout}    Error

Verify Wifi Connection
    [Arguments]    ${expected_ssid}
    ${result}=    Run Process    iwgetid -r    shell=True
    Should Be Equal    ${result.stdout.strip()}    ${expected_ssid}

Check IP Assigned
    ${result}=    Run Process    ip addr show wlan0    shell=True
    Should Contain    ${result.stdout}    inet

Ping Internet
    ${result}=    Run Process    ping -c 2 8.8.8.8    shell=True
    Should Contain    ${result.stdout}    bytes from
