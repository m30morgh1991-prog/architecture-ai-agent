from runtime.change_request_contract import ChangeRequest, build_change_request


def _valid(**overrides):
    data = {
        "request_id": "cr-74",
        "source_sha256": "a" * 64,
        "model_id": "pm-74",
        "change_type": "FURNITURE_LAYOUT_CHANGE",
        "instruction": "Move the sofa beside the north wall.",
        "target_ids": ("F01",),
        "evidence_ids": ("ev-01",),
    }
    data.update(overrides)
    return ChangeRequest(**data)


def test_change_request_validates_and_traces():
    request = _valid()
    request.validate()
    assert request.trace()["source_sha256"] == "a" * 64
    assert request.is_targeted


def test_change_request_rejects_invalid_source():
    try:
        _valid(source_sha256="bad").validate()
    except ValueError as exc:
        assert str(exc) == "CHANGE_REQUEST_SOURCE_INVALID"
    else:
        raise AssertionError("expected rejection")


def test_change_request_rejects_unknown_change_type():
    try:
        _valid(change_type="UNSUPPORTED").validate()
    except ValueError as exc:
        assert str(exc) == "CHANGE_REQUEST_TYPE_INVALID"
    else:
        raise AssertionError("expected rejection")


def test_change_request_rejects_empty_instruction():
    try:
        _valid(instruction="   ").validate()
    except ValueError as exc:
        assert str(exc) == "CHANGE_REQUEST_INSTRUCTION_MISSING"
    else:
        raise AssertionError("expected rejection")


def test_change_request_rejects_duplicate_targets():
    try:
        _valid(target_ids=("F01", "F01")).validate()
    except ValueError as exc:
        assert str(exc) == "CHANGE_REQUEST_TARGET_DUPLICATE"
    else:
        raise AssertionError("expected rejection")


def test_builder_returns_valid_request():
    request = build_change_request(
        request_id="cr-builder",
        source_sha256="b" * 64,
        model_id="pm-builder",
        change_type="FURNITURE",
        instruction="Add a dining table.",
    )
    assert request.request_id == "cr-builder"
    assert not request.is_targeted
