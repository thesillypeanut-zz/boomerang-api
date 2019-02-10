from src.validation import common_validators

ALLOWED_FIELDS = ['first_name', 'last_name', 'password']


def build(request):
    request_body = request.json
    return [
        common_validators.validate_non_empty_request_body(request_body),
        common_validators.validate_allowed_fields(request_body, ALLOWED_FIELDS)
    ]
