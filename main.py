from flask import Flask
from os import name
import rpy2.robjects as robjects
import removeSilence.soundprocess as sp
import createPieChart as cpc
import sys

app = Flask(__name__)

@app.route("/")
def index():
    return "Congratulations, it's a web app!"


@app.route("/")
def runApp (args):
  if len(args) != 1:
    sys.stderr.write('Usage: runApp.py <path to wav file>\n')
    sys.exit(1)

  nameWav = args[0]
  # Defining the R script and loading the instance in Python
  r = robjects.r
  r['source']('meeting2csv.R')
  print('hej')
  #Remove silence from audio 
  silenceRemovedPath = sp.soundProcessMain(f'{nameWav}')

  # Loading the functions we have defined in R.
  meeting2csv_function_r = robjects.globalenv['meeting2csv']
  #Invoking the R function and getting the result
  # extract features from sound to a CSV file
  namecsv = meeting2csv_function_r(silenceRemovedPath)
  namecsv=''.join(namecsv)
  
  #predict gender and print out a pie chart of the result
  cpc.mainPieChart(namecsv)
 
#runApplication('Poddelipodd.wav')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

