"""Trying to test papers"""

import os
import argparse
import dropbox
from dropbox.paper import ListPaperDocsResponse, PaperDocExportResult, ExportFormat


def main(args):
    """Main"""
    print(args)
    dbx = dropbox.Dropbox(args.token)

    print("Scanning papers")
    docs_list = []
    res: ListPaperDocsResponse = dbx.paper_docs_list()
    while True:

        for entry in res.doc_ids:
            print(entry)
            docs_list.append(entry)
        # read until no more
        if not res.has_more:
            break
        res = dbx.paper_docs_list_continue(res.cursor)

    # try download
    res: PaperDocExportResult = dbx.paper_docs_download_to_file(
        download_path="./paper3_old.html",
        doc_id=docs_list[2],
        export_format=ExportFormat.html,
    )
    print(f"{res.title} downlaoded, rev {res.revision}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic test of sample tutorial")
    parser.add_argument("--token", "-t", dest="token", default=os.environ.get("DROPBOX_TOKEN"))

    arg = parser.parse_args()
    main(arg)
