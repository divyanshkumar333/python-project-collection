class FinancialCalculator:
    """
    Handles financial math calculations: Simple Interest, Compound Interest, EMI,
    and Percentage Increase/Decrease.
    """

    @staticmethod
    def simple_interest(principal: float, rate: float, time: float) -> dict:
        """
        Calculates simple interest and total amount.
        
        Formula:
            Interest = (P * R * T) / 100
            Total Amount = P + Interest
        """
        if principal < 0 or rate < 0 or time < 0:
            raise ValueError("Principal, rate, and time must be non-negative.")
        
        interest = (principal * rate * time) / 100.0
        total = principal + interest
        return {
            "interest": interest,
            "total_amount": total
        }

    @staticmethod
    def compound_interest(principal: float, rate: float, time: float, compounds_per_year: int = 1) -> dict:
        """
        Calculates compound interest and total accumulated amount.
        
        Formula:
            Amount = P * (1 + R / (n * 100)) ^ (n * T)
            Interest = Amount - P
        """
        if principal < 0 or rate < 0 or time < 0 or compounds_per_year <= 0:
            raise ValueError("Principal, rate, time, and compounding frequency must be positive.")
        
        total = principal * ((1.0 + (rate / (compounds_per_year * 100.0))) ** (compounds_per_year * time))
        interest = total - principal
        return {
            "interest": interest,
            "total_amount": total
        }

    @staticmethod
    def emi_calculator(principal: float, annual_rate: float, years: float) -> dict:
        """
        Calculates Equated Monthly Installment (EMI), total interest, and total payment.
        
        Formula:
            EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
            where:
                r = monthly interest rate (annual_rate / 12 / 100)
                n = loan duration in months (years * 12)
        """
        if principal <= 0 or annual_rate <= 0 or years <= 0:
            raise ValueError("Principal, rate, and years must be positive values greater than zero.")
        
        # Monthly interest rate
        r = annual_rate / (12.0 * 100.0)
        # Total number of months
        n = years * 12.0
        
        # Calculate EMI
        emi = (principal * r * ((1.0 + r) ** n)) / (((1.0 + r) ** n) - 1.0)
        total_payment = emi * n
        total_interest = total_payment - principal
        
        return {
            "monthly_emi": emi,
            "total_interest": total_interest,
            "total_payment": total_payment
        }

    @staticmethod
    def percentage_change(original: float, new_value: float) -> dict:
        """
        Calculates percentage increase or decrease.
        
        Formula:
            Change = ((New - Original) / Original) * 100
        """
        if original == 0:
            raise ZeroDivisionError("Original value cannot be zero for calculating percentage change.")
        
        change = ((new_value - original) / original) * 100.0
        change_type = "increase" if change >= 0 else "decrease"
        return {
            "change_percentage": abs(change),
            "type": change_type
        }
