from pydantic import BaseModel, ValidationError, field_validator, constr


class Form(BaseModel):
    pass


class FormSend(Form):
    name: str = None
    phone: int
    message: str = ""

    @field_validator("phone")
    def validate_phone(cls, v):
        phone = str(v)
        print(phone)
        if not phone.startswith("7") or len(phone) != 11:
            raise ValueError("Incorrect phone number")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        if len(v) < 2:
            raise ValueError("Incorrect client name")
        return v
