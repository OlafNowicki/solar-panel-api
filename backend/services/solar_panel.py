from .electricity import ELECTRICITY
from ..logger import logger

class SolarPanelPayback:
    """
    This class is used to calculate the payback time of solar panels
    """
    def __init__(self, annual_energy_consumption, installation_cost, wp_of_installation):
        self.annual_energy_consumption = annual_energy_consumption
        self.installation_cost = installation_cost
        self.wp_of_installation = wp_of_installation

    async def calculate_payback_time(self) -> float:
        """
        Calculates the payback time of the solar panel installation.

        :return: The payback period in years
        """
        annual_cost_savings = -1 * await ELECTRICITY.calculate_total_cost(self.annual_energy_consumption, self.wp_of_installation)
        logger.info(f"Annual cost savings: {annual_cost_savings}")
        payback_period = self.installation_cost / annual_cost_savings
        return payback_period

    async def calculate_optimal_wp(self) -> int:
        """
        Calculates the optimal power of the solar installation in watts peak (Wp) to minimize the payback period.

        :return: The optimal power in Wp
        """
        fixed_cost = 1000
        variable_cost_per_wp = (self.installation_cost - fixed_cost) / self.wp_of_installation

        min_payback_period = float('inf')
        optimal_wp = 0

        for wp in range(self.wp_of_installation, 2 * self.wp_of_installation + 1, 10):
            total_cost = fixed_cost + (variable_cost_per_wp * wp)
            annual_savings = -1 * await ELECTRICITY.calculate_total_cost(self.annual_energy_consumption, wp)
            payback_period = total_cost / annual_savings

            if payback_period < min_payback_period:
                min_payback_period = payback_period
                optimal_wp = wp

        return optimal_wp

