import pytest

from core.libs.assertions import assert_auth
from core.libs.exceptions import FyleError
from core.libs.assertions import (
    base_assert,
    assert_auth,
    assert_true,
    assert_valid,
    assert_found,
)


def test_base_assert():
    with pytest.raises(FyleError) as exc_info:
        base_assert(400, "BAD_REQUEST")
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "BAD_REQUEST"


def test_assert_auth():
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False, "UNAUTHORIZED")
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "UNAUTHORIZED"

    # Should not raise an exception when condition is True
    assert_auth(True)


def test_assert_true():
    with pytest.raises(FyleError) as exc_info:
        assert_true(False, "FORBIDDEN")
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "FORBIDDEN"

    # Should not raise an exception when condition is True
    assert_true(True)


def test_assert_valid():
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False, "BAD_REQUEST")
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "BAD_REQUEST"

    # Should not raise an exception when condition is True
    assert_valid(True)


def test_assert_found():
    with pytest.raises(FyleError) as exc_info:
        assert_found(None, "NOT_FOUND")
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "NOT_FOUND"

    # Should not raise an exception when object is found
    assert_found(object())
