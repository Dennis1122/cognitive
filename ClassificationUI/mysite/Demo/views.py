import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")

import json
from django.http import HttpResponse
from time import sleep
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .pageBod import page_bod
import os
from pathlib import Path
from shutil import copyfile
import datetime
from django.views import View
from django.template.loader import render_to_string
import time


# import os, sys
sys.path.append("D:\SANAL\DjangoAR\mysite\Demo\\")

# from full_VARP import *
# from NOB_DEMO import *
# from pageBod import *
# from Final_Code_VARP import *

fileurls = []
ba_map_list = []
etd_setting_list = []
baple_list = []
cch_list = []
fileurl = ''
myfile = ''
nob_dict = []
jurisdiction = []
filename = ''

def loadHome(request):
	return render(request,'Demo/MLHome.html')

def Demo_page_load_cls(request):
	return render(request,'Demo/WK_SOP.html')

def predict_file(request):
	attributes = []
	pdf =""
	name = ""
	if request.method == 'POST' and request.FILES['myfile']:
		try:
			global myfile
			myfile = request.FILES['myfile']
			print("file frm client--->>",myfile)
			fs = FileSystemStorage()
			global filename
			filename = fs.save(myfile.name, myfile)

			print("file name--->>",filename)

			uploaded_file_url = fs.url(filename)
			name = os.path.basename(str(uploaded_file_url))
			global fileurl
			fileurl = os.path.join(settings.MEDIA_ROOT,name)

			print("FILE URL--->>>",fileurl)
			print("uploaded_file_url--->>",uploaded_file_url)
			now = datetime.datetime.now()
			print("fun call at",now.strftime("%Y-%m-%d %H:%M"))
			# page_no, board_members = extraction(fileurl)
			# page_list, bod_list = page_bod(fileurl)
			now = datetime.datetime.now()
			print("fun call at",now.strftime("%Y-%m-%d %H:%M"))
			print("pdf path---->>>",name)

			print("no exception")
			return render(request,'Demo/WK_SOP.html',{'pdf':myfile})
		except Exception as e:
			print("Exception-------------->>",e)
			return render(request,'Demo/WK_SOP.html',{'attributes':attributes,'pdf':name})

	return render(request,'Demo/WK_SOP.html',{'attributes':attributes,'pdf':name})

def predict_file1(request):
	# time.sleep(5)
	global pdf, page_num
	# pdf,page_content,page_num=read_cordinates1(fileurl)
	global nob_dict
	outpdf_path = 'C:/Users/denn/Desktop/POCs/Redaction-UI/mysite/Demo/static/Demo/pdfs/Redaction/'+filename+'_masked.pdf'
	out_pdf="Redaction/"+filename+"_masked.pdf"
	cords = [(59.919, 702.32, 112.381, 716.231),(58.919, 679.763, 141.076, 694.114),(59.919, 550.575, 122.345, 564.486),(59.919, 527.232, 173.493, 541.143),(536.408, 631.313, 551.324, 645.224),(518.237, 596.295, 533.153, 610.206),(59.919, 503.889, 99.139, 517.8),(477.656, 59.743, 560.284, 71.348),(410.776, 462.057, 443.968, 475.968),(466.804, 462.057, 486.092, 475.968),(508.825, 462.057, 556.022, 475.968),(410.776, 415.365, 429.971, 429.276),(452.797, 415.365, 541.992, 429.276)]
	# mask_pdf(fileurl,outpdf_path,cords)
	# nob_dict = {'party1', 'SOFTWARE SUPPLIER NAME','party2','THE REGENTS OF THE UNIVERSITY OF CALIFORNIA'}
	return render(request,'Demo/WK_SOP.html',{'nob_dict':nob_dict,'pdf':myfile,'out_pdf':out_pdf,'predit1':'true'})


def Classification_page_load_cls(request):

	return render(request,'Demo/doc_class.html')


















































"""

def upload_folder(request):
	if request.method == 'POST' and request.FILES['myfile']:
		try:

			global fileurls
			fs = FileSystemStorage()
			for afile in request.FILES.getlist('myfile'):

				filename = fs.save(afile.name, afile)
				uploaded_file_url = fs.url(filename)
				name = os.path.basename(str(uploaded_file_url))
				fileurls.append(name)

			print(fileurls)



			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
			#return render(request,'Demo/EmailClassification.html',{'ba_map':result[0],'etd_setting_list':result[1],'baple_list':result[3],'cch_list':result[2],'files':fileurls})
		except Exception as e:
			return render(request, 'Demo/EmailClassification.html',{'accuracy':'','err_msg':e})

	return render(request, 'Demo/EmailClassification.html',{'accuracy':''})


def all(request):
	global fileurls, ba_map_list, etd_setting_list, baple_list, cch_list
	if request.method == 'POST':
		try:
			for eachfile in fileurls:
				fileurl = os.path.join(settings.MEDIA_ROOT,eachfile)
				result = EMLPrediction().prediction(fileurl)
				if(result[4]==1):
					ba_map_list.append(eachfile)
				if(result[4]==2):
					etd_setting_list.append(eachfile)
				if(result[4]==3):
					baple_list.append(eachfile)
				if(result[4]==4):
					cch_list.append(eachfile)


			for eachfile in ba_map_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"BA MAP/"+eachfile))
			for eachfile in etd_setting_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"ETD Setting/"+eachfile))
			for eachfile in baple_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"BAPLE/"+eachfile))
			for eachfile in cch_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"CCH/"+eachfile))

			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
		except Exception as e:
			print(e)
			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
	return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})

def ba_map(request):
	global fileurls
	global ba_map_list
	global etd_setting_list
	global baple_list
	global cch_list
	if request.method == 'POST':
		try:
			for eachfile in fileurls:
				fileurl = os.path.join(settings.MEDIA_ROOT,eachfile)
				result = EMLPrediction().prediction(fileurl)
				print(type(baple_list))
				if(result[4]==1):
					ba_map_list.append(eachfile)

			for eachfile in ba_map_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"BA MAP/"+eachfile))

			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
		except Exception as e:
			print(e)
			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
	return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})



def etd_setting(request):
	global fileurls
	global ba_map_list
	global etd_setting_list
	global baple_list
	global cch_list
	if request.method == 'POST':
		try:
			for eachfile in fileurls:
				fileurl = os.path.join(settings.MEDIA_ROOT,eachfile)
				result = EMLPrediction().prediction(fileurl)
				print(type(baple_list))
				if(result[4]==2):
					etd_setting_list.append(eachfile)

			for eachfile in etd_setting_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"ETD Setting/"+eachfile))


			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
		except Exception as e:
			print(e)
			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
	return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})


def baple(request):
	global fileurls
	global ba_map_list
	global etd_setting_list
	global baple_list
	global cch_list
	if request.method == 'POST':
		try:
			for eachfile in fileurls:
				fileurl = os.path.join(settings.MEDIA_ROOT,eachfile)
				result = EMLPrediction().prediction(fileurl)
				print(type(baple_list))
				if(result[4]==3):
					baple_list.append(eachfile)

			for eachfile in baple_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"BAPLE/"+eachfile))


			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
		except Exception as e:
			print(e)
			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
	return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})

def cch(request):
	global fileurls
	global ba_map_list
	global etd_setting_list
	global baple_list
	global cch_list
	if request.method == 'POST':
		try:
			for eachfile in fileurls:
				fileurl = os.path.join(settings.MEDIA_ROOT,eachfile)
				result = EMLPrediction().prediction(fileurl)
				print(type(baple_list))
				if(result[4]==4):
					cch_list.append(eachfile)


			for eachfile in cch_list:
				copyfile(os.path.join(settings.MEDIA_ROOT,eachfile), os.path.join(settings.MEDIA_ROOT,"CCH/"+eachfile))

			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
		except Exception as e:
			print(e)
			return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})
	return render(request,'Demo/EmailClassification.html',{'ba_map':ba_map_list,'etd_setting_list':etd_setting_list,'baple_list':baple_list,'cch_list':cch_list,'files':fileurls})

"""
