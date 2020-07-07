from pathlib import Path
from cookietemple.sync.sync_utils.sync_util import has_template_version_changed


def snyc_template(project_dir: Path):
    print(has_template_version_changed(project_dir))

