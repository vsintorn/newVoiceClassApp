from flask import Flask, render_template, request, redirect
from os import name
import rpy2.robjects as robjects
import removeSilence.soundprocess as sp
import createPieChart as cpc
import sys
import os

#from werkzeug import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'\uploads'


#@app.route("/")
#def index():
 #   return "Congratulations, it's a web app!"

def classify():
  nameWav = 'recording.wav'
  # Defining the R script and loading the instance in Python
  r = robjects.r
  r['source']('meeting2csv.R')
  
  #Remove silence from audio 
  silenceRemovedPath = sp.soundProcessMain(f'{nameWav}')

  # Loading the functions we have defined in R.
  meeting2csv_function_r = robjects.globalenv['meeting2csv']
  #Invoking the R function and getting the result
  # extract features from sound to a CSV file
  namecsv = meeting2csv_function_r(silenceRemovedPath)
  namecsv=''.join(namecsv)
  
  #predict gender and print out a pie chart of the result
  data = cpc.mainPieChart(namecsv)
  return render_template('classify.html', values = data)
 


@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/classify', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      if f.filename.split('.')[-1] == 'wav':
         f.save('recording.wav')
      else: return redirect('/')
      nameWav = 'recording.wav'
      # Defining the R script and loading the instance in Python
      r = robjects.r
      r['source']('meeting2csv.R')
      
      #Remove silence from audio 
      silenceRemovedPath = sp.soundProcessMain(f'{nameWav}')

      # Loading the functions we have defined in R.
      meeting2csv_function_r = robjects.globalenv['meeting2csv']
      #Invoking the R function and getting the result
      # extract features from sound to a CSV file
      namecsv = meeting2csv_function_r(silenceRemovedPath)
      namecsv=''.join(namecsv)
      
      #predict gender and print out a pie chart of the result
      data = cpc.mainPieChart(namecsv)
      return render_template('classify.html', values = data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

