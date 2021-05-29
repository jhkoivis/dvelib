

Id_list = ['test']

f1_len = 0 
f2_len = 0
unique_f1 = 0
f2_not_in_f1_len = 0

with open("no_buttons_03.txt") as f:		
#with open("no_buttons_03.txt") as f:		
	for line in f:
		f1_len +=  1
		#print line
		if len(line) < 2: continue
		printline = False

		#print line
		line2 = line.split('>')
		if len(line2) < 2:
			continue
		line2 = line2[1].strip()
		#print line2

		for id in Id_list:
			if id in line2:
				printline = True
				
		if not printline: 
			Id_list.append(line2)
			
for id in Id_list:
	print id
#print(Id_list)
print("\n\n***********************************\n\n")

unique_f1 = len(Id_list)


unique_f2_list = []
all_f2_list = []


with open("volume_up_03.txt") as f:		
#with open("no_buttons_03.txt") as f:		
	for line in f:
		f2_len += 1
		#print line
		if len(line) < 2: continue
		printline = True

		#print line
		line2 = line.split('>')
		if len(line2) < 2:
			continue
		line2 = line2[1].strip()
		#print line2
		all_f2_list.append(line2)

		for id in Id_list:
			if id in line2:
				printline = False
				
		if printline: 
			print line2
			f2_not_in_f1_len += 1
			if not line2 in unique_f2_list:
				unique_f2_list.append(line2)
	
print(f1_len, f2_len, unique_f1, f2_not_in_f1_len)

for line in unique_f2_list:
	count = 0
	for line2 in all_f2_list:
		if line == line2: count += 1
	print count, line

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