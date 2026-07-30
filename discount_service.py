from typing import List, Optional, Dict
from decimal import Decimal

from models import CartItem, PaymentInfo, DiscountedPrice


# Voucher codes: code -> percentage
VOUCHERS = {
    "SUPER69": Decimal("69"),
}

# Bank offers: bank_name -> percentage
BANK_OFFERS = {
    "ICICI": Decimal("10"),
}


class DiscountService:
    """Service for calculating cart discounts and validating discount codes."""

    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        payment_info: Optional[PaymentInfo] = None,
        voucher_code: Optional[str] = None,
    ) -> DiscountedPrice:
        """
        Calculate final price after applying discount logic:
        1. Brand/category discounts (pre-applied in current_price)
        2. Voucher codes
        3. Bank offers
        """
        if not cart_items:
            return DiscountedPrice(
                original_price=Decimal("0"),
                final_price=Decimal("0"),
                message="Cart is empty"
            )

        applied_discounts: Dict[str, Decimal] = {}

        # Calculate totals
        original_total = sum(
            item.product.base_price * item.quantity for item in cart_items
        )
        current_total = sum(
            item.product.current_price * item.quantity for item in cart_items
        )

        # Track pre-applied brand/category discounts
        pre_applied = original_total - current_total
        if pre_applied > 0:
            applied_discounts["brand_category_discount"] = pre_applied

        working_total = current_total

        # Apply voucher if valid
        if voucher_code and await self.validate_discount_code(voucher_code):
            percentage = VOUCHERS[voucher_code.upper()]
            voucher_discount = (working_total * percentage / 100).quantize(Decimal("0.01"))
            applied_discounts[f"voucher_{voucher_code}"] = voucher_discount
            working_total -= voucher_discount

        # Apply bank offer
        if payment_info and payment_info.method == "CARD" and payment_info.bank_name:
            bank_percentage = BANK_OFFERS.get(payment_info.bank_name.upper())
            if bank_percentage:
                bank_discount = (working_total * bank_percentage / 100).quantize(Decimal("0.01"))
                applied_discounts[f"{payment_info.bank_name}_offer"] = bank_discount
                working_total -= bank_discount

        final_price = max(working_total, Decimal("0"))
        total_savings = original_total - final_price

        return DiscountedPrice(
            original_price=original_total,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message=f"Total savings: ₹{total_savings}"
        )

    async def validate_discount_code(
        self,
        code: str
    ) -> bool:
        return code.upper() in VOUCHERS
