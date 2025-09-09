Outbound Freight — Google Drive Setup

Quick scaffold to list, download, and upload CSV/XLSX files from Google Drive using a service account.

Prerequisites
- Python: 3.13+
- Google Cloud service account JSON key with Drive access
- The Drive folder or Shared Drive where files live (get the folder ID)

Setup
- Create or choose a Google Cloud project and enable the Drive API.
- Create a service account and download its JSON key.
- If using a Shared Drive: add the service account as a Manager of that drive.
- If using My Drive: share the specific folder(s) with the service account email.
- Set `GOOGLE_APPLICATION_CREDENTIALS` to the key path, e.g.:
  - macOS/Linux: `export GOOGLE_APPLICATION_CREDENTIALS=/abs/path/service-account.json`
  - Windows (PowerShell): `$Env:GOOGLE_APPLICATION_CREDENTIALS="C:\\path\\service-account.json"`

Install deps
- Using uv/pip:
  - `pip install -e .` (editable) or `pip install .`
  - This project depends on `google-api-python-client`.

CLI usage
- List a folder (filter to CSV/XLSX optional):
  - `python -m outbound_freight.cli list <FOLDER_ID>`
  - `python -m outbound_freight.cli list <FOLDER_ID> --only text/csv application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Download a file by ID:
  - `python -m outbound_freight.cli download <FILE_ID> ./data/invoice.xlsx`
- Upload a local file into a folder:
  - `python -m outbound_freight.cli upload <FOLDER_ID> ./exports/analysis.xlsx --mime application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

Notes
- The client uses `supportsAllDrives=True` and lists across Shared Drives.
- Work with file IDs, not names, to avoid collisions.
- For CSV/XLSX, uploads are binary files; no conversion is needed.
- If you also need Google Sheets editing later, we can add the Sheets API via the same auth.
