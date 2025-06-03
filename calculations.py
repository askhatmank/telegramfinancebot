def calculate_credit(amount: float, years: float, rate: float) -> tuple:
    months = years * 12
    monthly_rate = rate / 100 / 12
    payment = (amount * monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    total = payment * months
    overpayment = total - amount
    return round(payment, 2), round(total, 2), round(overpayment, 2)

def calculate_mortgage(amount: float, years: float, rate: float, insurance: float = 0.0) -> tuple:
    payment, total, overpayment = calculate_credit(amount, years, rate)
    if insurance > 0:
        insurance_payment = amount * insurance / 100 / 12
        payment += insurance_payment
        total += insurance_payment * years * 12
    return round(payment, 2), round(total, 2), round(overpayment, 2)

def calculate_deposit(amount: float, years: float, rate: float, capitalization: int) -> tuple:
    periods = years * capitalization
    total = amount * (1 + (rate / 100)/capitalization)**periods
    profit = total - amount
    return round(total, 2), round(profit, 2)

def calculate_vacation(budget: float, days: int, daily_cost: float) -> tuple:
    total = days * daily_cost
    remaining = budget - total
    return round(total, 2), round(remaining, 2)