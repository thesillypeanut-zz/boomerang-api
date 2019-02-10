from src.helpers import handle_exception


def validate_non_empty_request_body(request_body):
    def validate():
        if not request_body:
            return handle_exception('Bad Request: Request must have a body.', 400)

    return validate


def validate_required_fields(request_body, required_fields):
    def validate():
        if set(request_body) != set(required_fields):
            raise handle_exception(
                f'Bad Request: One or more required fields are missing or invalid: {", ".join(required_fields)}', 400
            )

    return validate


def validate_allowed_fields(request_body, allowed_fields):
    def validate():
        for field in request_body:
            if field not in allowed_fields:
                raise handle_exception(
                    f'Bad Request: Field "{field}" is not allowed. Allowed fields are: {", ".join(allowed_fields)}',
                    400
                )

    return validate
