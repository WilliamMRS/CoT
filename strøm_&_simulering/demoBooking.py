import demo_functions as defunc


# VIKTIG!!!
            # KUN BOOK MED 10 MINUTTERS INTERVAL
# VIKTIG!!!


def bookAllTheRooms() :
    # alle booker badet fra 07:30 til 09:00, 15 minutter hver.
    defunc.bookRoom(0, "07:30", "07:45", 1)
    defunc.bookRoom(0, "07:45", "08:00", 2)
    defunc.bookRoom(0, "08:00", "08:15", 3)
    defunc.bookRoom(0, "08:15", "08:30", 4)
    defunc.bookRoom(0, "08:30", "08:45", 5)
    defunc.bookRoom(0, "08:30", "08:45", 6)

    # folk booker kjøkkenet for en halvtime etter de har vært på badet hver. Det er da alltid bare 2 stk der samtidig. Fra 07:45 til 09:30
    defunc.bookRoom(2, "07:45", "08:15", 1)
    defunc.bookRoom(2, "08:00", "08:30", 2)
    defunc.bookRoom(2, "08:15", "08:45", 3)
    defunc.bookRoom(2, "08:30", "09:00", 4)
    defunc.bookRoom(2, "08:45", "09:15", 5)
    defunc.bookRoom(2, "09:00", "09:30", 6)

    # folk booker kjøkkenet for 15 minutter hver, to og to til lunsj. 12:00 til 13:00
    defunc.bookRoom(2, "12:00", "12:15", 1)
    defunc.bookRoom(2, "12:00", "12:15", 2)
    defunc.bookRoom(2, "12:15", "12:30", 3)
    defunc.bookRoom(2, "12:15", "12:30", 4)
    defunc.bookRoom(2, "12:30", "13:00", 5)
    defunc.bookRoom(2, "12:30", "13:00", 6)

    # 2 går på toalettet. 13:15 til 13:30
    defunc.bookRoom(0, "13:15", "13:30", 1)
    defunc.bookRoom(0, "13:30", "13:45", 2)
    # 4 går på toalettet fra 14:30 til 14:45
    defunc.bookRoom(0, "14:30", "14:35", 3)
    defunc.bookRoom(0, "14:35", "14:40", 4)
    defunc.bookRoom(0, "14:40", "14:45", 5)
    defunc.bookRoom(0, "14:45", "14:50", 6)

    # booker kjøkkenet 45 minutter hver, tre og tre. 16:30 til 17:15 og 17:15 til 18:00
    defunc.bookRoom(2, "16:30", "17:15", 1)
    defunc.bookRoom(2, "16:30", "17:15", 2)
    defunc.bookRoom(2, "16:30", "17:15", 3)
    defunc.bookRoom(2, "17:15", "18:00", 4)
    defunc.bookRoom(2, "17:15", "18:00", 5)
    defunc.bookRoom(2, "17:15", "18:00", 6)

    # 1,2,4 og 5 bruker stua fra 18:00 til 22:00
    defunc.bookRoom(1, "18:00", "22:00", 1)
    defunc.bookRoom(1, "18:00", "22:00", 2)
    defunc.bookRoom(1, "18:00", "22:00", 3)
    defunc.bookRoom(1, "18:00", "22:00", 4)

    # alle booker toalettet for 10 minutter før de legger seg, en og en. Mellom 22:00 og 23:00
    defunc.bookRoom(0, "22:00", "22:10", 1)
    defunc.bookRoom(0, "22:10", "22:20", 2)
    defunc.bookRoom(0, "22:20", "22:30", 3)
    defunc.bookRoom(0, "22:30", "22:40", 4)
    defunc.bookRoom(0, "22:40", "22:50", 5)
    defunc.bookRoom(0, "22:50", "23:00", 6)


#bookAllTheRooms() # Books rooms according to the specified pattern in demoBooking.py file 