
import pandas as pd
import numpy as np
import pvlib
import datetime
from pvlib.pvsystem import PVSystem
from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
#from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP


latitude, longitude, tz = 63.42024, 10.40122, 'Europe/Oslo' # specify location 
start = pd.Timestamp(datetime.date.today(), tz=tz)
end = start + pd.Timedelta(days=7)
irrad_vars = ['ghi', 'dni', 'dhi']


temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
# load some module and inverter specifications
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
print (sandia_modules)
cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_'] 
cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_'] 

location = Location(latitude=63.42024, longitude=10.40122) # Bredd/lengde-grad for Trondheim

# PUTT INN VERDI FRA JENS HER
pressure = 101325.0 
apparent_elevation = 90 
solarIrradiance = pvlib.clearsky.simplified_solis(apparent_elevation, aod700=0.1,
                        precipitable_water=1.0, pressure=101325.0, dni_extra=1364.0 )
                        # Returns GHI, DNI, DHI VALUES


system = PVSystem(surface_tilt=20, surface_azimuth=180, # vinkel og vridning for panel. Sør = 180
        module_parameters=sandia_module,
        inverter_parameters=cec_inverter,
        temperature_model_parameters=temperature_model_parameters)

mc = ModelChain(system, location)

weather = pd.DataFrame([[1050, 1000, 100, 30, 5]],  #TA INN VÆRDATA HER! 
        columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed'],
        index=[pd.Timestamp('20210401 1200', tz='Europe/Oslo')])

mc.run_model(weather)
print(mc.ac)