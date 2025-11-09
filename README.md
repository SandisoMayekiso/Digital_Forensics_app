File Metadata Extractor

A simple GUI tool built with Python and tkinter that extracts basic file metadata (name, type, size, creation/modification/access times) for one or more selected files and allows exporting the results to CSV. Designed for quick local analysis and lightweight reporting.

Features

Select one or more files via a native file dialog.

Display file metadata in a readable format in the app window.

Export collected metadata to a CSV file.

Clear results and re-run on different files.

Minimal dependencies — works with standard Python installation.

Error logging to errors.log for troubleshooting.

Screenshot

<img width="861" height="657" alt="image" src="https://github.com/user-attachments/assets/67b2b30d-2514-4ba0-8811-ff5e2bf4754d" />


Requirements

Python 3.8+ (should work on 3.7, but 3.8+ recommended)

tkinter (usually included with standard Python distributions)

Standard library modules used: os, csv, pprint, logging, datetime, pathlib, tkinter

On Debian/Ubuntu, if tkinter is missing:

sudo apt update
sudo apt install python3-tk


On macOS, use the Python from python.org or Homebrew (brew install python) which generally includes tkinter.

Installation

Clone the repository (or copy the script file) to your local machine:

git clone https://github.com/youruser/metadata-extractor.git
cd metadata-extractor


Ensure Python 3 is installed and tkinter is available.

(Optional) Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate


No extra pip packages are required.

Usage

Run the app from the command line:

python3 metadata_extractor.py
