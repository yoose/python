"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import sys
import datetime
import gspread
import numpy as np
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

json_key = 'metrics-745a25165853.json'
scope = ['https://spreadsheets.google.com/feeds']

#credentials = ServiceAccountCredentials.from_json_keyfile_name(google_api_key_file, scope)

# Setup the Sheets API
# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

gc = gspread.authorize(creds)

# Call the Sheets API
# SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SPREADSHEET_ID = '1QrucvzEoBD3Elb_KvzcyWhOODViixe1zqLeiFcRmSUg'
#RANGE_NAME = 'Class Data!A2:E'
# the sheet to read from, might want to make this an input in the future
RANGE_NAME = 'Metrics-Candidates'
# the sheet to write to, might want to make this an input in the future
WRITE_NAME = 'Kyle-Test'
#RANGE_NAME = 'To do'
now = datetime.datetime.now()

## using arguments from the command line
#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

sheet = gc.open_by_key(SPREADSHEET_ID)
worksheet = sheet.worksheet(RANGE_NAME)
writeSheet = sheet.worksheet(WRITE_NAME)
allData = worksheet.get_all_values()
headers = allData.pop(0)
headers_metrics = ['Position', 'Contacted', 'Replies', 'Interested', 'Phone Screens', 'Onsites', 'Offers']
#tmp = [x.encode('utf-8') for x in headers]
# convert all of the entries from unicode type to string

# this section is needed for python 2, but not python 3
# python 2 reads in the cells as unicde, python 3 reads it in as text
#headers = map(lambda x: x.encode('utf-8'), headers)
#for index, k in enumerate(allData):
#    allData[index] = map(lambda j: j.encode('utf-8'), k)
# cant remember what this part is for right now
    #for index, j in enumerate(k):
    #    print(headers[index].lower().find('date'))
        #if headers[index].lower().find('date') != -1:
        #    k[index] = datetime.datetime.strptime(j.encode('utf-8'), '%m/%d/%Y')

# get list of roles from this week
def getCandidateRows(intervalType, offset):
    candidateRows = []
    outreachIndex = headers.index('Date of Outreach')
    if intervalType == 'w':
        #outreachInterval = now.strftime('%W')
        # W here uses Monday as the first day of the week, U uses Sunday
        strIntType = '%W'
    elif intervalType == 'm':
        #outreachInterval = now.month
        strIntType = '%m'
    elif intervalType == 'y':
        strIntType = '%Y'
    outreachInterval = int(now.strftime(strIntType)) - offset
    for index, k in enumerate(allData):
        strDateOutreach = allData[index][outreachIndex]
        if intervalType == 'all':
            candidateRows.append(index)
        else:
            # here we want to try and convert the cell contents into a datetime object
            try:
                # we should also check for differnt date formats like %m/%d/%y
                dateOutreach = datetime.datetime.strptime(strDateOutreach, '%m/%d/%Y')
                candidateInterval = dateOutreach.strftime(strIntType)
                if int(candidateInterval) == outreachInterval:
                    candidateRows.append(index)
            except ValueError:
                # pass if the entry isn't a date
                pass
    candidateRows = np.array(candidateRows)
    return candidateRows

def getPositions(candidateIndex):
    positions = []
    posCol = headers.index('Position')
    for num in candidateIndex:
        curPosition = allData[num][posCol]
        # we only want unique positions so check to see if its already recorded
        # If it doesnt exist, then it will throw an exception so that is where we will append to the array
        try:
            boolExists = positions.index(curPosition)
            pass
        except ValueError:
            # need to get this to append a list so extend can be used later to create the array with the job titles
            positions.append(curPosition)
    return positions

# get the counts for the different Metrics
def getCounts(candidates, candidateRows, positions):
    # create a 2D array of zeroes to populate, we want zeroes for the sheet so
    # we don't get errors later. the 7 is the number of columns we need
    # Contacted, Replied, Replied with Interest, Phone Screen, Onsite, Offers, Accepted
    #counts = [[0] * 7 for i in range(positions.__len__())]
    counts = np.zeros((positions.__len__()+1,7), dtype = int)
    idxTotals = positions.__len__()
    idxPosition = headers.index('Position')
    idxReply = headers.index('Date of Reply')
    idxInterest = headers.index('Reply')
    idxPhone = headers.index('Date of Phone Screen')
    idxInterview = headers.index('Date of Interview')
    idxOffer = headers.index('Offer Date')
    counts[idxTotals][0] = candidateRows.__len__()
    for k in candidateRows:
        posRow = positions.index(candidates[k][idxPosition])
        counts[posRow][0] += 1
        # check to see if there was a reply
        try:
            dateReply = datetime.datetime.strptime(candidates[k][idxReply], '%m/%d/%Y')
            counts[posRow][1] += 1
            counts[idxTotals][1] += 1
        except ValueError:
            pass
        # check to see if there was interest
        if candidates[k][idxInterest].lower() == "interested":
            counts[posRow][2] += 1
            counts[idxTotals][2] += 1
        # check to see if there is a phone Screen
        try:
            dateReply = datetime.datetime.strptime(candidates[k][idxPhone], '%m/%d/%Y')
            counts[posRow][3] += 1
            counts[idxTotals][3] += 1
        except ValueError:
            pass
        # check to see if there was an onsite visit
        try:
            dateReply = datetime.datetime.strptime(candidates[k][idxInterview], '%m/%d/%Y')
            counts[posRow][4] += 1
            counts[idxTotals][4] += 1
        except ValueError:
            pass
        # check to see if there was an offer made
        try:
            dateReply = datetime.datetime.strptime(candidates[k][idxOffer], '%m/%d/%Y')
            counts[posRow][5] += 1
            counts[idxTotals][5] += 1
        except ValueError:
            pass

    return counts

# call the function to get row numbers for the candidates of interest
candidateIndices = getCandidateRows('y',0)
# get positions (unique) of the candidates of interest
positions = getPositions(candidateIndices)
# get the counts for each of the positions
counts = getCounts(allData, candidateIndices, positions)
positions.append('Totals')
print(positions)
print(counts)

# Output to sheets

batch_update_values_request_body = {
    # How the input data should be interpreted.
    'value_input_option': 'RAW',  # We want the data as is here

    # The new values to apply to the spreadsheet.
    'data': [
      {
        # Output in one column
        "range": 'Kyle-Test!A1',
        "majorDimension": 'COLUMNS',
        "values": [positions]
      },
      {
        # numpy array needs to be converted to a list otherwise its not JSON serializable
        "range": 'Kyle-Test!B1',
        "values": counts.tolist()
        #"values": [[1,2,3], [4,5,6], [7,8,9]]
      }
    ],  # TODO: Update placeholder value.

    # TODO: Add desired entries to the request body.
}

request = service.spreadsheets().values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_update_values_request_body)
response = request.execute()
#pprint(response)

#writeSheet.update_cell('A1:A3', [1,2,3])

#test = allData[0][5].encode('utf-8')
#dt = datetime.datetime.strptime(test, '%m/%d/%Y')


# result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
#                                              range=RANGE_NAME).execute()
# values = result.get('values', [])
# headers = values[0]
# data = values[1::]
# if not values:
#     print('No data found.')
# else:
#     data = data
    #print('Name, Major:')
    #for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
        #print('%s, %s' % (row[0], row[2]))
        #print(values[0][9])
