from src.validation import common_validators

REQUIRED_FIELDS = ['name', 'date', 'invitees', 'sms_content']


def build(request):
    request_body = request.json
    return [
        common_validators.validate_non_empty_request_body(request_body),
        common_validators.validate_required_fields(request_body, REQUIRED_FIELDS)
    ]
