def compute_score_data(bot_response):
    # Extract values
    responses = bot_response["bot_response"]
    income = float(responses.get("What’s your monthly income?", 0))
    expenses = float(responses.get("What are your monthly expenses?", 0))
    assets = responses.get("Do you have any assets? (e.g., property, savings)", "").count("property")
    liabilities = responses.get("What are your liabilities? (e.g., loans, debts)", "").count("loans")

    # Calculate scores
    max_income = 100000
    income_score = min((income / max_income) * 100, 100)

    max_expense_ratio = 0.30
    if income > 0:
        expense_ratio = expenses / income
        expenses_score = max(0, (1 - expense_ratio / max_expense_ratio) * 100)
    else:
        expenses_score = 0

    savings_score = min(assets * 20, 100)

    max_debt_score = 100
    debt_score = max(0, max_debt_score - (liabilities * 20))

    return {
        "Income Score": round(income_score, 2),
        "Expenses Score": round(expenses_score, 2),
        "Savings Score": round(savings_score, 2),
        "Debt Score": round(debt_score, 2),
    }


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
    financial_score = max(0, min(financial_score, 100))  # Limit score to 0-100

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
        "Score": round(financial_score, 2),
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