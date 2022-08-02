from google.cloud import storage

import os
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_FILE = FILE.parents[0].parents[0]  # backend root directory

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(ROOT_FILE,"GCP_KEY.json")