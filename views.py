import sys
import os
sys.path.insert(1,os.getcwd()+"/Demo")

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
import pandas as pd
# import os, sys
sys.path.append("D:\SANAL\DjangoAR\mysite\Demo\\")

# from full_VARP import *
from tess import *

fileurls = []
ba_map_list = []
etd_setting_list = []
baple_list = []
cch_list = []


def loadHome(request):
	return render(request,'Demo/MLHome.html')

def Demo_page_load_cls(request):
	return render(request,'Demo/WK_SOP.html')

def Demo_Train_page_load_cls(request):
	return render(request,'Demo/Training.html')

def predict_file(request):
	cordinates = []

	cords = request.POST.get('cords')
	cords = cords.split(",")
	print("cords--->>>",cords)
	attributes = request.POST.get('attributes')
	attributes = attributes.split(",")
	print("attributes--->>>",attributes)
	values = request.POST.get('values')
	values = values.split(",")
	print("values--->>>",values)
	no_of_boxes = len(cords)/4
	print("boxes-->>",no_of_boxes)

	imagepath="C:/Users/962884/Desktop/DB-Dennis/images/W8IMY2014/W8IMY2014-page-001.jpg"
	for i in range(0,int(no_of_boxes)):
		print(i)
		boxCord = cords[i*4:i*4 + 4]
		cordinates.append(boxCord)
	print("cordinates-->>",cordinates)
	word_boxes = getWordBox(imagepath)
	feature = []
	for i in range(0,len(cordinates)):
		df_test=getText(word_boxes,cordinates[i])
		df_new=df_test.sort_values(['x1'],ascending=True)
		text = ' '.join(df_new["value"])
		feature.append(text)
		print("feature--->>",feature)
	
	saveToCSV(attributes,feature,cordinates)
	# csvData = [][]
	# for i in range(0,int(len(feature)/2)):

	#print("data frame-->>",df_test)
	return HttpResponse('success')

# def predict_file(request):
# 	attributes = []
# 	pdf =""
# 	name = ""
# 	if request.method == 'POST' and request.FILES['myfile']:
# 		try:
# 			myfile = request.FILES['myfile']
# 			print("file frm client--->>",myfile)
# 			fs = FileSystemStorage()
# 			filename = fs.save(myfile.name, myfile)
			
# 			print("file name--->>",filename)

# 			uploaded_file_url = fs.url(filename)
# 			name = os.path.basename(str(uploaded_file_url))
# 			fileurl = os.path.join(settings.MEDIA_ROOT,name)

# 			print("FILE URL--->>>",fileurl)
# 			print("uploaded_file_url--->>",uploaded_file_url)
# 			now = datetime.datetime.now()
# 			print("fun call at",now.strftime("%Y-%m-%d %H:%M"))
# 			page_no, board_members = extraction(fileurl)
# 			now = datetime.datetime.now()
# 			print("fun call at",now.strftime("%Y-%m-%d %H:%M"))
# 			print("pdf path---->>>",name)
# 			print("pageNo--->>",page_no)
# 			print("board_members--->>",board_members)



# 			# return render(request,'Demo/WK_SOP.html',{'fpage':fpage,'page_no':page_no,'board_members':board_members,'pdf':name})
# 			return render(request,'Demo/WK_SOP.html',{'page_no':page_no,'board_members':board_members,'pdf':myfile})
# 		except Exception as e:
# 			print("Exception-------------->>",e)
# 			return render(request,'Demo/WK_SOP.html',{'attributes':attributes,'pdf':name})

# 	return render(request,'Demo/WK_SOP.html',{'attributes':attributes,'pdf':name})




















































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