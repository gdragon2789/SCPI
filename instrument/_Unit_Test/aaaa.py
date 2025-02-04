class Function:
    CAP = "CAPacitance"
    VOLT = "VOLTage"
    CURR = "CURRent"

    def __str__(self):
        return self.value

# Use class attributes like Enum
print(f"Hi {Function.CAP}")  # Output: Hi CAPacitance
