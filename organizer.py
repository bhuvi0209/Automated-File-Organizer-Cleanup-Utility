
import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# File extensions and their destination categories
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".rtf": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".csv": "Documents",

    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".svg": "Images",
    ".webp": "Images",

    # Videos
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".wmv": "Videos",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".aac": "Audio",
    ".flac": "Audio",

    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    # Code
    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".sql": "Code",
}

# Store logs beside this Python script
LOG_FILE = Path(__file__).resolve().parent / "organizer.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def get_unique_path(destination):
    """Generate a non-existing destination filename."""
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder_path):
    """Organize files directly inside the selected folder."""
    folder = Path(folder_path).expanduser().resolve()

    if not folder.exists():
        print(f"Error: Folder does not exist: {folder}")
        return

    if not folder.is_dir():
        print("Error: The provided path is not a directory.")
        return

    moved = 0
    skipped = 0
    failed = 0

    print(f"\nOrganizing folder: {folder}")
    print("-" * 55)

    try:
        # Snapshot the entries before creating destination folders
        with os.scandir(folder) as entries:
            files = [
                Path(entry.path)
                for entry in entries
                if entry.is_file(follow_symlinks=False)
            ]
    except PermissionError:
        print("Error: Permission denied while scanning this folder.")
        logging.exception("Permission denied while scanning %s", folder)
        return
    except OSError:
        print("Error: Could not scan the selected folder.")
        logging.exception("Failed to scan %s", folder)
        return

    for source in files:
        # Do not organize this script's own log file if it is in the target
        if source.resolve() == LOG_FILE.resolve():
            skipped += 1
            continue

        category = EXTENSION_MAP.get(
            source.suffix.lower(), "Others"
        )
        destination_folder = folder / category

        try:
            destination_folder.mkdir(exist_ok=True)
            destination = get_unique_path(
                destination_folder / source.name
            )

            shutil.move(str(source), str(destination))

            print(f"MOVED: {source.name} -> {category}/{destination.name}")
            logging.info("Moved %s to %s", source, destination)
            moved += 1

        except PermissionError:
            print(f"SKIPPED: Permission denied: {source.name}")
            logging.exception("Permission denied moving %s", source)
            failed += 1

        except OSError as error:
            print(f"ERROR: Could not move {source.name}: {error}")
            logging.exception("Failed to move %s", source)
            failed += 1

    print("\n" + "=" * 55)
    print("FILE ORGANIZATION SUMMARY")
    print("=" * 55)
    print(f"Files found:       {len(files)}")
    print(f"Files moved:       {moved}")
    print(f"Files skipped:     {skipped}")
    print(f"Files failed:      {failed}")
    print(f"Log file:          {LOG_FILE}")
    print("=" * 55)


def main():
    print("AUTOMATED FILE ORGANIZER")
    print("-" * 30)

    default_folder = Path.home() / "Downloads"
    entered_path = input(
        f"Enter folder path [{default_folder}]: "
    ).strip().strip('"')

    folder_path = entered_path or str(default_folder)

    if not Path(folder_path).expanduser().is_dir():
        print("Please enter a valid folder path.")
        return

    print(f"\nSelected folder: {Path(folder_path).expanduser()}")
    confirmation = input(
        "Files will be moved into category folders. Continue? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        organize_folder(folder_path)
    else:
        print("Operation cancelled. No files were moved.")


if __name__ == "__main__":
    main()
