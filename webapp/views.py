from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth,logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta,date
import socket
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
import urllib
import random
import time
import requests
import os 

import tensorflow as tf, sys

from webapp.models import ImageRecognization
from . import recognize_image


def image_recognization(request):
    """
    Image Recognization
    """
    image_recognization_result = {}
    image_file = ""
    latest_result = ImageRecognization.objects.filter().order_by("-created_date")[:5]

    if request.method == 'POST':
        image = request.FILES['input_file']
        strore_image = ImageRecognization.objects.create(image_file=image)

        image_file = str(strore_image.image_file)
        current_directory = os.getcwd()
        stoted_image_file = "%s/%s" %(current_directory,image_file)

        image_recognization_result = recognize_image.run_inference_on_image(stoted_image_file)
        strore_image.result=image_recognization_result
        strore_image.save()

    return render_to_response('googleSearch/image_recognization.html',{"image_recognization_result":image_recognization_result,"image_file":image_file,"latest_result":latest_result},context_instance=RequestContext(request))