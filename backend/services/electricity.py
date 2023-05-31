import pandas as pd
from xlrd import xldate_as_datetime
from ..logger import logger
from typing import ClassVar
from pathlib import Path

class Electricity:
    """
    This class is used to calculate electricity costs.
    """
    GRID_FEE: ClassVar[float] = 0.12
    AREA_PROVIDER: ClassVar[str] = "5414492999998"

    def __init__(self, production_profile: Path | str, consumption_profile: Path | str, energy_cost: Path | str):
        self.production_profile = self._load_data(
            production_profile,
            sheet_name="Ex-ante 2023 (IP8)", 
            usecols=["UTC", self.AREA_PROVIDER],
            date_column="UTC"
        )
        self.consumption_profile = self._load_consumption_data(consumption_profile)
        self.energy_cost = self._load_cost_data(energy_cost)
        self._calculate_grid_prices()


    @classmethod
    def create_from_spreadsheets(cls) -> "Electricity":
        base_dir = Path(__file__).resolve().parent.parent.parent
        production_profile = base_dir / "data" / "production_profiles.xlsx"
        consumption_profile = base_dir / "data" / "consumption_profiles.xlsb"
        energy_cost = base_dir / "data" / "energy_cost.xlsx"
        return cls(production_profile, consumption_profile, energy_cost)
    
    
    @staticmethod
    def _load_data(
        file_path: Path | str, 
        sheet_name: str = None, 
        skiprows: int = None, 
        usecols: list[str] = None, 
        date_column: str = None
    ) -> pd.DataFrame:
        """
        Loads data from an Excel file.
        
        :param file_path: Path or str to the data file
        :param sheet_name: Name of the sheet to read from
        :param skiprows: Number of rows to skip at the start
        :param usecols: List of column names to use
        :param date_column: Column name to convert to datetime and set as index
        """
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows, usecols=usecols)
        if date_column:
            df[date_column] = pd.to_datetime(df[date_column])
            df.set_index(date_column, inplace=True)
        return df

    def _load_consumption_data(self, file_path: Path | str) -> pd.DataFrame:
        """
        Loads consumption data from an Excel file.
        
        :param file_path: Path or str to the data file
        """
        df = pd.read_excel(file_path, skiprows=2, usecols=["CET", self.AREA_PROVIDER])
        df["CET"] = df["CET"].apply(lambda x: xldate_as_datetime(float(x), 0))
        df.set_index("CET", inplace=True)
        return df

    @staticmethod
    def _load_cost_data(file_path: Path | str) -> pd.DataFrame:
        """
        Loads cost data from an Excel file.
        
        :param file_path: Path or str to the data file
        """
        df = pd.read_excel(file_path)
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)
        df["Euro"] = df["Euro"].replace("[\€,]", "", regex=True).astype(float)
        return df

    def _calculate_grid_prices(self):
        """
        Calculates the price of buying and selling energy to/from the grid.
        """
        energy_cost_kwh = self.energy_cost["Euro"].mean() / 1000
        logger.info(f"energy_cost_kwh {energy_cost_kwh}")
        self.grid_price = (energy_cost_kwh * 1.20) + self.GRID_FEE
        self.grid_sell_price = energy_cost_kwh * 0.80

    async def calculate_total_cost(self, annual_energy_consumption: float, wp_of_installation: int) -> float:
        """
        Calculates the total cost of energy consumption and production.
        
        :param annual_energy_consumption: Estimated annual energy consumption in kWh
        :param wp_of_installation: Power of the solar installation in watts peak (Wp)
        """
        total_energy_produced_kwh = (self.production_profile[self.AREA_PROVIDER].sum() * wp_of_installation * 0.25) / 1000
        total_energy_consumed = self.consumption_profile[self.AREA_PROVIDER].sum() * annual_energy_consumption

        energy_from_grid, energy_to_grid = self._calculate_energy_flow(total_energy_produced_kwh, total_energy_consumed)

        cost_from_grid = energy_from_grid * self.grid_price
        revenue_from_grid = energy_to_grid * self.grid_sell_price

        total_cost = cost_from_grid - revenue_from_grid

        self._log_calculation_results(
            total_energy_produced_kwh,
            total_energy_consumed, energy_from_grid, 
            energy_to_grid, 
            cost_from_grid, 
            revenue_from_grid, 
            total_cost
        )

        return total_cost

    @staticmethod
    def _calculate_energy_flow(total_energy_produced: float, total_energy_consumed: float) -> tuple[float]:
        """
        Calculates the amount of energy bought from or sold to the grid.
        
        :param total_energy_produced: Total amount of energy produced in kWh
        :param total_energy_consumed: Total amount of energy consumed in kWh
        """
        energy_from_grid = max(0, total_energy_consumed - total_energy_produced)
        energy_to_grid = max(0, total_energy_produced - total_energy_consumed)
        return energy_from_grid, energy_to_grid

    def _log_calculation_results(
            self, 
            total_energy_produced, 
            total_energy_consumed, 
            energy_from_grid, 
            energy_to_grid, 
            cost_from_grid, 
            revenue_from_grid, total_cost
        ) -> None:
        logger.info(f"total_energy_produced_kwh {total_energy_produced}")
        logger.info(f"total_energy_consumed {total_energy_consumed}")
        logger.info(f"energy_from_grid {energy_from_grid}")
        logger.info(f"energy_to_grid {energy_to_grid}")
        logger.info(f"cost_from_grid {cost_from_grid}")
        logger.info(f"revenue_from_grid {revenue_from_grid}")
        logger.info(f"total_cost {total_cost}")




ELECTRICITY = Electricity.create_from_spreadsheets()
