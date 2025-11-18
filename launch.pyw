# launch.pyw — Silent launcher (no terminal window)
import subprocess
import sys
import os

if __name__ == "__main__":
    # Run main.py silently
    subprocess.Popen([sys.executable, 'main.py'], 
                     stdout=subprocess.DEVNULL, 
                     stderr=subprocess.DEVNULL,
                     shell=False)