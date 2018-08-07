from django.core.exceptions import ValidationError

def minimum_validator(minimum = 0):
    '''
    passes a minimum value , that generates a function which
    does the corresponding validation
    :param minimum:
    :return:
    '''
    def is_greater(value, minimum=minimum):
        if not value > minimum:
            raise ValidationError(
                ('%(value)s is not greater than zero'),
                params={'value': value},
            )
    return is_greater

