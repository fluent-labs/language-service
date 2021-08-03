import da_core_news_sm
from language_service.dto.word import Word

parser = da_core_news_sm.load()


def tag_danish(text):
    return [
        Word(token=word.text, tag=word.pos_, lemma=word.lemma_) for word in parser(text)
    ]
