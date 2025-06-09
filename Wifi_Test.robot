*** Settings ***
Library           String
Library           Process

*** Test Cases ***
Check if Wifi Module is preset
    ${result}=  Run Process  networksetup   -listallhardwareports  stdout=PIPE
    ${output}=  Set Variable  ${result.stdout}
    Log To Console  ${output}
    Should Contain  ${output}  Wi-Fi

Check if Wifi Module is turned on
    ${result}=  Run Process  networksetup   -getairportpower  en0  stdout=PIPE
    ${output}=  Set Variable  ${result.stdout}
    Log To Console  ${output}
    Should Contain  ${output}  On

Check if Wifi Module is connected to a Wi-Fi Network
    ${result}=  Run Process  networksetup   -getairportnetwork  en0  stdout=PIPE
    ${output}=  Set Variable  ${result.stdout}
    Log To Console  ${output}
    Should Not Contain  ${output}  You are not associated with an AirPort network.

Verify Internet is working
    ${result}=  Run Process  ping  -c 5  www.google.com  stdout=PIPE
    ${output}=  Set Variable  ${result.stdout}
    Log To Console  ${output}
    Should Contain  ${output}  5 packets transmitted, 5 packets received