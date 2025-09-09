from __future__ import annotations

import io
import mimetypes
import os
from typing import Iterable, List, Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/drive",
]


class DriveClient:
    """Minimal Google Drive client for listing, downloading, and uploading files.

    Auth uses a Google Cloud service account JSON key by default.
    Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the key path,
    or pass `credentials_path` explicitly.
    """

    def __init__(
        self,
        *,
        credentials_path: Optional[str] = None,
        scopes: Optional[Iterable[str]] = None,
    ) -> None:
        scopes = list(scopes or DEFAULT_SCOPES)
        credentials_path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "Missing service account key file. Set GOOGLE_APPLICATION_CREDENTIALS or pass credentials_path."
            )

        creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)
        self._drive = build("drive", "v3", credentials=creds)

    # -------------
    # File listing
    # -------------
    def list_folder(
        self,
        folder_id: str,
        *,
        mime_types: Optional[Iterable[str]] = None,
        page_size: int = 100,
    ) -> List[dict]:
        """List files in a folder by ID.

        Returns a list of dicts with keys: id, name, mimeType, size.
        """
        q = [f"'{folder_id}' in parents", "trashed=false"]
        if mime_types:
            mime_filter = " or ".join([f"mimeType='{mt}'" for mt in mime_types])
            q.append(f"({mime_filter})")

        query = " and ".join(q)
        fields = "nextPageToken, files(id, name, mimeType, size)"
        files: List[dict] = []
        page_token: Optional[str] = None

        while True:
            resp = (
                self._drive.files()
                .list(
                    q=query,
                    fields=fields,
                    pageSize=page_size,
                    pageToken=page_token,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                )
                .execute()
            )
            files.extend(resp.get("files", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        return files

    # ---------------
    # File download
    # ---------------
    def download_file(self, file_id: str, dest_path: str) -> str:
        """Download a file by ID to `dest_path`. Returns the written path."""
        request = self._drive.files().get_media(fileId=file_id)
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _status, done = downloader.next_chunk()

        # Ensure destination directory exists
        os.makedirs(os.path.dirname(os.path.abspath(dest_path)) or ".", exist_ok=True)
        with open(dest_path, "wb") as f:
            f.write(buf.getvalue())
        return dest_path

    # ---------------
    # File upload
    # ---------------
    def upload_file(
        self,
        folder_id: str,
        local_path: str,
        *,
        name: Optional[str] = None,
        mime_type: Optional[str] = None,
        resumable: bool = True,
    ) -> str:
        """Upload a local file into a Drive folder. Returns the new file ID."""
        if not os.path.isfile(local_path):
            raise FileNotFoundError(local_path)

        file_name = name or os.path.basename(local_path)
        mime = mime_type or mimetypes.guess_type(local_path)[0] or "application/octet-stream"

        media = MediaFileUpload(local_path, mimetype=mime, resumable=resumable)
        metadata = {"name": file_name, "parents": [folder_id]}
        created = (
            self._drive.files()
            .create(body=metadata, media_body=media, fields="id", supportsAllDrives=True)
            .execute()
        )
        return created["id"]

    # ---------------
    # Optional helpers
    # ---------------
    def get_file(self, file_id: str, *, fields: str = "id, name, mimeType, size, parents") -> dict:
        return (
            self._drive.files()
            .get(fileId=file_id, fields=fields, supportsAllDrives=True)
            .execute()
        )

