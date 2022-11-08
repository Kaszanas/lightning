import os

import pytest
from tests_app import _PROJECT_ROOT

from lightning_app.testing.testing import application_testing, LightningTestApp


class LightningTestMultiNodeApp(LightningTestApp):
    def on_before_run_once(self):
        res = super().on_before_run_once()
        if self.works and all(w.has_stopped for w in self.works):
            assert len([w for w in self.works]) == 2
            return True
        return res


@pytest.mark.skipif(True, reason="flaky")
def test_multi_node_example():
    cwd = os.getcwd()
    new_cwd = os.path.join(_PROJECT_ROOT, "examples/app_multi_node")
    os.chdir(new_cwd)
    command_line = [
        "app.py",
        "--blocking",
        "False",
        "--open-ui",
        "False",
    ]
    result = application_testing(LightningTestMultiNodeApp, command_line)
    assert result.exit_code == 0
    os.chdir(cwd)


class LightningTestMultiNodeWorksApp(LightningTestApp):
    def on_before_run_once(self):
        res = super().on_before_run_once()
        if self.works and all(w.has_stopped for w in self.works):
            assert len([w for w in self.works]) == 2
            return True
        return res


@pytest.mark.parametrize(
    "app_name",
    [
        "train_pytorch.py",
        "train_any.py",
        # "app_lite_work.py",
        "train_pytorch_spawn.py",
        # "app_pl_work.py": TODO Add once https://github.com/Lightning-AI/lightning/issues/15556 is resolved.
    ],
)
def test_multi_node_examples(app_name):
    cwd = os.getcwd()
    new_cwd = os.path.join(_PROJECT_ROOT, "examples/app_multi_node")
    os.chdir(new_cwd)
    command_line = [
        app_name,
        "--blocking",
        "False",
        "--open-ui",
        "False",
    ]
    result = application_testing(LightningTestMultiNodeWorksApp, command_line)
    assert result.exit_code == 0
    os.chdir(cwd)
