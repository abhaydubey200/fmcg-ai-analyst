def get_cleaning_rules(profile):
    """
    Placeholder function to return AI cleaning rules.
    Replace with actual AI logic later.
    """
    rules = """
1. Drop columns with >80% missing values.
2. Impute missing MOBILE_NO with 'UNKNOWN'.
3. Convert ORDER_DATE and ORDER_TIME to datetime.
4. Convert categorical columns to category dtype.
5. Flag outliers in TOTAL_QUANTITY and AMOUNT.
"""
    return rules
