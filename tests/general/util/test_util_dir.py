import os
from pathlib import Path

from cookietemple.util.dir_util import delete_dir_tree


def test_delete_dir_tree(tmp_path):
    """
    Delete an arbitrarily deep nested directory so its completely removed.
    """
    os.makedirs(f"{tmp_path}/testdir/my/deep/nested/directory")
    delete_dir_tree(Path(f"{tmp_path}/testdir"))
    assert len(list(tmp_path.iterdir())) == 0
