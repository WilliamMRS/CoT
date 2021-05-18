import pandas as pd
import numpy as np
import pvlib
import datetime
from pvlib import irradiance
from pvlib import location
from pvlib.pvsystem import PVSystem
#from pvlib.location import Location
from pvlib.modelchain import ModelChain
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
import weatherData


latitude, longitude, tz = 63.42024, 10.40122, 'Europe/Oslo' # specify location 
start = pd.Timestamp(datetime.date.today(), tz=tz)
end = start + pd.Timedelta(days=1)
irrad_vars = ['ghi', 'dni', 'dhi']

# Create location object to store lat, lon, timezone
#location = Location(latitude=63.42024, longitude=10.40122) # Bredd/lengde-grad for Trondheim
site = location.Location(latitude, longitude, tz=tz)

temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
# Bestemmer hvilke moduler og invertere vi ønsker å modelere. 
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_'] 
cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_'] 


# Calculate clear-sky GHI and transpose to plane of array
def get_irradiance(site_location, date, tilt, surface_azimuth):
    # Creates one day's worth of 10 min intervals
    times = pd.date_range(date, freq='10min', periods=6*24,
                          tz=site_location.tz)
    # Generate clearsky data using the Ineichen model, which is the default
    # The get_clearsky method returns a dataframe with values for GHI, DNI,
    # and DHI

    clearsky = site_location.get_clearsky(times)
    # Get solar azimuth and zenith to pass to the transposition function
    solar_position = site_location.get_solarposition(times=times)
    # Use the get_total_irradiance function to transpose the GHI to POA
    POA_irradiance = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=surface_azimuth,
        dni=clearsky['dni'],
        ghi=clearsky['ghi'],
        dhi=clearsky['dhi'],
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'])
    # Return DataFrame with only GHI and POA
    return pd.DataFrame({'GHI': clearsky['ghi'],
                         'DNI' : clearsky['dni'],
                         'DHI' : clearsky['dhi'],
                         'POA': POA_irradiance['poa_global']})

system = PVSystem(surface_tilt=20, surface_azimuth=180, # vinkel og vridning for panel. Sør = 180
        module_parameters = sandia_module,
        inverter_parameters = cec_inverter,
        temperature_model_parameters = temperature_model_parameters)


###____ Kjør ____ ### 

def getIndexIntoDay():
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day)
    diff = now - start
    seconds_in_day = 24 * 60 * 60
    return int((144 / seconds_in_day) * diff.seconds) # converts seconds to intervals of 144 (10 min) and throws away decimal.

def solarPanelPower(date, index):
    """ 
    Returns solarPower generationn in Watt
     """   

    irradiance = get_irradiance(site, date, 20, 180) # irradiance i Trondheim, i dag
    wattPerSquareMeter = irradiance["POA"][index]
    solarPanelArrayPower = wattPerSquareMeter * 150 * 0.19 # times square meters * solar panel efficiency.
    cloudCover = weatherData.Get_data_now().variables["cloud_area_fraction"]
    cloudCover = float(str(cloudCover).split()[1][:-1])/100
    solarPanelArrayPower = solarPanelArrayPower * (1 - cloudCover) # power * 1 - cloud coverage
    return solarPanelArrayPower
    
#power = solarPanelPower('14-05-2021', getIndexIntoDay())
#print(power)



"""
weatherList = [irradiance["GHI"], irradiance["DHI"], irradiance["DNI"], 30, 5]

#print(weatherList)

weather = pd.DataFrame([[irradiance["GHI"], irradiance["DHI"], irradiance["DNI"], 30, 5]],
                         columns=['ghi', 'dni', 'dhi', 'temp_air', 'wind_speed'],
                         index=[pd.Timestamp('20210401 1200', tz='Europe/Oslo')])

print(weather)

#MÅ FIKSES MER PÅ. Må få tatt innn riktige verdier i weather DF og ikke arrays.
mc = ModelChain(system, site)

mc.run_model(weather)
print(mc.ac)
"""