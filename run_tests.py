import os
import sys
from datetime import datetime
from robot import run

# Get all provided arguments as test targets (list of files or folders)
# If no arguments are provided, default to 'tests/' folder
test_targets = sys.argv[1:] if len(sys.argv) > 1 else ["tests/"]

# Generate unique output directory based on date-time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_dir = os.path.join("results", current_time)
os.makedirs(output_dir, exist_ok=True)

# Run Robot Framework with multiple test files/folders
run(*test_targets,
    outputdir=output_dir,
    report="report.html",
    log="log.html",
    output="output.xml")

print(f"Test results are stored in: {output_dir}")
