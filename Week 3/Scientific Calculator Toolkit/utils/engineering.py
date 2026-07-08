import statistics

class EngineeringUtilities:
    """
    Implements engineering and statistics utilities, including BMI calculation,
    percentage computations, and list descriptive statistics (Mean, Median, Mode, Std Dev).
    """

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
        """
        Calculates Body Mass Index (BMI) and provides health classification.
        
        Formula:
            BMI = weight_kg / (height_m ^ 2)
        """
        if weight_kg <= 0 or height_cm <= 0:
            raise ValueError("Weight and height must be positive numbers.")
        
        height_m = height_cm / 100.0
        bmi = weight_kg / (height_m ** 2)
        
        # Classification
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
            
        return {
            "bmi": bmi,
            "category": category
        }

    @staticmethod
    def percentage_of_value(percentage: float, total_value: float) -> float:
        """Calculates what is X% of Y."""
        return (percentage / 100.0) * total_value

    @staticmethod
    def value_as_percentage(part_value: float, total_value: float) -> float:
        """Calculates part_value is what percentage of total_value."""
        if total_value == 0:
            raise ZeroDivisionError("Total value cannot be zero for calculating percentage.")
        return (part_value / total_value) * 100.0

    @staticmethod
    def calculate_list_statistics(numbers: list[float]) -> dict:
        """
        Calculates mean, median, mode, and standard deviation for a list of numbers.
        Uses Python's statistics module.
        """
        if not numbers:
            raise ValueError("The list of numbers cannot be empty.")

        n = len(numbers)
        avg = sum(numbers) / n
        mean_val = statistics.mean(numbers)
        median_val = statistics.median(numbers)
        
        # Handle cases where multiple modes exist or no mode exists cleanly
        try:
            mode_val = statistics.mode(numbers)
        except statistics.StatisticsError:
            mode_val = "No unique mode"

        # Standard deviation requires at least 2 data points
        if n >= 2:
            stdev_val = statistics.stdev(numbers)
        else:
            stdev_val = 0.0

        return {
            "count": n,
            "average": avg,
            "mean": mean_val,
            "median": median_val,
            "mode": mode_val,
            "std_dev": stdev_val
        }
