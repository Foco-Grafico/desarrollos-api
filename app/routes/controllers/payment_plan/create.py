from app.models.payment_plan import PaymentPlan
from services.db import colina_db
from fastapi import HTTPException
from app.utils import auth, perms
from app.enums.permissions import PAYMENT_PLAN

async def payment_plan(
    token: str,
    payment_plan: PaymentPlan
):
    perm = perms.get_perm_id(PAYMENT_PLAN.CREATE.value)
    if not auth.verify_perm(token, perm):
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action.")

    try:
        plan_id = colina_db.insert(
            table='payment_plans',
            data={
                'price': payment_plan.price,
                'months_to_pay': payment_plan.months_to_pay,
                'annuity': payment_plan.annuity,
                'pay_per_month': payment_plan.pay_per_month,
                'interest_rate': payment_plan.interest_rate,
                'payment_method': payment_plan.payment_method,
                'down_payment': payment_plan.down_payment
            }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating payment plan")
    
    return {
        "plan_id": plan_id,
        "message": "Payment plan created successfully"
    }