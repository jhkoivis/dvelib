

Id_list = [	"217FFC", 
			"131726C",
			"1E0162A",
        "14034A2",
        "2202262",
        "E01008",
        "C00402",
        "1601422",
        "1A0600A",
        "2C1302A",
        "12173BE",
        "2803008",
        "2300492",
        "2510000",
        "3000042",
        "3200408",
        "2616CFC",
        "3A04004",
        "3C01428",
        "381526C",
        "2006428",
        "1017FFC",
        "4000002",
        "3E0004A",
        "3600008",
        "4200002",
        "4900002",
        "A10408",
        "1B500000",
        "4600002"]

with open("volume_up_03.txt") as f:		
#with open("no_buttons_03.txt") as f:		
	for line in f:
		#print line
		if len(line) < 2: continue
		printline = True

		for id in Id_list:
			if id in line:
				printline = False
				
		if printline: print line
	

"""
0x217FFC &&
        0x131726C &&
        canId != 0x1E0162A &&
        canId != 0x14034A2 &&
        canId != 0x2202262 &&
        canId != 0xE01008 &&
        canId != 0xC00402 &&
        canId != 0x1601422 &&
        canId != 0x1A0600A &&
        canId != 0x2C1302A &&
        canId != 0x12173BE &&
        canId != 0x2803008 &&
        canId != 0x2300492 &&
        canId != 0x2510000 &&
        canId != 0x3000042 &&
        canId != 0x3200408 &&
        canId != 0x2616CFC &&
        canId != 0x3A04004 &&
        canId != 0x3C01428 &&
        canId != 0x381526C &&
        canId != 0x2006428 &&
        canId != 0x1017FFC &&
        canId != 0x4000002 &&
        canId != 0x3E0004A &&
        canId != 0x3600008 &&
        canId != 0x4200002 &&
        canId != 0x4900002 &&
        canId != 0xA10408 &&
        canId != 0x1B500000 &&
        canId != 0x4600002)



"""