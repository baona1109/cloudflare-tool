# Import modules
import os
import sys
import CloudFlare

# Function: get option, input max value of option
def getOpt(maxOpt):
	try:
        	option = int(input("Option: "))
	except (ValueError):
	      	print("Invalid option")
	if (option <= maxOpt) and (option >= 0):
		return option
	else:
		return -1

# Function: print logo
def printLogo():
	os.system('clear')
	print("░█████╗░██╗░░░░░░█████╗░██╗░░░██╗██████╗░███████╗██╗░░░░░░█████╗░██████╗░███████╗")
	print("██╔══██╗██║░░░░░██╔══██╗██║░░░██║██╔══██╗██╔════╝██║░░░░░██╔══██╗██╔══██╗██╔════╝")
	print("██║░░╚═╝██║░░░░░██║░░██║██║░░░██║██║░░██║█████╗░░██║░░░░░███████║██████╔╝█████╗░░")
	print("██║░░██╗██║░░░░░██║░░██║██║░░░██║██║░░██║██╔══╝░░██║░░░░░██╔══██║██╔══██╗██╔══╝░░")
	print("╚█████╔╝███████╗╚█████╔╝╚██████╔╝██████╔╝██║░░░░░███████╗██║░░██║██║░░██║███████╗")
	print("░╚════╝░╚══════╝░╚════╝░░╚═════╝░╚═════╝░╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝")

# Function: draw table
def printTable():
	print("====================")
	return 1

# Function: print Main menu
def printMenu():
	printTable()
	print("1. List zones")
	print("2. Update record files")
	print("3. Get record information")
	print("4. Add a DNS record")
	print("5. Update a DNS record")
	print("6. Delete a DNS record")
	print("0. Exit")
	printTable()
	return 1
		
# Function: switcher for Main menu
def doOption(option,cf):
	if (option == 0):
		return 1
	printLogo()
	printTable()
	if (option == 1):
		listZones(cf)
		return 1
	if (option == 2): 
		updateRecords(cf)
		return 1
	if (option == 3):
		getRecordInfo(cf)
		return 1
	if (option == 4):
		addRecord(cf)
		return 1
	if (option == 5):
		updateRecord(cf)
		return 1
	if (option == 6):
		deleteRecord(cf)
		return 1
	print("not define yet")

# Function: list all zones of Cloudflare
def listZones(cf):
	zones = cf.zones.get(params={'per_page':50})
	count = 1
	print("Zones list:")
	for zone in zones:
		zone_name = zone['name']
		print("%d. %s" % (count,zone_name))
	return 1

# Function: get zone ID
def getZone(cf):
	listZones(cf)
	zones = cf.zones.get(params={'per_page':50})
	zone_num = getOpt(len(zones))
	zone = zones[zone_num - 1]
	zone_id = zone['id']
	return zone_id

# Function: update all records to files
def updateRecords(cf):
	zones = cf.zones.get(params={'per_page':50})
	page_number = 0
	for zone in zones:
		zone_id = zone['id']
		zone_name = zone['name']
		file_name = zone_name + ".records"
		fileHandler = open(file_name, "w")
		fileHandler.truncate(0)
		print("Exporting zone %s to %s..." % (zone_name,file_name))
		while True:
			page_number += 1
			records = cf.zones.dns_records.get(zone_id,params={'per_page':50,'page':page_number})
		
			if records:
				for record in records:
					record_id = record['id']
					record_type = record['type']
					record_name = record['name']
					record_value = record['content']
					line = record_id + "\t" + record_type + "\t" + record_name + "\t" + record_value
					fileHandler.write(line + "\n")
			else:
				break
		fileHandler.close()
	print("Done!!!")
	return 1

# Function: get record information by type and name
def getRecordInfo(cf):
	# exportRecords(cf)
	print("Search record:")
	type = input("Record type (A, MX, TXT, CNAME...): ")
	name = input("Record name (abc.com): ")
	files = [f for f in os.listdir("./") if f.endswith(".records")]
	count = 0
	for file in files:
		record_file = open(file, "r")
		for line in record_file:
			column = line.split()
			record_id = column[0]
			record_type = column[1]
			record_name = column[2]
			record_value = column[3]
			if (record_type == type) and (record_name == name):
				count += 1
				print("%d. %s\t%s\t%s\t%s\n" % (count,record_id,record_type,record_name,record_value))
		record_file.close()
	if (count == 0):
		print("Record not found!!!")

# Function: add a DNS record
def addRecord(cf):
	listZones(cf)
	zone_id = getZone(cf)
	type = input("Record type (A, MX, TXT, CNAME...): ")
	name = input("Record name (without domain.com): ")
	content = input("Content: ")
	dns_record = {'name':name, 'type':type, 'content':content}
	r = cf.zones.dns_records.post(zone_id,data=dns_record)

# Function: update a DNS record
def updateRecord(cf):
	listZones(cf)
	zone_id = getZone(cf)
	getRecordInfo(cf)
	record_id = input("Record ID: ")
	print("Update record:")
	new_type = input("New record type (A, MX, TXT, CNAME...): ")
	new_name = input("New record name (without domain.com): ")
	new_content = input("New record content: ")
	dns_record = {'name':new_name, 'type':new_type, 'content':new_content}
	r = cf.zones.dns_records.put(zone_id,record_id,data=dns_record)

# Function: delete a DNS record
def deleteRecord(cf):
	updateRecords(cf)
	listZones(cf)
	zone_id = getZone(cf)
	getRecordInfo(cf)
	record_id = input("Record ID: ")
	sure = input("Are you sure? (yes|no or y|n): ")
	if sure.lower() in ["y","yes"]:
		r = cf.zones.dns_records.delete(zone_id,record_id)		

def main():
	cf = CloudFlare.CloudFlare(profile="CloudFlare")

	option = -1
	while option != 0:
		printLogo()
		printMenu()
				
		option = -1
		while option == -1:
			option = getOpt(6)

		doOption(option,cf)
		if (option != 0):
			os.system('read -s -n 1 -p "Press Any key to continue..."')
			print()

main()
