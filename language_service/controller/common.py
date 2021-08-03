import logging

SUPPORTED_LANGUAGES = ["CHINESE", "DANISH", "ENGLISH", "SPANISH"]
logger = logging.getLogger("LanguageService")


def check_language(language):
    """
    Checks the language to see if it is valid.
    Returns either (language, None) on success or (None, error_message) on failure
    """
    if language is None or language == "":
        logger.error("No language passed")
        return None, "Language is required"

    normalized_language = language.upper()

    if normalized_language not in SUPPORTED_LANGUAGES:
        logger.error("Unsupported language %s requested" % language)
        return None, "Language %s is not supported" % language

    return normalized_language, None


def get_required_field(request, field_name):
    """
    Checks the request body for a required field
    Returns either (field, None) on success or (None, error_message) on failure
    """
    request_json = request.get_json()

    if request_json is None:
        logger.error("Request body is empty")
        return None, "A request is required"
    if field_name not in request_json:
        logger.error("Required field %s was not included in request" % field_name)
        return None, "Field %s is required" % field_name

    return request_json[field_name], None
