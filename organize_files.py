"""Simple test app from the tutorial"""

import os
import argparse
import dropbox
from dropbox.files import (
    ListFolderResult,
    Metadata,
    FileMetadata,
    FolderMetadata,
    DeletedMetadata,
)
from dropbox.exceptions import ApiError


def main(args):
    print(args)
    dbx = dropbox.Dropbox(args.token)

    def path_exists(path):
        try:
            dbx.files_get_metadata(path)
            return True
        except ApiError as ae:
            if ae.error.get_path().is_not_found():
                return False
            raise

    print("Scanning files")
    path = "/j.badillo@numat-tech.com’s files/Home/sample_expenses"
    file_set = []
    res: ListFolderResult = dbx.files_list_folder(path=path)
    while True:
        entry: Metadata
        for entry in res.entries:
            if isinstance(entry, FolderMetadata):
                print(f"{entry.id} folder {entry.name}")
            elif isinstance(entry, FileMetadata):
                print(f"{entry.id} file {entry.name}")
                file_set.append(entry)
            elif isinstance(entry, DeletedMetadata):
                print(f"{entry.id} deleted {entry.name}")
        # read until no more
        if not res.has_more:
            break
        res = dbx.files_list_folder_continue(res.cursor)
    print("creating folder")
    new_path = f"{path}/pdfs"
    if not path_exists(new_path):
        dbx.files_create_folder(new_path)
        print("created")
    else:
        print("existed already")
    print("moving pdfs")

    f: FileMetadata
    for f in file_set:
        if f.name.endswith(".pdf"):
            print(f"moving {f.path_display}")
            r = dbx.files_move_v2(f.path_lower, f"{new_path}/{f.name}")
            print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic test of sample tutorial")
    parser.add_argument(
        "--token", "-t", dest="token", default=os.environ.get("DROPBOX_TOKEN")
    )

    arg = parser.parse_args()
    main(arg)
