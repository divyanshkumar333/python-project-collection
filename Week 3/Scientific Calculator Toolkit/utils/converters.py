class UnitConverter:
    """
    Handles unit conversions for Length, Weight, and Temperature.
    """
    
    # Length conversion factors relative to Meters (m)
    LENGTH_FACTORS = {
        'meter': 1.0,
        'kilometer': 1000.0,
        'centimeter': 0.01
    }

    # Weight conversion factors relative to Grams (g)
    WEIGHT_FACTORS = {
        'gram': 1.0,
        'kilogram': 1000.0
    }

    @classmethod
    def convert_length(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts length between meter, kilometer, and centimeter."""
        from_u = from_unit.lower().strip()
        to_u = to_unit.lower().strip()
        if from_u not in cls.LENGTH_FACTORS or to_u not in cls.LENGTH_FACTORS:
            raise ValueError(f"Unsupported length units. Supported: {list(cls.LENGTH_FACTORS.keys())}")
        
        # Convert to base unit (meters) then to target unit
        value_in_meters = value * cls.LENGTH_FACTORS[from_u]
        return value_in_meters / cls.LENGTH_FACTORS[to_u]

    @classmethod
    def convert_weight(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts weight between gram and kilogram."""
        from_u = from_unit.lower().strip()
        to_u = to_unit.lower().strip()
        if from_u not in cls.WEIGHT_FACTORS or to_u not in cls.WEIGHT_FACTORS:
            raise ValueError(f"Unsupported weight units. Supported: {list(cls.WEIGHT_FACTORS.keys())}")
        
        # Convert to base unit (grams) then to target unit
        value_in_grams = value * cls.WEIGHT_FACTORS[from_u]
        return value_in_grams / cls.WEIGHT_FACTORS[to_u]

    @classmethod
    def convert_temperature(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Converts temperature between Celsius, Fahrenheit, and Kelvin."""
        from_u = from_unit.upper().strip()
        to_u = to_unit.upper().strip()
        supported = {'C', 'F', 'K', 'CELSIUS', 'FAHRENHEIT', 'KELVIN'}
        
        # Normalize unit names
        def normalize(unit: str) -> str:
            if unit in ('C', 'CELSIUS'):
                return 'C'
            if unit in ('F', 'FAHRENHEIT'):
                return 'F'
            if unit in ('K', 'KELVIN'):
                return 'K'
            raise ValueError(f"Unsupported unit: {unit}")

        try:
            from_norm = normalize(from_u)
            to_norm = normalize(to_u)
        except ValueError as e:
            raise ValueError(f"Unsupported temperature units. Supported: Celsius (C), Fahrenheit (F), Kelvin (K)") from e

        if from_norm == to_norm:
            return value

        # Convert input to Celsius first
        if from_norm == 'C':
            celsius = value
        elif from_norm == 'F':
            celsius = (value - 32.0) * 5.0 / 9.0
        else:  # 'K'
            celsius = value - 273.15

        # Convert Celsius to output unit
        if to_norm == 'C':
            return celsius
        elif to_norm == 'F':
            return (celsius * 9.0 / 5.0) + 32.0
        else:  # 'K'
            return celsius + 273.15


class NumberSystemConverter:
    """
    Converts numbers between Binary, Octal, Decimal, and Hexadecimal.
    """
    
    @staticmethod
    def to_decimal(value_str: str, from_base: int) -> int:
        """Converts a value from a specified base (2, 8, 10, 16) to decimal integer."""
        val = value_str.strip()
        if from_base not in (2, 8, 10, 16):
            raise ValueError("Unsupported base. Choose 2 (Bin), 8 (Oct), 10 (Dec), or 16 (Hex).")
        try:
            return int(val, from_base)
        except ValueError as e:
            base_names = {2: "binary", 8: "octal", 10: "decimal", 16: "hexadecimal"}
            raise ValueError(f"'{val}' is not a valid {base_names[from_base]} representation.") from e

    @staticmethod
    def from_decimal(decimal_value: int, to_base: int) -> str:
        """Converts a decimal integer to a string in the specified base (2, 8, 10, 16)."""
        if to_base == 2:
            return bin(decimal_value)[2:]  # Remove '0b'
        elif to_base == 8:
            return oct(decimal_value)[2:]  # Remove '0o'
        elif to_base == 10:
            return str(decimal_value)
        elif to_base == 16:
            return hex(decimal_value)[2:].upper()  # Remove '0x'
        else:
            raise ValueError("Unsupported base. Choose 2 (Bin), 8 (Oct), 10 (Dec), or 16 (Hex).")
