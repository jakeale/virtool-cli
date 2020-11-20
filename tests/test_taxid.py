import json
import os
import subprocess
import shutil

import pytest

TEST_PATH = "tests/files/src_taxid"
TEST_SRC = "src_taxid"


@pytest.fixture(scope="session", autouse=True)
def output(tmpdir_factory):
    return tmpdir_factory.getbasetemp()


@pytest.fixture(scope="session", autouse=True)
def run(output):
    dest = shutil.copytree(TEST_PATH, os.path.join(output, "src"))
    command = [
        "python", "virtool_cli/run.py",
        "taxid", "-src",
        dest, "-f"]
    subprocess.call(command)

    return dest


@pytest.mark.parametrize("path", ["h/hop_stunt_viroid", "r/reovirus_tf1_(not_a_plant_virus)",
                                  "t/tobacco_mosaic_virus", "t/totivirus_tf1_(not_a_plant_virus)"])
def test_taxid(path, run, output):
    path = os.path.join(run, path)

    with open(os.path.join(path, "otu.json"), 'r') as f:
        otu = json.load(f)

        if "not" in otu["name"]:
            assert otu["taxid"] is None
        else:
            assert otu["taxid"] is not None
