from language_service.service.tag.chinese import tag_chinese
from language_service.service.tag.danish import tag_danish
from language_service.service.tag.english import tag_english
from language_service.service.tag.spanish import tag_spanish


def tag(language, text):
    if language == "CHINESE":
        return tag_chinese(text)
    elif language == "DANISH":
        return tag_danish(text)
    elif language == "ENGLISH":
        return tag_english(text)
    elif language == "SPANISH":
        return tag_spanish(text)
    else:
        raise NotImplementedError("Unknown language requested: %s")
