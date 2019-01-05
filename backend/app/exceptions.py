from jaaxman.exceptions import JaaxmanException


class RssFetchError(JaaxmanException):
    pass


class RssParseError(JaaxmanException):
    pass


class CloudTranslationError(JaaxmanException):
    pass


class CloudTranslationParseError(CloudTranslationError):
    pass
