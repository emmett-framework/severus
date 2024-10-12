# -*- coding: utf-8 -*-

from severus.ctx import context, language


def test_translate(T, Tpre):
    with context(T):
        assert T("test") == "test"
        assert T("test", lang="it") == "test"
        assert T("test", lang="ru") == "test"
        assert T("partly cloudy") == "partly cloudy"
        assert T("partly cloudy", lang="it") == "nuvolosità variabile"
        assert T("partly cloudy", lang="ru") == "переменная облачность"
        assert T("like") == "like"
        assert T("like", lang="it") == "mi piace"

    with context(Tpre):
        assert Tpre("test") == "test"
        assert Tpre("test", lang="it") == "test"
        assert Tpre("test", lang="ru") == "test"
        assert Tpre("weather.cloudy.partly") == "partly cloudy"
        assert Tpre("weather.cloudy.partly", lang="it") == "nuvolosità variabile"
        assert Tpre("weather.cloudy.partly", lang="ru") == "переменная облачность"
        assert Tpre("like.numerical") == "like"
        assert Tpre("like.numerical", lang="it") == "mi piace"


def test_translate_context(T):
    with context(T):
        assert T("test") == "test"
        assert T("partly cloudy") == "partly cloudy"
        assert T("like") == "like"

        with language("it"):
            assert T("test") == "test"
            assert T("partly cloudy") == "nuvolosità variabile"
            assert T("like") == "mi piace"

        with language("ru"):
            assert T("test") == "test"
            assert T("partly cloudy") == "переменная облачность"

        with language("it"):
            assert T("partly cloudy", lang="ru") == "переменная облачность"


def test_plurals(T):
    with context(T):
        assert T("you received") + " " + T("like").format(n=1) == "you received a like"
        assert T("you received {}").format(T("like").format(n=1)) == "you received a like"
        assert T("you received", lang="it") + " " + T("like", lang="it").format(n=1) == "hai ricevuto un mi piace"

        assert T("you received") + " " + T("like").format(n=2) == "you received some likes"
        assert T("you received", lang="it") + " " + T("like", lang="it").format(n=2) == "hai ricevuto alcuni mi piace"

        assert T("you received") + " " + T("like").format(n=5) == "you received 5 likes"
        assert T("you received", lang="it") + " " + T("like", lang="it").format(n=5) == "hai ricevuto 5 mi piace"

        assert T("you received") + " " + T("like").format(n=10) == "you received several likes"
        assert T("you received", lang="it") + " " + T("like", lang="it").format(n=10) == "hai ricevuto diversi mi piace"

        assert T("you received") + " " + T("like").format(n=20) == "you received several likes"
        assert T("you received", lang="it") + " " + T("like", lang="it").format(n=20) == "hai ricevuto diversi mi piace"

        assert T("you received") + " " + T("like").format(n=50) == "you received a lot of likes"
        assert (
            T("you received", lang="it") + " " + T("like", lang="it").format(n=50) == "hai ricevuto tantissimi mi piace"
        )

        assert T("you received") + " " + T("like").format(n=100) == "you received a lot of likes"
        assert (
            T("you received", lang="it") + " " + T("like", lang="it").format(n=100)
            == "hai ricevuto tantissimi mi piace"
        )


def test_format(T):
    with context(T):
        assert T("type {n} characters").format(n=10) == "type 10 characters"
        assert T("type {n} characters", lang="it").format(n=10) == "digita 10 caratteri"
        assert T("type {n} characters") % {"n": 10} == "type 10 characters"
        assert T("type {n} characters", lang="it") % {"n": 10} == "digita 10 caratteri"
        assert T("type {} characters") % (10,) == "type 10 characters"
        assert T("type {} characters", lang="it") % (10,) == "digita 10 caratteri"
        assert T("type {} characters") % 10 == "type 10 characters"
        assert T("type {} characters", lang="it") % 10 == "digita 10 caratteri"
