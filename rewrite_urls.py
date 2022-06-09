"""Trying to test papers"""

import os
import argparse
import dropbox
from dropbox.paper import (
    ImportFormat,
    PaperDocCreateUpdateResult,
    PaperDocUpdatePolicy,
    ListPaperDocsResponse,
    ExportFormat,
    PaperDocExportResult
)

# 8UHH0KQFM0CdRYtByDCCk

def rewrite_urls(doc: PaperDocExportResult):
    # TODO write
    path = f"./data/paper{doc.doc_id}.html"
    pass

def main(args):
    print(args)
    dbx = dropbox.Dropbox(args.token)
    docs = []

    print("download papers")
    for doc_id in args.doc_ids:
        # try download
        path = f"./data/paper{doc_id}.html"
        doc: PaperDocExportResult = dbx.paper_docs_download_to_file(
            download_path=path,
            doc_id=args.doc_id,
            export_format=ExportFormat.html,
        )
        docs.append(doc)
        print(f"{doc.title} downloaded, rev {doc.revision}")

    # TODO rewrite urs
    print("Rewrite urls")
    for doc in docs:
        rewrite_urls(doc)

    # upload papers
    doc: PaperDocExportResult
    for doc in docs:
        print(f"uploading paper {doc.title}")
        path = f"./data/paper{doc.doc_id}.html"
        with open(path, "rb") as in_file:
            content = in_file.read()
        res: PaperDocCreateUpdateResult = dbx.paper_docs_update(
            f=content,
            doc_id=doc.doc_id,
            import_format=ImportFormat.html,
            doc_update_policy=PaperDocUpdatePolicy.overwrite_all,
            revision=int(doc.revision),
        )
        print(f"{res.title} updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rewrites url on a single paper")

    parser.add_argument(dest="doc_ids", nargs="+", required=True)
    parser.add_argument(
        "--token", "-t", dest="token", default=os.environ.get("DROPBOX_TOKEN")
    )
    arg = parser.parse_args()
    main(arg)
# 8UHH0KQFM0CdRYtByDCCk
# rev 53
