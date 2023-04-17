from django.core.exceptions import ValidationError

SPECIAL_SYM = ['$', '@', '#', '%']


class PasswordValidator:

    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError('length should be at least 8 character')
        if any(char in ['=', "'", ] for char in password):
            raise ValidationError("Password should not have [ = ] or [ ' ] symbols", code='pwd_no_letter')
        if not any(char.isupper() for char in password):
            raise ValidationError('Password should have at least one uppercase letter')
        if not any(char.islower() for char in password):
            raise ValidationError('Password should have at least one lowercase letter')
        if not any(char in SPECIAL_SYM for char in password):
            raise ValidationError('Password should have at least one of the symbols $@#')
        if not any(char.isalpha() for char in password):
            raise ValidationError('Votre mot de passe ne contient pas de lettre')
        pass

    def get_help_text(self):
        return "Your password should have at least : 1 / Uppercase / Lowercase / Letter / Symbols / Numeric"
