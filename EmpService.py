'''
	This is a simple service class which accepts http requests and return data based on the request in JSON format.
	
	Services -
		1./emp - return all rows of the csv file as a JSON array.
		2./emp/column/{csv column name} It return all values of a csv column.
			E.g./emp/column/City will return all Cities like "Seattle, Fairfax, ALDIE, Chantilly, Herndon"
		3./emp/search/{search string} - It returns all rows of the csv file in a json array, where each row contains given string.
		4./emp/search/{csv column name}/{searchString} It works same like above service but the search is performed only in the given column name instead of on all columns.

	Sample Reqeust URL	
	 	http://localhost:50012/emp/search/Position/Analyst

	 Follwoing are expected to run this servies.
	 	1. Python 2.7.10 or later
	 	2. Port shoudl be accessible on which the services are run. Here i am using the port "50012" you can update your port here.
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import simplejson as json
import csv
searchDict = {}
allDicts = []
SocketServer.TCPServer.allow_reuse_address
class MockServices(BaseHTTPRequestHandler):
	print 'Service started'
	reader = csv.DictReader(open('EmployeeData.csv'))	
	key = 0
	for row in reader:
		arrSearchValues = []	
		col1 = row["EmpId"]
		col2 = row["FirstName"]	
		col3 = row["LastName"]
		col4 = row["Position"]		
		col5 = row["Manager"]
		col6 = row["Street"]
		col7 = row["City"]
		col8 = row["State"]
		col9 = row["Zip"]
		col10 = row["Country"]
		arrSearchValues.append(col1)
		arrSearchValues.append(col2)
		arrSearchValues.append(col3)	
		arrSearchValues.append(col4)
		arrSearchValues.append(col5)
		arrSearchValues.append(col6)
		arrSearchValues.append(col7)
		arrSearchValues.append(col8)
		arrSearchValues.append(col9)
		arrSearchValues.append(col10)
		allValues = ''.join(arrSearchValues)
		# All values is the main string in which search is performed.
		# If you want the serach operation should be perforced on only few columnns then you can update the stirng with only those columns.
		searchDict[allValues] = row
		allDicts.append(row);
	# This function return all the values for a column name in the csv
	def getDetailsOfRecord(self, cellName):
		responsesTring = (list({d[cellName] for d in searchDict.values()}))
		return self.wfile.write(json.dumps(responsesTring))
	# This function Search in a column and return entire row of columns which met filtered in search
	def searchStringInColumn(self,searchColumn,searchStr,inputDicts):
		resultlist = [d    for d in inputDicts     if d[searchColumn] == searchStr]
		responsesTring = (json.dumps(resultlist))
		return self.wfile.write(responsesTring)
	# This function search given string in each row of the csv and return filtered rows
	def searchString(self,searchStr,inputDicts):
		matches = {x for x in inputDicts.keys() if searchStr in x}
		returnDicts = []
		for tempStr in matches:
			returnDicts.append(searchDict[tempStr])
		responsesTring = (json.dumps(returnDicts))
		return self.wfile.write(responsesTring)
	# This function return all rows of the csv
	def do_GET(self):		
		print(self.path)
		requestPath = self.path.split('/')		
		print(requestPath)
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		if len(requestPath) > 0:
			serviceName = requestPath[1]
			if serviceName=="emp" :
				if len(requestPath) > 2:
					operationName = requestPath[2]
					print operationName
					if operationName=="search":
						if len(requestPath) > 4:
							# search data in the column name
							searchColumnName = requestPath[4]
							return self.searchStringInColumn(requestPath[3],requestPath[4],allDicts)
						else:
							return self.searchString(requestPath[3],searchDict)
					elif operationName=="column":
						return self.getDetailsOfRecord(requestPath[3])
					else:
						responsesTring = (json.dumps(searchDict))
						return self.wfile.write(responsesTring)
				else:
					responsesTring = (json.dumps(allDicts))
					return self.wfile.write(responsesTring)

Handler = MockServices
httpd = SocketServer.TCPServer(("", 50012), Handler)
httpd.serve_forever()