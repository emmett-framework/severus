# -*- coding: utf-8 -*-


def test_load(T, Tpre):
    assert not T._languages["en"]._strings
    assert set(T._languages["it"]._strings.keys()) == {
        "partly cloudy",
        "you received",
        "type {n} characters",
        "type {} characters",
    }
    assert set(T._languages["ru"]._strings.keys()) == {"partly cloudy"}
    assert set(T._languages["en"]._groups.keys()) == {"like"}
    assert set(T._languages["it"]._groups.keys()) == {"like"}
    assert not T._languages["ru"]._groups
    assert set(T._languages["en"]._groups["like"].keys()) == {1, 2, 5, 10, 50}
    assert set(T._languages["it"]._groups["like"].keys()) == {"_", 1, 2, 5, 10, 50}

    assert set(Tpre._languages["en"]._strings.keys()) == {"weather.cloudy.partly", "like.received"}
    assert set(Tpre._languages["it"]._strings.keys()) == {"weather.cloudy.partly", "like.received"}
    assert set(Tpre._languages["ru"]._strings.keys()) == {"weather.cloudy.partly"}
    assert set(Tpre._languages["en"]._groups.keys()) == {"like.numerical"}
    assert set(Tpre._languages["it"]._groups.keys()) == {"like.numerical"}
    assert not Tpre._languages["ru"]._groups
    assert set(Tpre._languages["en"]._groups["like.numerical"].keys()) == {"_", 1, 2, 5, 10, 50}
    assert set(Tpre._languages["it"]._groups["like.numerical"].keys()) == {"_", 1, 2, 5, 10, 50}
