import urllib2
import json

import urllib2

from lxml import html
import requests
from bs4 import BeautifulSoup
import csv

# - First Name
# - Last Name
# - Phone Number
# - Mobile Number
# - Email Address
# - Website URL
# - City
# - State
# - Company Name

data = []
response = urllib2.urlopen("https://mortgageapi.zillow.com/getLenderDirectoryListings?partnerId=RD-CZMBMCZ&sort=Relevance&pageSize=100&page=1&fields.0=individualName&fields.1=imageURL120x120Secure&fields.2=companyName&fields.3=totalReviews&fields.4=rating&fields.5=screenName&fields.6=imageURL120x120Secure&fields.7=individualName&fields.8=employerScreenName&location=New%20York%20NY")
json_data = json.load(response)
m = 0
for i in json_data["lenders"]:
	link = i["id"]
	res = urllib2.urlopen("https://mortgageapi.zillow.com/getRegisteredLender?partnerId=RD-CZMBMCZ&fields.0=aboutMe&fields.1=address&fields.2=cellPhone&fields.3=contactLenderFormDisclaimer&fields.4=companyName&fields.5=employerScreenName&fields.6=equalHousingLogo&fields.7=faxPhone&fields.8=imageURL75x100Secure&fields.9=imageURL120x120Secure&fields.10=imageURL160x180Secure&fields.11=imageURL320x360Secure&fields.12=individualName&fields.13=languagesSpoken&fields.14=memberFDIC&fields.15=nationallyRegistered&fields.16=nmlsId&fields.17=nmlsType&fields.18=officePhone&fields.19=rating&fields.20=screenName&fields.21=stateLicenses&fields.22=title&fields.23=totalReviews&fields.24=website&lenderRef.lenderId=%s"%link)
	final_json = json.load(res)
	m = m+1
	output = {}
	if final_json["lender"].has_key("individualName"):
		for k, v in final_json["lender"]["individualName"].iteritems():
			output["Sl No"] = m
			if k =="firstName":
				output["First Name"] = v
			if k== "lastName":
				output["Last Name"] = v
				print " Las Name "
				print v
			
	if final_json["lender"].has_key("cellPhone"):
		area_code =""
		number = ""
		prefix =""
		for j,h in final_json["lender"]["cellPhone"].iteritems():
			if j =="areaCode":
				area_code=h
			if j =="number":
				number=h
			if j =="prefix":
				prefix =h
		if area_code and number and prefix is not None:
				cell_phone ="(%s)%s-%s"%(area_code,prefix,number)
				output["Mobile Number"] = cell_phone
				print cell_phone
	else:
		output["Mobile Number"] =""


	if final_json["lender"].has_key("officePhone"):
		area =""
		num = ""
		pre =""
		for j,h in final_json["lender"]["officePhone"].iteritems():
			if j =="areaCode":
				area=h
			if j =="number":
				num=h
			if j =="prefix":
				pre =h
		if area and num and pre is not None:
				office_phone ="(%s)%s-%s"%(area,pre,num)
				output["Phone Number"] = office_phone
				print "office_phone "
				print office_phone
	else:
		output["Phone Number"] = ""

	if final_json["lender"].has_key("address"):
		print " Address "
		for k,v in final_json["lender"]["address"].iteritems():
			if k =="city":
				output["City"] = v
				print " Printing City "
				print v 

			if k =="stateAbbreviation":
				output["State"] = v
	if final_json["lender"].has_key("companyName"):
		output["Company Name"] = final_json["lender"]["companyName"]

	if final_json["lender"].has_key("website"):
		output["Website Url"] = final_json["lender"]["website"]
	else:
		output["Website Url"] = ""

	data.append(output)
	print output



def WriteDictToCSV(csv_columns,dict_data):
	with open("zillow.csv", 'w') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
		writer.writeheader()
		for row in dict_data:
			print row
			writer.writerow(row)


csv_columns =['Sl No', 'First Name','Last Name','Phone Number', 'Mobile Number', 'Website Url', 'City', 'State','Company Name']

WriteDictToCSV(csv_columns,data)

