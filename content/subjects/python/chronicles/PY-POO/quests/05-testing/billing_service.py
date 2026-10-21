"""Cloud Storage Billing Service module for TDD cycle implementation.

Business requirements:
- Storage consumption cannot be negative (raise ValueError).
- Tier 1: First 100 GB billed at $0.02 per GB.
- Tier 2: Consumption beyond 100 GB billed at $0.015 per GB.
- Enterprise discount: 10% off total invoice if is_enterprise is True.
"""


class StorageBillingCalculator:
    """Calculates storage consumption invoices following tiered pricing rules."""

    TIER_1_RATE: float = 0.02
    TIER_2_RATE: float = 0.015
    TIER_1_LIMIT: float = 100.0
    ENTERPRISE_DISCOUNT: float = 0.10

    def calculate_invoice(self, gigabytes: float, is_enterprise: bool = False) -> float:
        """Calculate total storage invoice based on consumption and tier status.

        Args:
            gigabytes: Total data volume stored in gigabytes.
            is_enterprise: Flag indicating if the account qualifies for enterprise discount.

        Returns:
            Calculated total invoice amount as float.

        Raises:
            ValueError: If gigabytes is negative with message 'Storage consumption cannot be negative'.
        """
        # TODO: Implement validation for negative gigabytes
        # TODO: Implement tiered pricing calculation
        # TODO: Apply enterprise discount if is_enterprise is True
        # TODO: Return final total amount
        if gigabytes < 0:
            raise ValueError("Storage consumption cannot be negative")
        if gigabytes == 0.0:
            cost = 0.00
        if gigabytes <= self.TIER_1_LIMIT:
            cost = gigabytes * self.TIER_1_RATE
        else:
            cost_tier1 = 100 * self.TIER_1_RATE
            overcost = (gigabytes - self.TIER_1_LIMIT) * self.TIER_2_RATE
            cost = cost_tier1 + overcost
        if is_enterprise:
            cost *= (1.0 - self.ENTERPRISE_DISCOUNT)

        return cost