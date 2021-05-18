# prototype for bookingsystemet. 
# Koden virker helt fint, men kan forbedres med tanke på error-meldinger. 
# Men min ESP32 kan ikke motta signaler av en eller annen grunn, så om problemet vedvarer så vil det være forgjeves å sende Error-meldinger uansett.

from booking_functions import *

signal_key = 9940
cot_token = "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI1MjI4In0.K58Zp9kRjEWJdlIkNRhD2yrV5EB6DcbDRnHsIVRspps"

df = csvToDf("booking.csv")
updateTime(df)

prevBookingVal = round(getVal(signal_key, cot_token))

while(True):
    curBookingVal = round(getVal(signal_key, cot_token)) # sjekker booking-signalet fra CoT
    #print(len(str(curBookingVal)))

    if(curBookingVal != prevBookingVal and len(str(curBookingVal)) == 9): # sjekker om den har mottatt nytt signal
        booking(df, curBookingVal) # booker rom
        prevBookingVal = curBookingVal

    updateTime(df) # oppdaterer tidspunktene i df-en
    saveDf(df, "booking.csv") # lagrer data i csv-fil

    print(df)
    time.sleep(0.5)