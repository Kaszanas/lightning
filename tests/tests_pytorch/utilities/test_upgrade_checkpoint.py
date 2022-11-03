# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from pytorch_lightning.utilities.migration import migrate_checkpoint
from pytorch_lightning.utilities.migration.utils import _get_version, _set_legacy_version, _set_version


@pytest.mark.parametrize(
    "old_checkpoint, new_checkpoint",
    [
        (
            {"epoch": 1, "global_step": 23, "checkpoint_callback_best": 0.34},
            {"epoch": 1, "global_step": 23, "callbacks": {ModelCheckpoint: {"best_model_score": 0.34}}},
        ),
        (
            {"epoch": 1, "global_step": 23, "checkpoint_callback_best_model_score": 0.99},
            {"epoch": 1, "global_step": 23, "callbacks": {ModelCheckpoint: {"best_model_score": 0.99}}},
        ),
        (
            {"epoch": 1, "global_step": 23, "checkpoint_callback_best_model_path": "path"},
            {"epoch": 1, "global_step": 23, "callbacks": {ModelCheckpoint: {"best_model_path": "path"}}},
        ),
        (
            {"epoch": 1, "global_step": 23, "early_stop_callback_wait": 2, "early_stop_callback_patience": 4},
            {"epoch": 1, "global_step": 23, "callbacks": {EarlyStopping: {"wait_count": 2, "patience": 4}}},
        ),
    ],
)
def test_upgrade_checkpoint(tmpdir, old_checkpoint, new_checkpoint):
    _set_version(old_checkpoint, "0.9.0")
    _set_legacy_version(new_checkpoint, "0.9.0")
    _set_version(new_checkpoint, pl.__version__)
    updated_checkpoint, _ = migrate_checkpoint(old_checkpoint)
    assert updated_checkpoint == old_checkpoint == new_checkpoint
    assert _get_version(updated_checkpoint) == pl.__version__
