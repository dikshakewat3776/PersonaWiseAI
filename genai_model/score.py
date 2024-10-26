def calculate_financial_score(financial_data):
    # Input validation
    if financial_data.get("income", 0) < 0:
        return "Error: Income cannot be negative."
    if financial_data.get("expenses", 0) < 0:
        return "Error: Expenses cannot be negative."
    if financial_data.get("savings", 0) < 0:
        return "Error: Savings cannot be negative."
    if financial_data.get("debt", 0) < 0:
        return "Error: Debt cannot be negative."

    # Extract values
    income = financial_data["income"]
    expenses = financial_data["expenses"]
    savings = financial_data["savings"]
    debt = financial_data["debt"]

    # Calculations
    net_income = income - expenses
    savings_rate = (savings / income * 100) if income > 0 else 0
    debt_to_income_ratio = (debt / income * 100) if income > 0 else 0

    financial_score = (0.4 * net_income) + (0.3 * savings_rate) - (0.3 * debt_to_income_ratio)

    # Health status classification
    if financial_score > 75:
        health_status = "Good Financial Health"
    elif financial_score >= 50:
        health_status = "Moderate Financial Health"
    else:
        health_status = "Poor Financial Health"

    return {
        "Net Income": net_income,
        "Savings Rate (%)": savings_rate,
        "Debt-to-Income Ratio (%)": debt_to_income_ratio,
        "Financial Score": financial_score,
        "Health Status": health_status
    }


if __name__ == "__main__":
    financial_data = {
        "income": 5000,
        "expenses": 3000,
        "savings": 1000,
        "debt": 2000
    }

    result = calculate_financial_score(financial_data)
    print(result)