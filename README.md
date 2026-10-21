\# Automated File Organizer \& Cleanup Utility



A Python 3 utility that automatically organizes files into category-based folders using file extensions.



\## Features



\- Automatically sorts files by extension.

\- Creates category folders when needed.

\- Supports documents, images, videos, audio, archives, code, and other files.

\- Avoids overwriting files with duplicate names.

\- Handles permission errors and filesystem exceptions.

\- Logs file operations to `organizer.log`.

\- Displays a formatted execution summary.

\- Requests confirmation before moving files.



\## Technologies Used



\- Python 3

\- os

\- shutil

\- pathlib

\- logging



\## How to Run



1\. Install Python 3.

2\. Open a terminal in the project directory.

3\. Run:



&#x20;  `python organizer.py`



4\. Enter the folder path or press Enter to use your Downloads folder.

5\. Confirm the operation when prompted.



\## Example Folder Structure



Before:



\- `Downloads/report.pdf`

\- `Downloads/photo.jpg`

\- `Downloads/archive.zip`

\- `Downloads/script.py`



After:



\- `Downloads/Documents/report.pdf`

\- `Downloads/Images/photo.jpg`

\- `Downloads/Archives/archive.zip`

\- `Downloads/Code/script.py`



\## Safety



Test with a sample folder before using the utility on important files. The program moves files and does not delete them. It does not recursively organize existing subfolders.



\## License



For educational use.

