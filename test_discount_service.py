import pytest
from decimal import Decimal

from discount_service import DiscountService
from fake_data import (
    ICICI_CARD_PAYMENT, UPI_PAYMENT,
    get_puma_tshirt_cart,
)


@pytest.fixture
def service():
    return DiscountService()


class TestMainScenario:
    """
    Scenario from problem statement:
    - PUMA T-shirt with 40% brand + 10% category (pre-applied)
    - ICICI bank offer: 10% instant discount
    """

    @pytest.mark.asyncio
    async def test_puma_tshirt_with_icici_bank_offer(self, service):
        """Base: ₹1999 -> After brand/cat: ₹1079.46 -> After ICICI 10%: ₹971.51"""
        cart = get_puma_tshirt_cart()

        result = await service.calculate_cart_discounts(
            cart_items=cart,
            payment_info=ICICI_CARD_PAYMENT,
        )

        assert result.original_price == Decimal("1999.00")
        assert result.applied_discounts["brand_category_discount"] == Decimal("919.54")
        assert result.applied_discounts["ICICI_offer"] == Decimal("107.95")
        assert result.final_price == Decimal("971.51")

    @pytest.mark.asyncio
    async def test_puma_tshirt_without_bank_offer(self, service):
        """UPI payment - no bank offer."""
        cart = get_puma_tshirt_cart()

        result = await service.calculate_cart_discounts(
            cart_items=cart,
            payment_info=UPI_PAYMENT,
        )

        assert result.final_price == Decimal("1079.46")


class TestVoucherCodes:
    """Test voucher application."""

    @pytest.mark.asyncio
    async def test_super69_voucher(self, service):
        """SUPER69 gives 69% off."""
        cart = get_puma_tshirt_cart()

        result = await service.calculate_cart_discounts(
            cart_items=cart,
            voucher_code="SUPER69",
        )

        # 69% of 1079.46 = 744.83
        assert result.applied_discounts["voucher_SUPER69"] == Decimal("744.83")
        assert result.final_price == Decimal("334.63")

    @pytest.mark.asyncio
    async def test_invalid_voucher(self, service):
        """Invalid code is ignored."""
        cart = get_puma_tshirt_cart()

        is_valid = await service.validate_discount_code("INVALID")
        assert is_valid is False


class TestDiscountStacking:
    """Test combining voucher + bank offer."""

    @pytest.mark.asyncio
    async def test_voucher_and_bank_offer_stack(self, service):
        """Voucher + bank offer both apply."""
        cart = get_puma_tshirt_cart()

        result = await service.calculate_cart_discounts(
            cart_items=cart,
            payment_info=ICICI_CARD_PAYMENT,
            voucher_code="SUPER69",
        )

        # 1079.46 -> 69% voucher -> 334.63 -> 10% ICICI -> 301.17
        assert "voucher_SUPER69" in result.applied_discounts
        assert "ICICI_offer" in result.applied_discounts
        assert result.final_price == Decimal("301.17")


class TestEdgeCases:
    """Edge cases."""

    @pytest.mark.asyncio
    async def test_empty_cart(self, service):
        result = await service.calculate_cart_discounts(cart_items=[])
        assert result.final_price == Decimal("0")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
