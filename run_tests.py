import os
import sys
from datetime import datetime
from robot import run
from notify import notify_robot_failures

def run_robot_tests(test_targets):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = os.path.join("results", timestamp)
    os.makedirs(results_dir, exist_ok=True)

    print(f"[INFO] Running Robot Framework tests on: {test_targets} by triggering manually")
    
    run(*test_targets,
        outputdir=results_dir,
        report="report.html",
        log="log.html",
        output="output.xml")

    print(f"[INFO] Test completed. Results saved in {results_dir}\n")

    output_xml_path = os.path.join(results_dir, "output.xml")
    notify_robot_failures(output_xml_path, "Manual")

if __name__ == "__main__":
    test_targets = sys.argv[1:] if len(sys.argv) > 1 else ["tests/"]
    run_robot_tests(test_targets)
