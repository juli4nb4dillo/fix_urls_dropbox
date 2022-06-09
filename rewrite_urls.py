"""Trying to test papers"""

import os
import argparse
from typing import List
from xmlrpc.client import Boolean
import dropbox
from dropbox.paper import (
    ImportFormat,
    PaperDocCreateUpdateResult,
    PaperDocUpdatePolicy,
    ExportFormat,
    PaperDocExportResult,
)

# 8UHH0KQFM0CdRYtByDCCk
OLD_URL = "internal.numat-tech.com/django-tracking"
NEW_URL = "erp.numat.com"


def rewrite_urls(doc_id: str, doc: PaperDocExportResult, format: str):
    """Rewrites all old urls

    Arguments:
        doc -- A description of the document
    """
    path = f"./data/paper{doc_id}.{'html' if format == 'html' else 'md'}"
    with open(path, "r") as file:
        content = file.read()
    content = content.replace(OLD_URL, NEW_URL)
    with open(path, "w") as file:
        file.write(content)


def process_docs(
    doc_ids: List[str],
    download: Boolean,
    rewrite: Boolean,
    upload: Boolean,
    format: str,
):
    """_summary_

    Arguments:
        doc_ids -- _description_
    """
    e_format = ExportFormat.html if format == "html" else ExportFormat.markdown
    i_format = ImportFormat.html if format == "html" else ImportFormat.markdown

    print("download papers")
    docs = {}
    for doc_id in doc_ids:
        # try download
        if download:
            path = f"./data/paper{doc_id}.{'html' if format == 'html' else 'md'}"
        else:
            path = "./data/temp.txt"
        doc: PaperDocExportResult = dbx.paper_docs_download_to_file(
            download_path=path,
            doc_id=doc_id,
            export_format=e_format,
        )
        docs[doc_id] = doc
        print(f"{doc.title} downloaded, rev {doc.revision}")
    if rewrite:
        # processing files locally
        print("Rewrite urls")
        for doc_id, doc in docs.items():
            rewrite_urls(doc_id, doc, format)
    if upload:
        # upload papers
        doc: PaperDocExportResult
        for doc_id, doc in docs.items():
            print(f"uploading paper {doc.title}")
            path = f"./data/paper{doc_id}.{'html' if format == 'html' else 'md'}"
            with open(path, "rb") as in_file:
                content = in_file.read()
            res: PaperDocCreateUpdateResult = dbx.paper_docs_update(
                f=content,
                doc_id=doc_id,
                import_format=i_format,
                doc_update_policy=PaperDocUpdatePolicy.overwrite_all,
                revision=int(doc.revision),
            )
            print(f"{res.title} updated")


def main(args):
    """Main"""
    print(args)
    global dbx
    dbx = dropbox.Dropbox(args.token)
    process_docs(args.doc_ids, args.download, args.rewrite, args.upload, args.format)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rewrites url on a list of papers (ids)")

    parser.add_argument(dest="doc_ids", nargs="+")
    parser.add_argument("--token", "-t", dest="token", default=os.environ.get("DROPBOX_TOKEN"))
    parser.add_argument("--download", "-d", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--rewrite", "-r", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--upload", "-u", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--format", "-f", default="html", choices=("html", "markdown"))
    arg = parser.parse_args()
    main(arg)
# 8UHH0KQFM0CdRYtByDCCk
# 7jlzfTDUqYZONXBRtAAnH
# rev 53
