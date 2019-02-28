from csvvalidator import CSVValidator, enumeration

from .models import Medicine


def validate_csv(csv):
    field_names = ("provider_id", "kind", "name", "dosage", "measure", "amount")

    validator = CSVValidator(field_names)

    kinds = [kind[0] for kind in Medicine.KIND]

    validator.add_header_check("HEADER", "bad header")
    validator.add_value_check(
        "provider_id", int, "PROVIDER", "provider_id must be an integer"
    )
    validator.add_value_check(
        "kind", enumeration(*kinds), "PROVIDER", f"kind must be {str(kinds)}"
    )

    return validator.validate(csv)
