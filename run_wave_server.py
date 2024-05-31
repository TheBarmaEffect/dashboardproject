import subprocess
import os

# Change directory to where app.py is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run the H2O Wave server
subprocess.run(["wave", "run", "--no-reload", "app.py"])
