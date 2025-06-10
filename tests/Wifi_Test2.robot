*** Settings ***
Resource  ../resources/wifi_keywords.robot
Library   ../load_env.py

*** Test Cases ***
Basic Wifi Functionality Test
    ${env}=  Load Environment Variables
    ${SSID}=  Set Variable  ${env['SSID']}
    ${WIFI_PASSWORD}=  Set Variable  ${env['WIFI_PASSWORD']}
    ${EXPECTED_SSID}=  Set Variable  ${env['EXPECTED_SSID']}
    Log To Console  ${SSID}
    Check Wifi Module Exists
    Check Wifi Interface UP
    Scan Available Networks
    Connect To Wifi    ${SSID}    ${WIFI_PASSWORD}
    Verify Wifi Connection    ${EXPECTED_SSID}
    Check IP Assigned
    Ping Internet