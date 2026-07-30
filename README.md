# Fashion E-commerce Discount Service

Discount calculation service for fashion e-commerce.

## Supported Discounts

- **Brand discounts**: "Min 40% off on PUMA" (pre-applied in `current_price`)
- **Category discounts**: "Extra 10% off on T-shirts" (pre-applied)
- **Bank offers**: "10% instant discount on ICICI Bank cards"
- **Vouchers**: "SUPER69" for 69% off

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest test_discount_service.py -v
```

## Usage

```python
from discount_service import DiscountService
from fake_data import get_puma_tshirt_cart, ICICI_CARD_PAYMENT

service = DiscountService()
result = await service.calculate_cart_discounts(
    cart_items=get_puma_tshirt_cart(),
    payment_info=ICICI_CARD_PAYMENT
)
# Original: ₹1999, Final: ₹971.51
```

## Assumptions

1. Brand/category discounts are pre-applied in `Product.current_price`
2. Discount order: Brand/Category → Voucher → Bank Offer
3. Single voucher per order

## Files

- `models.py` - Data models
- `discount_service.py` - Core service
- `fake_data.py` - Test data
- `test_discount_service.py` - Tests
