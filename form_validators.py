from wtforms.validators import ValidationError

from constants import States


class PhoneNumerValidator:

    def __call__(self, form, field):
        given_state_code = field.data.split('-')[0]
        available_codes = form.state.data.value.phone_codes
        if given_state_code not in available_codes:
            raise ValidationError(f'Given state code {given_state_code} is not in acceptable code list: {available_codes}')


class RequiredPreviousField:

    def __init__(self, previous_field):
        self.previous_field = previous_field

    def __call__(self, form, field):
        previous_value = getattr(form, self.previous_field).data

        if (not previous_value) and field.data:
            raise ValidationError(f"Given previous value: {previous_value} and set data {field.data} are not compatible.")
