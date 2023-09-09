from decimal import Decimal

from cerberus import Validator, TypeDefinition

Validator.types_mapping["decimal"] = TypeDefinition("decimal", (Decimal,), ())

validator = Validator()
