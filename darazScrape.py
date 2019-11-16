#import Libraries
from selenium import webdriver  # for chrome open library for scraping
import time #time library for sleep
from selenium.webdriver.common.keys import Keys  # chrome keys libraries for input forms
from selenium.webdriver.common.action_chains import ActionChains #performing action libraries in chrome like Enter ESC
from bs4 import BeautifulSoup, NavigableString #Libraries to parse HTML  

#open chrome browser
driver = webdriver.Chrome()

#list for all products URL save
list1=[]


#create CSV for Saving Data of mobile phones with sentiment polarity
data=open('DarazDataComplete.csv','a',encoding="utf-8")

#writing header for the FILE
data.write("ProductNumber,BrandName,BrandTitle,URL,AverageRating,Review\n")



#First URL of DARAZ where mobile numbers list
URL = 'https://www.daraz.pk/smartphones/'
for i in range(1,84): #loop for total number of pages in DARAZ mobile phones
 
	URL = 'https://www.daraz.pk/smartphones/?page='+str(i) # URL to open one by one
	driver.get(URL)  					#open that URL for finding the URLS of Every Product on that page
	print(URL) 				#printing the URL
	src=driver.page_source   # Getting The META DATA of that page
	soup=BeautifulSoup(src,'html.parser')  #parge that meta data in to HTML
	time.sleep(2)						#Sleep for 2 seconds
	urll=soup.findAll('div',{'data-qa-locator':'product-item'})  #finding the URLS of products
	for i in urll:
		i=i.find('a')   #finding the Tag a in that div
		print(i['href']) 
		list1.append(i['href'])    # now url is in the HREF
	


driver.quit() #Quit the first driver for Memory Cleaning

#list for reviews rating

urllist=list1 #now all the URLS i have in the list
countproduct=0 	#for priting the current product which is parsing at that time

driver = webdriver.Chrome()			#open the driver again


for i in urllist:			#parse one by one that product URL
	countproduct=countproduct+1		#increment the current product one by one
	print('Product '+str(countproduct))	#print the current product
	i=i.replace('\n','')  #removing the end line for open link clearly
	URL = 'https:'+str(i) 	#apped https: in the URL
	driver.get(URL)			#same as above defined
	print(URL)				#same as above defined
	src=driver.page_source	#same as above defined
	soup=BeautifulSoup(src,'html.parser') #same as above defined
	time.sleep(2) #same as above defined
	
	
	#pdp-mod-product-badge-title
	brandtitle=''					#For BrandTitle Scrape
	#checking Brand Name
	if(soup.find('span',{'class':'pdp-mod-product-badge-title'})):		#Checking the Brand Title Exist or not
		brandtitle=soup.find('span',{'class':'pdp-mod-product-badge-title'})	#Getting the Brand Title 
		brandtitle=brandtitle.get_text()			#Now Parse the HTML and Get the text in the html tag of that span 
		brandtitle=brandtitle.strip()				#strip for that gettext remove extra spaces 
		brandtitle=brandtitle.replace(',','')		#Replace , . \n or any extra thing. 
		brandtitle=brandtitle.replace('.','')
		brandtitle=brandtitle.replace('\n','')
		brandtitle=brandtitle.replace('\t','')
		brandtitle=brandtitle.replace('"','')
		print(brandtitle)					#same as above defined

	
	
	brandname=''				#same as above defined now for brandname 
	#checking Brand Name
	if(soup.find('div',{'class':'pdp-product-brand'})):			#same as above defined
		brandname=soup.find('div',{'class':'pdp-product-brand'})	#same as above defined
		brandname=brandname.find('a')					#same as above defined
		brandname=brandname.get_text()					#same as above defined
		brandname=brandname.strip()						#same as above defined
		print(brandname)								#same as above defined
	
	averagerating=''							#same as above defined for aveagerating
	#checking product have rating or not
	if(soup.find('span',{'class':'score-average'})):			#same as above defined
		averagerating=soup.find('span',{'class':'score-average'})			#same as above defined
		averagerating=averagerating.get_text()			#same as above defined
		averagerating=averagerating.strip()			#same as above defined
		print(averagerating)						#same as above defined
		
	if(soup.find('div',{'class':'mod-reviews'})):  		#reviews 	#same as above defined
		reviewstag=soup.find('div',{'class':'mod-reviews'})			#same as above defined
		reviews=reviewstag.findAll('div',{'class':'content'})			#same as above defined
		for ii in reviews:			#same as above defined as parsing review for first page of all review if exist
			ii=ii.get_text()			#same as above defined
			ii=ii.replace('.','')		#same as above defined
			ii=ii.replace('\n','')			#same as above defined
			ii=ii.replace('\t','')		#same as above defined
			ii=ii.replace('\n\n','')		#same as above defined
			ii=ii.replace(',','')			#same as above defined
			ii=ii.replace('\r','')				#same as above defined
			ii=ii.strip()				#same as above defined
			data.write('Product '+str(countproduct)+","+brandname+","+brandtitle+","+URL+","+averagerating+","+ str(ii)) #writing in the CSV
			data.write('\n')			#writing in the CSV end line
			
	else:							#no reviews
		data.write('Product '+str(countproduct)+","+brandname+","+brandtitle+","+URL+","+averagerating+","+ str('')) #writing in the CSV no found reviews
		data.write('\n')			#writing in the CSV
		
driver.quit()			#same as above defined