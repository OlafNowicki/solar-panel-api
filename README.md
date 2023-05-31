## Summary of Steps:

1.  **Problem Analysis**: Comprehensive understanding of the problem statement, requirements, data sources, unit measurements, and the business context.
    
2.  **Data Loading**: Loaded the data from the provided sources into pandas DataFrames. Three types of data are loaded:
    
    -   Energy production profile: https://www.synergrid.be/images/downloads/spp-2023-ex-ante-and-ex-post_v2.0.xlsx
    -   Energy consumption profile: https://www.synergrid.be/images/downloads/rlp0n2023-electricity.xlsb
    -   Historical energy cost data: https://my.elexys.be/MarketInformation/SpotBelpex.aspx

3.  **Data Transformation**: Cleaned and transformed the data for further calculations. This includes converting currency strings to floats, date columns to pandas datetime objects, and handling anomalies if any.
    
4.  **Implementation of Calculation Logic**: Implemented three main calculations:
    
    -   The `calculate_total_cost` method calculates the net annual cost of electricity. This considers energy production from solar panels, energy consumption, and the cost/revenue of buying or selling electricity to the grid.
    -   The `calculate_payback_time` method calculates the payback period for the solar panel installation. It's based on the net annual cost of electricity and the installation cost.
    -   The `calculate_optimal_wp` method calculates the number of solar panels in Wp that would result in the quickest payback time.
 
5.  **Creation of SolarPanelPayback class**: Created a class that encapsulates the data and methods related to a solar panel installation. This class includes the methods for calculating the payback period and the optimal number of solar panels for the quickest payback.
    
6.  **Quality Assurance**: Added thorough error handling and logging statements throughout the code to track the execution and debug any issues that might arise.
    
7.  **Dockerization**: Created a Dockerfile to containerize the application and make it easier to deploy and scale on any environment.
    
8.  **API Development**: Used FastAPI to create two API endpoints that expose the calculations as a service, allowing for easy integration with other systems.
    
9.  **Documentation**: Documented the code and created a user guide for the API, helping others understand and use the service effectively.
    

## Assumptions:

1.  The electricity grid fee is always 0.12€/kWh and is only applied when buying electricity from the grid.
    
2.  Area provider is set to **5414492999998** for both _production profile_ and _consumption profile_
    
3.  The cost of buying electricity from the grid is always 20% more than the average cost in the cost data, plus the grid fee.
    
4.  The revenue from selling electricity to the grid is always 80% of the average cost in the cost data, with no grid fee applied.
    
5.  The energy production of the solar panels is proportional to their power output in Wp.
    
6.  The energy consumption and production profiles, as well as the energy cost, will not change significantly in the future.
    
7.  The fixed installation cost is 1000€, and the variable cost per Wp is calculated based on the total installation cost and the power output in Wp of the installation.
    
8.  The API inputs are expressed in:
    
    -   Annual energy consumption in kilowatt hours (kWh)
    -   Installation power output in watt peak (Wp)
9.  Production profile data for a specific net area provider is available per Wp. The data is provided in mW/mWp per quarter-hour intervals. The production profile contains ~35,040 rows, spanning from December 31, 2017, 11:00:00 PM to December 31, 2018, 10:45:00 PM.
    
10.  The consumption profile shows the energy consumption spread over the year for every kWh of annual consumption. The data is provided in quarter-hour intervals. The consumption profile contains ~35,040 rows, covering from January 1, 2018, 12:00:00 AM to December 31, 2018, 11:45:00 PM.
    
11.  While optimizing the system for the quickest payback time, the system may suggest a lower Wp of installation than the initially installed Wp. The consumption and production profiles have been normalized to a per-unit basis (kWh or Wp) so they can be scaled based on the inputs.
    
12.  The calculations assume that all produced energy is either used or sold back to the grid, and there's no energy storage system like a battery involved.

13. The class methods `calculate_payback_time` and `calculate_optimal_wp` are implemented as asynchronous for efficiency and scalability.

14.  The `calculate_optimal_wp` function uses a simple optimization approach of varying the installed power (Wp) and checking the resulting payback period. The range used for the installed power is from the initial installed power to twice its value, with a step of 10 Wp. This approach may not find the global optimum in case the function has multiple local minima.

16. The methods of the class return the payback period in years and the optimal power in Wp as floating-point and integer values, respectively.


## Run API

### Docker (recommended)
1.  Build the Docker Image: Open a terminal or command prompt and navigate to the directory where your Dockerfile is located. Run the following command to build the Docker image:
    
    `docker build -t solar-panel-api .` 
 
2.  Run the Docker Container: 
    
    `docker run -p 8000:8000 --name my-solar-api solar-panel-api` 
    
3.  Access the API Endpoints: 

    - `http://localhost:8000/calculate_payback_time` Calculates the payback period in years for the solar panel installation.
    - `http://localhost:8000/calculate_optimal_wp` Calculates number of solar panels in Wp that would result in the quickest payback time

8.  Or check them using docs:
    
    - `http://localhost:8000/docs`

### Locally
    
1.  Ensure you have Python 3.10 installed on your system. You can check the Python version by running the following command:
    
    `python --version` 
    
2.  Open a terminal or command prompt and navigate to the project directory root.
3.  Create a virtual environment to isolate the project dependencies. You can use `venv` module to create a virtual environment. Run the following command to create a virtual environment named "venv":
  
    `python -m venv venv` 
    
4.  Activate the virtual environment. The activation command varies depending on the operating system:
    
    -   For Windows:
        
        `venv\Scripts\activate` 
        
    -   For macOS and Linux:
        
        `source venv/bin/activate` 
        
5.  Install the project dependencies. Run the following command to install the required packages:
    
    `pip install -r requirements.txt` 
    
6.  Once the dependencies are installed, you can start the API server by running the following command:
    
    `uvicorn backend.main:app --port 8000` 
    
    This command will start the API server and make it accessible at `http://localhost:8000`.
    
7.  You can now access the API endpoints:
    
    -   `http://localhost:8000/calculate_payback_time` calculates the payback period in years for the solar panel installation.
    -   `http://localhost:8000/calculate_optimal_wp` calculates the number of solar panels in Wp that would result in the quickest payback time.

8.  Or check them using docs:
    
    -   `http://localhost:8000/docs` 
