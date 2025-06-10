*** Settings ***
Resource    system_monitor_keywords.robot

*** Variables ***
${CPU_THRESHOLD}        85
${RAM_THRESHOLD}        90
${TEMP_THRESHOLD}       75
${DISK_THRESHOLD}       90
${SWAP_THRESHOLD}       60
${PING_TARGET}          8.8.8.8

*** Test Cases ***
Check CPU RAM Temp
    ${cpu}=    Get CPU Usage
    Should Be True    ${cpu} < ${CPU_THRESHOLD}    CPU Usage is too high: ${cpu}%
    ${ram}=    Get RAM Usage
    Should Be True    ${ram} < ${RAM_THRESHOLD}    RAM Usage is too high: ${ram}%
    ${temp}=   Get Temperature
    Should Be True    ${temp} < ${TEMP_THRESHOLD}    Temperature too high: ${temp}C

Check Disk Usage
    ${disk}=   Get Disk Usage
    Should Be True    ${disk} < ${DISK_THRESHOLD}    Disk Usage too high: ${disk}%

Check Network Status
    ${ping_result}=    Run Ping Test    ${PING_TARGET}
    Should Contain    ${ping_result}    0% packet loss    Network issue detected: ${ping_result}

Check Undervoltage
    ${throttle}=    Get Throttled Status
    Should Contain    ${throttle}    throttled=0x0    Undervoltage or power issues detected: ${throttle}

Check Swap Usage
    ${swap}=    Get Swap Usage
    Should Be True    ${swap} < ${SWAP_THRESHOLD}    Swap usage too high: ${swap}%

Check Stuck or Malicious Processes
    ${suspicious}=    Find Suspicious Processes
    Should Be Equal As Integers    ${suspicious}    0    Suspicious processes detected: ${suspicious}

Check Uptime
    ${uptime}=    Get Uptime Hours
    Should Be True    ${uptime} > 1    Uptime suspiciously low: ${uptime} hours
