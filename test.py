#'''[GRADE]:[MAIN ERRORS], [ERROR LOCATION], [WIRE CAUGHT]. '''
lsograde = "_LURX_ TMRDX_ (LURIM) _LULIM_ _LOIC_ _PIC_ _LULIC_ (LL)"

grades = {
    "AFU": " All “fouled” up",
    "DL": "Drifted left",
    "DR": "Drifted right",
    "EG": "Eased gun (pulled throttles back to help set the hook for arrestment)",
    "F": "Fast",
    "FD": "Fouled deck",
    "H": " High",
    "LL": "Landed left",
    "LO": "Low",
    "LR": "Landed right",
    "LUL": "Lined up left",
    "LUR": "Lined up right",
    "N": "Nose",
    "NERD": "Not enough rate of descent",
    "NSU": "Not set up",
    "P": "Power",
    "SLO": "Slow",
    "TMRD": "Too much rate of descent",
    "W": "Wings",
    "LLWD": "Landed left wing down",
    "LRWD": "Landed right wing down",
    "LNF": "Landed nose",
    "PTS": "Landed 3 points",
    "BC": "Ball call (before first 1/3 of glideslope)",
    "X": "At the start (first 1/3 of glideslope)",
    "IM": "In the middle (middle 1/3 of the glideslope)",
    "IC": "In close (last 1/3 of glideslope)",
    "AR": "At the ramp",
    "TL": "To land (between AR and first wire",
    "IW": "In the wires",
    "AW": "After wires",
}

lsograde = lsograde.split(" ")
parsed_grades = {}
readout_desription = ""

for lsosubgrade in lsograde:
    readout = ''
    print(lsosubgrade)
    for grade, remarks in grades.items():
        if grade in lsosubgrade:
            # print(f"found {grade}")
            readout = readout + f"{remarks} "
    readout = readout + "\n"
    parsed_grades[lsosubgrade] = readout

print(parsed_grades)
