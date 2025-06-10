import os
import sys
import schedule
import time
from datetime import datetime
from robot import run

def run_robot_tests(test_targets):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = os.path.join("results", timestamp)
    os.makedirs(results_dir, exist_ok=True)

    print(f"[INFO] Running Robot Framework tests on: {test_targets}")
    
    run(*test_targets,
        outputdir=results_dir,
        report="report.html",
        log="log.html",
        output="output.xml")

    print(f"[INFO] Test completed. Results saved in {results_dir}\n")

def run_periodically(test_targets, interval_minutes=60):
    print(f"[INFO] Scheduling tests: {test_targets} every {interval_minutes} minute(s).")
    schedule.every(interval_minutes).minutes.do(run_robot_tests, test_targets=test_targets)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
            print("\n [INFO] Scheduler stopped manually by user.")

if __name__ == "__main__":
    # Usage: python scheduler.py <test_target1> <test_target2> ... [interval_minutes]
    args = sys.argv[1:]

    # If last argument is digit, treat as interval (minutes)
    if args and args[-1].isdigit():
        interval = int(args.pop())
    else:
        interval = 60  # default 60 minutes

    # If no targets given, default to 'tests' folder
    test_targets = args if args else ['tests']

    run_periodically(test_targets, interval)
