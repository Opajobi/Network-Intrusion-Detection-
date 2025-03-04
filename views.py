from django.shortcuts import render
from django.http import HttpResponse
import joblib
import numpy as np
from datetime import datetime

# Create your views here.

def landingpage(request):
    return render(request, 'landingpage.html')

def home(request):
    return render(request, 'home.html')

def mitigation(request):
    return render(request, 'mitigation.html')

def result(request):
    # Initialize cls to None
    cls = None

    try:
        # Attempt to load the classifier
        cls = joblib.load('C:\\Users\\hp\\Desktop\\Web app\AttackIoT\\New_EnsembleModel.joblib')
    except Exception as e:
        # Handle any exceptions that occur during loading
        return HttpResponse(f"Error loading model: {e}")

    if cls is None:
        return HttpResponse("Model could not be loaded.")

    # Get user input from the form
    lis = [
        request.GET['SrcBytes'],
        request.GET['DstBytes'],
        request.GET['SrcLoad'],
        request.GET['DstLoad'],
        request.GET['SIntPkt'],
        request.GET['DIntPkt'],
        request.GET['SIntPktAct'],
        request.GET['DIntPktAct'],
        request.GET['SrcJitter'],
        request.GET['DstJitter'],
        request.GET['sMinPktSz'],
        request.GET['dMinPktSz'],
        request.GET['Dur'],
        request.GET['TotPkts'],
        request.GET['Load'],
        request.GET['Loss'],
        request.GET['pLoss'],
        request.GET['pSrcLoss'],
        request.GET['pDstLoss'],
        request.GET['Rate'],
        request.GET['Packet_num'],
        request.GET['Temp'],
        request.GET['SpO2'],
        request.GET['Pulse_Rate'],
        request.GET['SYS'],
        request.GET['DIA'],
        request.GET['Heart_rate'],
        request.GET['Resp_Rate'],
        request.GET['ST']
    ]

    # Convert the list of input data to a format suitable for the model
    input_data = [float(i) for i in lis]
    input_data = [input_data]  # Model expects a 2D array

    # Make the prediction
    prediction = cls.predict(input_data)

    # Get the predicted label (numerical)
    predicted_label_num = prediction[0]

    # Log the result in a file with a timestamp
    with open('prediction_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} - Prediction: {predicted_label_num}\n")

    # Render the result page with the prediction
    return render(request, 'result.html', {'predicted_label': predicted_label_num})

def view_logs(request):
    # Read the log file and pass the content to the template
    with open('prediction_log.txt', 'r') as log_file:
        log_content = log_file.readlines()

    return render(request, 'views_logs.html', {'log_content': log_content})
