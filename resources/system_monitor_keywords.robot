*** Settings ***
Library    OperatingSystem
Library    Process
Library    Collections
Library    psutil
Library    BuiltIn

*** Keywords ***
Get CPU Usage
    ${cpu}=    Evaluate    psutil.cpu_percent(interval=1)    modules=psutil
    RETURN    ${cpu}

Get RAM Usage
    ${mem}=    Evaluate    psutil.virtual_memory().percent    modules=psutil
    RETURN    ${mem}

Get Temperature
    ${temp_out}=    Run Process    vcgencmd measure_temp    shell=True
    ${temp}=    Evaluate    float('${temp_out.stdout}'.split('=')[1].split("'")[0])
    RETURN    ${temp}

Get Disk Usage
    ${disk}=    Evaluate    psutil.disk_usage('/').percent    modules=psutil
    RETURN    ${disk}

Run Ping Test
    [Arguments]    ${target}
    ${result}=    Run Process    ping -c 4 ${target}    shell=True
    RETURN    ${result.stdout}

Get Throttled Status
    ${throttle}=    Run Process    vcgencmd get_throttled    shell=True
    RETURN    ${throttle.stdout}

Get Swap Usage
    ${swap}=    Evaluate    psutil.swap_memory().percent    modules=psutil
    RETURN    ${swap}

Find Suspicious Processes
    ${count}=    Evaluate    len([p for p in psutil.process_iter() if p.cpu_percent(interval=0.1) > 90])    modules=psutil
    RETURN    ${count}

Get Uptime Hours
    ${uptime}=    Evaluate    psutil.boot_time()    modules=psutil
    ${now}=    Evaluate    __import__('time').time()
    ${uptime_hours}=    Evaluate    (${now} - ${uptime}) / 3600
    RETURN    ${uptime_hours}
