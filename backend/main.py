from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from .models import SolarPanelInput, OkResponse, CreatedResponse
from .services.solar_panel import SolarPanelPayback
from .exceptions import CalculationException
from .logger import logger

app = FastAPI()


@app.exception_handler(CalculationException)
async def calculation_exception_handler(request, exc: CalculationException):
    logger.error(f"Error occurred: {str(exc)}")
    return JSONResponse(status_code=400, content={"error": str(exc)})


async def get_solar_panel_payback(solar_panel_input: SolarPanelInput) -> SolarPanelPayback:
    return SolarPanelPayback(
        solar_panel_input.annual_energy_consumption,
        solar_panel_input.installation_cost,
        solar_panel_input.wp_of_installation,
    )

@app.post(
    "/calculate_payback_time",
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED,
    description="Calculates the payback time of solar panels based on given input",
    tags=["Payback Time Calculation"],
    summary="Calculate Payback Time",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,
            "description": "OK response",
        },
        status.HTTP_201_CREATED: {
            "model": CreatedResponse,
            "description": "Created response, the payback time has been successfully calculated",
        },
    },
)
async def calculate_payback_time(solar_panel: SolarPanelPayback = Depends(get_solar_panel_payback)):
    try:
        payback_time = await solar_panel.calculate_payback_time()
        logger.info(f"Calculated payback time: {payback_time}")
        return {"message": "Payback time calculated successfully", "data": {"payback_time": payback_time}}
    except Exception as e:
        logger.error(f"Error occurred while calculating payback time: {str(e)}")
        raise CalculationException("Error occurred while calculating payback time")



@app.post(
    "/calculate_optimal_wp",
    response_model=CreatedResponse,
    status_code=status.HTTP_200_OK,
    description="Calculates the optimal Wp (number of solar panels) for the shortest payback time",
    tags=["Optimal Wp Calculation"],
    summary="Calculate Optimal Wp",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,
            "description": "OK response",
        },
        status.HTTP_201_CREATED: {
            "model": CreatedResponse,
            "description": "Created response, the payback time has been successfully calculated",
        },
    },
)
async def calculate_optimal_wp(solar_panel: SolarPanelPayback = Depends(get_solar_panel_payback)):
    try:
        optimal_wp = await solar_panel.calculate_optimal_wp()
        logger.info(f"Calculated optimal Wp: {optimal_wp}")
        return {"message": "Optimal Wp calculated successfully", "data": {"optimal_wp": optimal_wp}}
    except Exception as e:
        logger.error(f"Error occurred while calculating optimal Wp: {str(e)}")
        raise CalculationException("Error occurred while calculating optimal Wp")
