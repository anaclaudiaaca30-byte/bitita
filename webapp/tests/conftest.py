import os
import tempfile
from pathlib import Path

# Configura um banco temporário antes da importação da aplicação.
TEST_DIRECTORY = Path(tempfile.mkdtemp(prefix="bitita-tests-"))
TEST_DATABASE = TEST_DIRECTORY / "testes.db"

os.environ["DATABASE_URL"] = (
    "sqlite:///" + TEST_DATABASE.as_posix()
)