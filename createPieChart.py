import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from numpy import genfromtxt
import urllib.request
import json
import os
import ssl
import csv

#from sklearn.metrics import confusion_matrix
import pandas as pd


def CreatePieChart(arrayML):

    maleStats = arrayML.count('male')
    femaleStats = arrayML.count('female')

    data = [maleStats, femaleStats]
    gender = ['Male '+str(round(maleStats*100/len(arrayML)))+'%', 'Female '+str(round(femaleStats*100/len(arrayML)))+'%']

    plt.figure(figsize =(10, 7))
    plt.pie(data, labels = gender)
    print(data)
    plt.show()


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here

def runML(fileName, modelURL):
    df = pd.read_csv(fileName, delimiter=',', dtype = str)
    dataval = df.to_json(orient='records')
    data = json.loads(dataval)

    #print (dataval)
    data = {"data" : data}


    body = str.encode(json.dumps(data))

    url = modelURL #newreal
    api_key = '' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
      
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))


    
    result = result.decode("utf-8").replace('"',"")
    result = result.split(',')
    resultarray = []
    for res in result:

        resultarray.append(res.split(':'))

    del resultarray[0][0]
    flatlist = list(matplotlib.cbook.flatten(resultarray))
    newlist=[]
    i=1
    for gender in flatlist:
        s = ''.join(ch for ch in gender if ch.isalnum())
        #print(str(i) + " " + s)
        i = i+1

        newlist.append(s)
    
    return(newlist)






def mainPieChart(fileName):
  arrayML = runML(fileName, 'http://57ce19b0-2b8d-4687-a39a-8279cd57273f.northeurope.azurecontainer.io/score') #10 seconds no silence
 
  CreatePieChart(arrayML)

#testModels('Testdata\Sigge Eklund Jag har känt mycket avund.wavconverted.wavNon-Silenced.csv', 'Testdata\Sigge Eklund Jag har känt mycket avund.wavconverted.wavNon-Silenced_facit.csv')
#mainPieChart('61 Det gäller ett saldo redigerad.wavconverted.wavNon-Silenced.csv')