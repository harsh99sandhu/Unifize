"""
Fake data for testing - PUMA T-shirt scenario.

- PUMA T-shirt: base ₹1999, after 40% brand + 10% category = ₹1079.46
- ICICI bank offer: 10% instant discount
- SUPER69 voucher: 69% off
"""

from decimal import Decimal
from models import Product, CartItem, PaymentInfo, BrandTier


# Products
PUMA_TSHIRT = Product(
    id="prod_001",
    brand="PUMA",
    brand_tier=BrandTier.PREMIUM,
    category="T-SHIRTS",
    base_price=Decimal("1999.00"),
    current_price=Decimal("1079.46"),  # After 40% brand + 10% category
)

# Payment
ICICI_CARD_PAYMENT = PaymentInfo(method="CARD", bank_name="ICICI", card_type="CREDIT")
UPI_PAYMENT = PaymentInfo(method="UPI")


def get_puma_tshirt_cart() -> list[CartItem]:
    return [CartItem(product=PUMA_TSHIRT, quantity=1, size="M")]
