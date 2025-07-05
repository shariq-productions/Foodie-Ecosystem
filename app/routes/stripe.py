#! /usr/bin/env python3.8
import os
import json
from app.dependencies.auth import get_current_user
from app.service.cart import empty_cart, get_total_amount
from app.service.order import add_order_details
from app.service.stripe import create_payment_service, payUsers, saveTransaction, webhook_service
from fastapi import APIRouter, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import stripe
from app.core.config import settings

stripeRouter = APIRouter()

# Stripe config
stripe.set_app_info(
    name = settings.stripe_app_name,
    version = settings.stripe_app_version,
    url = settings.stripe_app_url
    )
stripe.api_version = settings.stripe_api_version
stripe.api_key = settings.stripe_api_key

# Static files and templates
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "html"))
stripeRouter.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=static_dir)

@stripeRouter.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@stripeRouter.get("/config")
async def get_config():
    return {"publishableKey": settings.stripe_publishable_key}

@stripeRouter.get("/create-payment-intent")
async def create_payment(user_data=Depends(get_current_user)):
    amount = await get_total_amount(user_data.id)
    amount = int(amount * 100)  # Convert to cents
    currency = "inr"  # You can change this to your desired currency
    clientSecret =  await create_payment_service(amount, currency)
    if clientSecret:
        await saveTransaction(user_data.id, amount, "stripe", "user")
        await payUsers(user_data.id)
        await add_order_details(user_data.id)
        await empty_cart(user_data.id)

    return {"clientSecret": clientSecret}

@stripeRouter.post("/webhook")
async def webhook_received(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()

    await webhook_service(payload, stripe_signature)
    return {"status": "success"}

