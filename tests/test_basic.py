from flow_gate.bump import group_updates

def test_group_updates_major():
    outdated = [{"name": "fake", "version": "1.0.0", "latest_version": "2.0.0"}]
    grouped = group_updates(outdated)
    assert len(grouped["major"]) == 1
    assert len(grouped["minor"]) == 0
    assert len(grouped["patch"]) == 0

def test_group_updates_minor():
    outdated = [{"name": "fake", "version": "1.0.0", "latest_version": "1.1.0"}]
    grouped = group_updates(outdated)
    assert len(grouped["major"]) == 0
    assert len(grouped["minor"]) == 1
    assert len(grouped["patch"]) == 0

def test_group_updates_patch():
    outdated = [{"name": "fake", "version": "1.0.0", "latest_version": "1.0.1"}]
    grouped = group_updates(outdated)
    assert len(grouped["major"]) == 0
    assert len(grouped["minor"]) == 0
    assert len(grouped["patch"]) == 1
