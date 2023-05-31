from pydantic import BaseModel, Field


class SolarPanelInput(BaseModel):
    annual_energy_consumption: float = Field(..., gt=0, description="Annual energy consumption in kWh")
    installation_cost: float = Field(..., gt=0, description="Installation cost in €")
    wp_of_installation: int = Field(..., gt=0, description="Installation capacity in Wp")

    class Config:
        schema_extra = {
            "example": {
                "annual_energy_consumption": 5000,
                "installation_cost": 10000,
                "wp_of_installation": 5000,
            }
        }



class OkResponse(BaseModel):
    message: str


class CreatedResponse(BaseModel):
    message: str
    data: dict
