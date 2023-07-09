from pathlib import Path
import glob
main_directory = Path(__file__).resolve().parent
file_pattern = str(main_directory / 'assets/data/controls.json')
files = glob.glob(file_pattern)
if files:
    controlsPath = files[0]
    print(controlsPath)