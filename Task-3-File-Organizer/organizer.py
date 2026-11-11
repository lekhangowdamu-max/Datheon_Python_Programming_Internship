import os
import shutil
from pathlib import Path

# Extension-to-category mapping
FILE_CATEGORIES = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".svg": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",

    ".py": "Code",
    ".java": "Code",
    ".cpp": "Code",
    ".c": "Code",
    ".html": "Code",
    ".css": "Code",
    ".js": "Code",
}


def get_unique_path(destination):
    """Generate a unique filename to avoid collisions."""

    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):

    source_folder = Path(folder_path)

    if not source_folder.exists() or not source_folder.is_dir():
        print("Error: Invalid directory!")
        return

    total_moved = 0
    total_skipped = 0
    total_failed = 0

    print("\n========== AUTOMATED FILE ORGANIZER ==========")

    try:
        with os.scandir(source_folder) as entries:

            for entry in entries:

                # Process files only, not directories or symlinks
                if not entry.is_file(follow_symlinks=False):
                    continue

                source_file = Path(entry.path)

                # Identify category from extension
                extension = source_file.suffix.lower()

                category = FILE_CATEGORIES.get(extension)

                # Handle unknown file extensions
                if category is None:
                    print(
                        f"Skipped: {source_file.name} "
                        "(Unknown file type)"
                    )
                    total_skipped += 1
                    continue

                destination_folder = source_folder / category

                try:
                    # Create category folder dynamically
                    destination_folder.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    destination_file = (
                        destination_folder / source_file.name
                    )

                    # Avoid overwriting existing files
                    destination_file = get_unique_path(
                        destination_file
                    )

                    # Move the file
                    shutil.move(
                        str(source_file),
                        str(destination_file)
                    )

                    print(
                        f"[SUCCESS] {source_file.name} "
                        "-> " + category
                    )

                    total_moved += 1

                except PermissionError:
                    print(
                        f"[PERMISSION ERROR] {source_file.name}"
                    )
                    total_failed += 1

                except FileExistsError:
                    print(
                        f"[FILE EXISTS] {source_file.name}"
                    )
                    total_failed += 1

                except (OSError, shutil.Error) as error:
                    print(
                        f"[ERROR] {source_file.name}: {error}"
                    )
                    total_failed += 1

    except PermissionError:
        print("Error: Permission denied accessing directory.")
        return

    except OSError as error:
        print("Directory error:", error)
        return

    # Final execution report
    print("\n========== EXECUTION SUMMARY ==========")
    print("Total files relocated :", total_moved)
    print("Total files skipped   :", total_skipped)
    print("Total files failed    :", total_failed)
    print("=======================================")

    print("\nFile organization completed!")


# Main program
if __name__ == "__main__":

    print("AUTOMATED FILE ORGANIZER")
    print("------------------------")

    folder = input(
        "Enter directory path to organize: "
    ).strip().strip('"')

    organize_files(folder)