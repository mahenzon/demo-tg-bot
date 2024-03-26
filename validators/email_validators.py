from aiogram import types

from email_validator import validate_email, EmailNotValidError


def valid_email_filter(message: types.Message) -> dict[str, str] | None:
    try:
        email = validate_email(message.text)
    except EmailNotValidError:
        return None

    return {"email": email.normalized}
