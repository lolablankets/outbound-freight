import argparse
import os
import sys
from typing import Optional

from .drive_client import DriveClient


def _ensure_creds(credentials_path: Optional[str]) -> str:
    path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not path:
        raise SystemExit(
            "Missing GOOGLE_APPLICATION_CREDENTIALS. Set it or pass --credentials."
        )
    return path


def cmd_list(args: argparse.Namespace) -> None:
    creds_path = _ensure_creds(args.credentials)
    client = DriveClient(credentials_path=creds_path)
    mimes = None
    if args.only:
        mimes = args.only
    files = client.list_folder(args.folder_id, mime_types=mimes)
    for f in files:
        size = f.get("size", "-")
        print(f"{f['id']}	{f['mimeType']}	{size}	{f['name']}")


def cmd_download(args: argparse.Namespace) -> None:
    creds_path = _ensure_creds(args.credentials)
    client = DriveClient(credentials_path=creds_path)
    out = client.download_file(args.file_id, args.dest)
    print(out)


def cmd_upload(args: argparse.Namespace) -> None:
    creds_path = _ensure_creds(args.credentials)
    client = DriveClient(credentials_path=creds_path)
    new_id = client.upload_file(args.folder_id, args.path, name=args.name, mime_type=args.mime)
    print(new_id)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="outbound-freight")
    p.add_argument(
        "--credentials",
        help="Path to service account JSON (defaults to $GOOGLE_APPLICATION_CREDENTIALS)",
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List files in a Drive folder")
    p_list.add_argument("folder_id", help="Folder ID to list")
    p_list.add_argument(
        "--only",
        nargs="+",
        help="Optional list of MIME types to filter (e.g. text/csv application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)",
    )
    p_list.set_defaults(func=cmd_list)

    p_dl = sub.add_parser("download", help="Download a file by ID")
    p_dl.add_argument("file_id", help="File ID to download")
    p_dl.add_argument("dest", help="Destination path for the downloaded file")
    p_dl.set_defaults(func=cmd_download)

    p_up = sub.add_parser("upload", help="Upload a local file to a Drive folder")
    p_up.add_argument("folder_id", help="Destination Folder ID")
    p_up.add_argument("path", help="Path to the local file to upload")
    p_up.add_argument("--name", help="Optional filename to use in Drive")
    p_up.add_argument("--mime", help="Optional MIME type override (auto-guessed if omitted)")
    p_up.set_defaults(func=cmd_upload)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())

