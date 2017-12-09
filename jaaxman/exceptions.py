# 独自定義の例外の基底クラス
class JaaxmanException(Exception):
    pass


# バリデーションエラーに関する基底クラス
class ValidationError(JaaxmanException):
    pass


class InvalidDeploymentRoleError(ValidationError):
    pass


class EnvironmentVariableNotDefineError(JaaxmanException):
    pass
