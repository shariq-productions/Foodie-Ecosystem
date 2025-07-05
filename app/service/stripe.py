import datetime
from app.models.transaction import TransactionModel
import stripe
from stripe import PaymentIntent
import json
from fastapi import HTTPException
from app.core.config import settings
from beanie import PydanticObjectId

calculateTax = False

async def create_payment_service(orderAmount: int, currency: str):
    try:
        if calculateTax:
            taxCalculation = calculate_tax(orderAmount, currency)
            intent: PaymentIntent = stripe.PaymentIntent.create(
                amount=taxCalculation['amount_total'],
                currency=currency,
                automatic_payment_methods={'enabled': True},
                metadata={'tax_calculation': taxCalculation['id']}
            )
        else:
            intent: PaymentIntent = stripe.PaymentIntent.create(
                amount=orderAmount,
                currency='usd',
                automatic_payment_methods={'enabled': True}
            )
        return intent.client_secret
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail={'error': {'message': str(e)}})
    except Exception as e:
        raise HTTPException(status_code=400, detail={'error': {'message': str(e)}})

async def calculate_tax(orderAmount: int, currency: str):
    tax_calculation = await stripe.tax.Calculation.create(
        currency=currency,
        customer_details={
            "address": {
                "line1": "10709 Cleary Blvd",
                "city": "Plantation",
                "state": "FL",
                "postal_code": "33324",
                "country": "US",
            },
            "address_source": "shipping",
        },
        line_items=[
            {
                "amount": orderAmount,  # Amount in cents
                "reference": "ProductRef",
                "tax_behavior": "exclusive",
                "tax_code": "txcd_30011000"
            }
        ],
        shipping_cost={"amount": 300}
    )
    return tax_calculation

async def webhook_service(payload, stripe_signature: str):
    webhook_secret = settings.stripe_publishable_key
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=stripe_signature, secret=webhook_secret
            )
        else:
            event = json.loads(payload)

        event_type = event['type']
        data_object = event['data']['object']

        if event_type == 'payment_intent.succeeded':
            print('💰 Payment received!')
        elif event_type == 'payment_intent.payment_failed':
            print('❌ Payment failed.')
    except Exception as e:
        print(f"Webhook error: {e}")
        raise HTTPException(status_code=400, detail={'error': str(e)})

async def saveTransaction(user_id: PydanticObjectId, amount: int, payment_method: str, user_type: str):
    inserted_transaction = {
        "user_id": user_id,
        "amount": amount,
        "payment_method": payment_method,
        "user_type": user_type,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }
    transaction_doc = TransactionModel(**inserted_transaction)
    await transaction_doc.insert()
    return transaction_doc.id

async def payUsers(user_id: str):
    pass