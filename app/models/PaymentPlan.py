from pydantic import BaseModel

class PaymentPlan(BaseModel):
    price: float
    months_to_pay: int
    annuity: float
    pay_per_month: float
    interest_rate: float
    payment_method: str