"""Trying to test papers"""

import os
import argparse
import dropbox
from dropbox.files import ListFolderResult, Metadata, FileMetadata, FolderMetadata, DeletedMetadata
from dropbox.paper import ListPaperDocsResponse, PaperDocExportResult, ImportFormat, PaperDocCreateUpdateResult, PaperDocUpdatePolicy
from dropbox.exceptions import ApiError

#8UHH0KQFM0CdRYtByDCCk

def main(args):
    print(args)
    dbx = dropbox.Dropbox(args.token)
    print(f"uploading paper {args.in_file_path}")
    
    with open(args.in_file_path, 'rb') as in_file:
        content = in_file.read()

    docs_list = []
    res: PaperDocCreateUpdateResult = dbx.paper_docs_update(
        f=content,
        doc_id=args.doc_id,
        import_format=ImportFormat.html,
        doc_update_policy=PaperDocUpdatePolicy.overwrite_all,
        revision=int(args.rev)
    )
    
    print(f"{res.title} updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Updates a paper')

    parser.add_argument(dest='in_file_path')
    parser.add_argument(dest='doc_id')
    parser.add_argument(dest='rev', default='1')
    parser.add_argument("--token", "-t", dest='token', default=os.environ.get("DROPBOX_TOKEN"))
    arg = parser.parse_args()
    main(arg)
#8UHH0KQFM0CdRYtByDCCk
# rev 53