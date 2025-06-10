*** Settings ***
Library           ../load_env.py
Resource          ../resources/wifi_keywords.robot

*** Test Cases ***

Check if Wifi Module is preset
    Check Wifi Module Exists

Check if Wifi Module is turned on
    Check Wifi Interface UP

Check if Wifi Module is able to scan Wi-Fi Network
    Scan Available Networks

Check if Wifi Module is able to connect to Wi-Fi Network
    ${env}=  Load Environment Variables
    ${SSID}=  Set Variable  ${env['SSID']}
    ${WIFI_PASSWORD}=  Set Variable  ${env['WIFI_PASSWORD']}
    Connect To Wifi    ${SSID}    ${WIFI_PASSWORD}

Verify Internet is working
    Ping Internet