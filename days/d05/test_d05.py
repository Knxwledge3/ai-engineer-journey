import pytest

import d05


class Resp:
    def __init__(self, code, data=None):
        self.status_code, self._data = code, data

    def json(self):
        return self._data


def test_with_retries_backoff():
    calls, sleeps = [], []

    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise d05.TransientError("503")
        return "ok"

    assert d05.with_retries(fn, attempts=4, base_delay=0.5, sleep=sleeps.append) == "ok"
    assert len(calls) == 3
    assert sleeps == [0.5, 1.0]


def test_with_retries_gives_up_without_last_sleep():
    calls, sleeps = [], []

    def fn():
        calls.append(1)
        raise d05.TransientError("всегда")

    with pytest.raises(d05.TransientError):
        d05.with_retries(fn, attempts=3, base_delay=1, sleep=sleeps.append)
    assert len(calls) == 3
    assert sleeps == [1, 2]


def test_with_retries_does_not_retry_other_errors():
    calls = []

    def fn():
        calls.append(1)
        raise ValueError("ошибка в запросе, повтор не поможет")

    with pytest.raises(ValueError):
        d05.with_retries(fn, attempts=5, sleep=lambda s: None)
    assert len(calls) == 1


def test_fetch_json_ok_and_timeout_passed():
    seen = {}

    def get(url, timeout=None):
        seen.update(url=url, timeout=timeout)
        return Resp(200, {"temp": -5})

    assert d05.fetch_json("http://api/weather", get, timeout=7) == {"temp": -5}
    assert seen == {"url": "http://api/weather", "timeout": 7}


@pytest.mark.parametrize("code", [429, 500, 503])
def test_fetch_json_transient(code):
    with pytest.raises(d05.TransientError):
        d05.fetch_json("http://x", lambda url, timeout=None: Resp(code))


@pytest.mark.parametrize("code", [400, 401, 404])
def test_fetch_json_client_error(code):
    with pytest.raises(ValueError) as e:
        d05.fetch_json("http://x", lambda url, timeout=None: Resp(code))
    assert str(code) in str(e.value)
    assert not isinstance(e.value, d05.TransientError)
