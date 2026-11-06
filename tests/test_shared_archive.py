import json

import pytest

from soam.platform.runner import Budget
from soam.shared.archive import InputStore, identity, verify_contract
from soam.shared.data import SharedTask
from soam.shared.runner import Config


def test_shared_inputs_restore_and_charge_unique_bytes(tmp_path):
    verify_contract()
    budget = Budget(Config(archive_revision="a1"))
    store = InputStore(tmp_path / "objects", budget)
    _, episodes = SharedTask().training_batch(9001, 100, "transition", fixture=True, batch_size=2)
    key = store.write(tmp_path / "fit-a", episodes)
    before = budget.measurements()["artifact_bytes"]
    assert store.write(tmp_path / "fit-b", episodes) == key
    assert budget.measurements()["artifact_bytes"] - before < 1024
    assert len(list(store.root.iterdir())) == 1
    assert identity(store.restore(tmp_path / "fit-b")) == identity(episodes)
    ref = json.loads((tmp_path / "fit-b/input-ref.json").read_text())
    ref["object"] = "../escape"
    (tmp_path / "fit-b/input-ref.json").write_text(json.dumps(ref))
    with pytest.raises(ValueError, match="digest"):
        store.restore(tmp_path / "fit-b")
    object_file = store.root / key / "streams.json"
    object_file.write_text("[]")
    with pytest.raises(ValueError, match="integrity"):
        store.restore(tmp_path / "fit-a")
    with pytest.raises(ValueError, match="integrity"):
        store.write(tmp_path / "fit-c", episodes)


def test_incomplete_object_and_symlink_rejected(tmp_path):
    store = InputStore(tmp_path / "objects", Budget(Config()))
    _, episodes = SharedTask().training_batch(9001, 0, "recall", fixture=True, batch_size=2)
    key = identity(episodes)
    path = store.root / key
    path.mkdir(parents=True)
    with pytest.raises(ValueError, match="incomplete"):
        store.write(tmp_path / "ref", episodes)
    path.rmdir()
    path.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        store.write(tmp_path / "ref", episodes)
