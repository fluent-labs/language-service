import pytest
from testfixtures import compare
from language_service.service.tag import tag
from language_service.dto.word import Word


def test_can_tag_chinese():
    words = tag("CHINESE", "测试已通过，因为返回了这些单词。")
    compare(
        words,
        [
            Word(token="测试", tag="NOUN", lemma="测试"),
            Word(token="已", tag="ADV", lemma="已"),
            Word(token="通过", tag="VERB", lemma="通过"),
            Word(token="，", tag="PUNCT", lemma="，"),
            Word(token="因为", tag="ADP", lemma="因为"),
            Word(token="返回", tag="VERB", lemma="返回"),
            Word(token="了", tag="PART", lemma="了"),
            Word(token="这些", tag="DET", lemma="这些"),
            Word(token="单词", tag="NOUN", lemma="单词"),
            Word(token="。", tag="PUNCT", lemma="。"),
        ],
    )


def test_can_tag_danish():
    words = tag("DANISH", "Hej, jeg er en sætning i Dansk.")
    compare(
        words,
        [
            Word(token="Hej", tag="PROPN", lemma="Hej"),
            Word(token=",", tag="PUNCT", lemma=","),
            Word(token="jeg", tag="PRON", lemma="jeg"),
            Word(token="er", tag="AUX", lemma="være"),
            Word(token="en", tag="DET", lemma="en"),
            Word(token="sætning", tag="NOUN", lemma="sætning"),
            Word(token="i", tag="ADP", lemma="i"),
            Word(token="Dansk", tag="ADJ", lemma="Dansk"),
            Word(token=".", tag="PUNCT", lemma="."),
        ],
    )


def test_can_tag_english():
    words = tag("ENGLISH", "The test has passed because these words were returned.")
    compare(
        words,
        [
            Word(token="The", tag="DET", lemma="the"),
            Word(token="test", tag="NOUN", lemma="test"),
            Word(token="has", tag="AUX", lemma="have"),
            Word(token="passed", tag="VERB", lemma="pass"),
            Word(token="because", tag="SCONJ", lemma="because"),
            Word(token="these", tag="DET", lemma="these"),
            Word(token="words", tag="NOUN", lemma="word"),
            Word(token="were", tag="AUX", lemma="be"),
            Word(token="returned", tag="VERB", lemma="return"),
            Word(token=".", tag="PUNCT", lemma="."),
        ],
    )


def test_can_tag_spanish():
    words = tag(
        "SPANISH", "La prueba ha pasado porque estas palabras fueron devueltas."
    )
    compare(
        words,
        [
            Word(token="La", tag="DET", lemma="el"),
            Word(token="prueba", tag="NOUN", lemma="prueba"),
            Word(token="ha", tag="AUX", lemma="haber"),
            Word(token="pasado", tag="VERB", lemma="pasar"),
            Word(token="porque", tag="SCONJ", lemma="porque"),
            Word(token="estas", tag="DET", lemma="este"),
            Word(token="palabras", tag="NOUN", lemma="palabra"),
            Word(token="fueron", tag="AUX", lemma="ser"),
            Word(token="devueltas", tag="ADJ", lemma="devuelta"),
            Word(token=".", tag="PUNCT", lemma="."),
        ],
    )


def test_raises_exception_on_unknown_language():
    with pytest.raises(NotImplementedError):
        tag("KLINGON", "We can't handle this sentence")
