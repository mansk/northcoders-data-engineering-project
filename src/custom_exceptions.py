class AccessDenied(Exception):
    pass


class BucketAlreadyExists(Exception):
    pass


class BucketAlreadyOwnedByYou(Exception):
    pass


class BucketNotEmpty(Exception):
    pass


class InvalidBucketName(Exception):
    pass


class InvalidParameterException(Exception):
    pass


class InvalidRequest(Exception):
    pass


class MalformedXML(Exception):
    pass


class NoSuchBucket(Exception):
    pass


class NoSuchKey(Exception):
    pass


class ParameterNotFound(Exception):
    pass


class ResourceExistsException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class ValidationException(Exception):
    pass


error_map = {
    "AccessDenied": AccessDenied,
    "BucketAlreadyExists": BucketAlreadyExists,
    "BucketAlreadyOwnedByYou": BucketAlreadyOwnedByYou,
    "BucketNotEmpty": BucketNotEmpty,
    "InvalidBucketName": InvalidBucketName,
    "InvalidParameterException": InvalidParameterException,
    "InvalidRequest": InvalidRequest,
    "MalformedXML": MalformedXML,
    "NoSuchBucket": NoSuchBucket,
    "NoSuchKey": NoSuchKey,
    "ParameterNotFound": ParameterNotFound,
    "ResourceExistsException": ResourceExistsException,
    "ResourceNotFoundException": ResourceNotFoundException,
    "ValidationException": ValidationException,
}


def error_handler(e):
    error_body = e.response["Error"]
    error_code = error_body["Code"]
    error_msg = error_body["Message"]

    if error_code in error_map:
        raise error_map[error_code](error_msg)
