

LES FØRST README.md I SERVER MAPPA

Husk:
pip install pvlib[optional]
pip install metno_locationforecast
pip install ENTSOE

Start server

kjør demo


CSV filen som genereres består av følgende verdier: 

        klokkeslett
        "Total" strømforbruk oppgitt i KWh fratrekt strøm generert i solceller 
        "livingroom" strømforbruk oppgitt i KWh
        "kitchen" strømforbruk oppgitt i KWh
        "bad" strømforbruk oppgitt i KWh
        "bedroom_1" strømforbruk oppgitt i KWh
        "bedroom_2" strømforbruk oppgitt i KWh
        "bedroom_3" strømforbruk oppgitt i KWh
        "bedroom_4" strømforbruk oppgitt i KWh
        "bedroom_5" strømforbruk oppgitt i KWh
        "bedroom_6" strømforbruk oppgitt i KWh
        "costOfPower" Price per kWh oppgitt i NOK per KWh
        "solarPanels" kwH generert av solvcellepanel
        "solarSavings" Strøm generert i solcellepanel * strømpris.
        "TotalExSolar" strømforbruk oppgitt i KWh uten strøm fra solceller. 



""" Alle tilgjengelige apparater: Flytt til README?

Oppdater tilstand med pc.consumers["apparatnavn"].updateState(NewState)

ex. 
        pc.consumers["stove"].updateState(1) 
for å skru på ovn. 1 er ny tilstand. Kan være 0 for av, 22 for temperatur. 

# Stue
    "livingroomLight", "TV" , "LivingroomTemp"
# Kitchen: 
    "stove" , "dishwasher" , "coffeeMachine", "fridge", "kitchenTemp",
    "kitchenLight" 
# Bad:      
    "washingMachine", "shower", "bathroomTemp", "bathroomLight"
#Sov1:
    "light_1" , "curtains_1", "bedroom_1Temp" 
#Sov2 : 
    "light_2" , "curtains_2" , "bedroom_2Temp" 
# Sov 3:
    "light_3", "curtains_3" , "bedroom_3Temp" 
# Sov 4:
    "light_4" , "curtains_4", "bedroom_4Temp"
# Sov 5:
    "light_5" , "curtains_5", "bedroom_5Temp"
#Sov6:
    "light_6" , "curtains_6", "bedroom_6Temp" 

Merk: Alle curtains har samme CoT kode og vil justeres samtidig. 

"""