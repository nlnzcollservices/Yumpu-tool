import os
import re
import wget
import shutil
import requests
import urllib
import time
import PySimpleGUI as sg
from pathlib import Path
from datetime import datetime as dt
from bs4 import BeautifulSoup as bs
from rosetta_sip_factory.sip_builder import build_sip
from description_maker import make_description
import random
import filetype
from PIL import Image


def is_image_predominantly_white(image_path, threshold=0.95):
    """Check if the given image is predominantly white."""
    try:
        with Image.open(image_path) as img:
            # Convert image to RGB to ensure consistent handling of pixel values
            img = img.convert('RGB')
            pixels = list(img.getdata())
            num_white_pixels = sum(1 for pixel in pixels if sum(pixel) / 3 > 255 * threshold)
            total_pixels = img.size[0] * img.size[1]
            return num_white_pixels / total_pixels > threshold
    except Exception as e:
        print(f"Error checking if image is predominantly white: {e}")
        return False  # Assume the image is not predominantly white to avoid halting the process

    


def import_variables_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        exec(content, globals())

def my_gui(values = None):
	"""
	This function running form in separate window and collect values
	Returns:
		values(dict) - dictionary of form values
	"""
	value_list  = ["PeriodicIE", "OneOffIE"]

	import_variables_from_file("api_file.txt")
	sg.Print("#"*30)
	sg.Print('name = ',  name)
	sg.Print('apikey = ', apikey)
	sg.Print('out_folder = ', out_folder)
	sg.Print('sip_out_folder = ', sip_out_folder)
	sg.Print("#"*30)
	sg.Print()
	if not os.path.isdir(out_folder):
		os.mkdir(out_folder)
	if not os.path.isdir(sip_out_folder):
		os.mkdir(sip_out_folder)


	if not values:
		initial_alma_mms ='mms_id'
		initial_dc = 'Title'
		initial_url = r'https://www.yumpu.com/en/document/read/68644538/march-2024-bay-of-plenty-business-news'
		initial_output = str(out_folder)
		initial_output_sip = str(sip_out_folder)
		initial_rights = '200'
		initial_entity = "PeriodicIE"
		initial_enum_a = ""
		initial_enum_b= ""
		initial_enum_c = ""
		initial_chron_i = dt.now().strftime("%Y")
		initial_chron_j = ""
		initial_chron_k = ""
		initial_pol = 'po_line'
		initial_api=apikey

	else:
		initial_alma_mms =values['mms_id']
		initial_dc = values['dc_title']
		initial_url = values['url']
		initial_output = values["output_folder"]
		initial_output_sip = values["output_sip_folder"]
		initial_entity = values["entity_type"]
		initial_rights = values['access']
		initial_enum_a = values["enum_a"]
		initial_enum_b = values["enum_b"]
		initial_enum_c = values["enum_c"]
		initial_chron_i = values["chron_i"]
		initial_chron_j = values["chron_j"]
		initial_chron_k = values["chron_k"]
		initial_pol = values['po_line']
		initial_api=values['api_key']





	form = sg.FlexForm('Simple SIP form')
	schemes = ["BlueMono","Tan","BluePurple","LightBrown","SystemDefaultForReal","LightBrown18","LightBrown16","LightBrown15","LightBrown14","LightBrown12","LightBrown11","LightBrown10","LightBrown8","LightBrown7","LightBrown6","LightBrown9","LightBrown5","Kayak","Purple","DarkGreen1","DarkGreen2","DarkGreen3","TealMono","Python","LightGrey3","LightGrey6","SendyBeach","BluePurple","DarkTeal7","LightGreen2",'DarkBrown6','Purple','DarkGreen4','DarkTeal7']
	all_schemes = ['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 'DarkPurple6', 'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 'Green', 'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Python', 'Reddit', 'Reds', 'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']
	all_schemes =["LightBlue2",'LightGrey2',"GrayGrayGray","Default1"]
	all_schemes = ["HotDogStand","SandyBeach","DarkTeal"]
	all_schemes = themes
	# sg.theme("BlueMono")
	# sg.theme("Tan")
	# sg.theme("BluePurple")
	# sg.theme("LightBrown")
	# sg.theme("SystemDefaultForReal")
	# sg.theme("LightBrown18")
	# sg.theme("LightBrown16")
	# sg.theme("LightBrown15")
	# sg.theme("LightBrown14")
	# sg.theme("LightBrown12")
	# sg.theme("LightBrown11")
	# sg.theme("LightBrown10")
	# sg.theme("LightBrown8")
	# sg.theme("LightBrown7")
	#sg.theme("LightBrown6")
	#sg.theme("LightBrown9")
	#sg.theme("LightBrown5")
	#sg.theme("Kayak")
	# sg.theme("Purple")
	# sg.theme("DarkGreen1")
	# sg.theme("DarkGreen2")
	# sg.theme("DarkGreen3")
	# sg.theme("TealMono")
	# sg.theme("Python")
	#sg.theme("LightGrey3")
	# sg.theme("LightGrey6")
	#sg.theme("SendyBeach")
	r = random.choice(all_schemes)
	sg.theme(r)


	

	layout = [

			[sg.Text('Insert YUMPU information')],

			[sg.Text('Alma MMS', size=(17, 1)), sg.InputText(initial_alma_mms,key='mms_id',size=(35, 1))],
			[sg.Text('Title', size=(17, 1)), sg.InputText(initial_dc,key='dc_title', size=(35, 1))],
			[sg.Checkbox('Download?', default=False,key='if_download', font = ('Helvetica', 15, 'bold italic'))],
			[sg.Text('YUMPU URL', size=(17, 1)), sg.InputText(initial_url,key='url',size=(35, 1))],
			[sg.Text('Files output folder', size=(17, 1)), sg.InputText(initial_output,key = "output_folder", size=(50, 1))],
			[sg.Checkbox('Make SIP?', default=False,key='if_sip',font = ('Helvetica', 15, 'bold italic'))],
			[sg.Text('Output SIP folder', size=(17, 1)), sg.InputText(initial_output_sip,key = "output_sip_folder", size=(50, 1))],
			[sg.Text('Entity type',size=(17, 1)), sg.Listbox(values=value_list, size=(30, 1), default_values=initial_entity, key='entity_type')],
			[sg.Text('Policy ID', size=(17, 1)), sg.InputText(initial_rights,key='access',size=(5, 1))],
			[sg.Text('enumerationA (volume)', size=(10, 2)), sg.InputText(initial_enum_a,key="enum_a",size=(5, 1)),sg.Text('enumerationB (number)', size=(10, 2)), sg.InputText(initial_enum_b,key="enum_b",size=(5, 1)),sg.Text('enumerationC (issue)', size=(10, 2)), sg.InputText(initial_enum_c,key="enum_c",size=(5, 1))],
			[sg.Text('chronology I (year)', size=(10, 2)), sg.InputText(initial_chron_i,key="chron_i",size=(5, 1)),sg.Text('chronology J (month)', size=(10, 2)), sg.InputText(initial_chron_j,key="chron_j",size=(5, 1)),sg.Text('chronology K (day)', size=(10, 2)), sg.InputText(initial_chron_k,key="chron_k",size=(5, 1))],
			[sg.Checkbox('Make item?', default=False,key='if_item',font = ('Helvetica', 15, 'bold italic'))],
			[sg.Text('PO_line', size=(17, 1)), sg.InputText(initial_pol,key='po_line',size=(35, 1))],
			[sg.Text('Your PROD API key', size=(17, 1)), sg.InputText(initial_api,key='api_key',size=(35, 1))],
			[sg.Checkbox('Try in SANDBOX?',default=False,key='if_sb',font = ('Helvetica', 15, 'bold italic'))],
			[sg.Button("Run!")]

			]

	window =sg.Window(f'YUMPU tool {name} ("{r}" theme)', layout, default_element_size=(35, 2))#,background_color='#ACBAAB')
	event,values=window.read()

	return values,window,event
	




class YumpuTool():
	def __init__(self):
		self.ind = 0
		pass
	def get_item(self, mms_id, holding_id, item_pid):
		"""Retrieves item  record.
		Parameters:
			mms_id(str) - Alma bib record objectIdentifier
			holding_id(str) - holding id
			item_pid(str) - item pid
		Returns:
			r.text(str) - item_data in xml format
		"""

		url = r"https://api-ap.hosted.exlibrisgroup.com/almaws/v1/bibs/{}/holdings/{}/items/{}".format(mms_id, holding_id, item_pid)
		parameters = {"apikey": self.api_key}
		r = requests.get(url, params = parameters, verify= False)
		return r.text

	def update_item(self, mms_id, holding_id, item_pid, item_data):
		"""Updates item with generating description
		Parameters:
			mms_id(str) - Alma bib record objectIdentifier
			holding_id(str) - holding id
			item_pid(str) - item pid
			item_data(str) - item data in xml format
		Returns:
			description(str) - description
			status_code(int) - response code - 200 if success, 404 if opposite

		"""

		url = r"https://api-ap.hosted.exlibrisgroup.com/almaws/v1/bibs/{}/holdings/{}/items/{}".format(mms_id, holding_id, item_pid)
		headers = {'content-type': 'application/xml'}
		parameters = {"apikey": self.api_key,"generate_description":True}
		r = requests.put(url, data = item_data.encode("utf-8"), headers=headers, params = parameters, verify= False)
		description= re.findall(r"<description>(.*?)</description>", r.text)[0]

		return description, r.status_code

	def create_item_by_po_line(self, xml_record_data):

		"""
		Creates item.
		Parameters:
			po_line(str) - Alma POL
			xml_record_data(str) - new item in xml format
			options(dict) - optional parameters for request
		Returns:
			self.xml_response_data
			self.status_code
		Notes:
			holding_id required in the  xml data
		"""

		headers = {'content-type': 'application/xml'}
		url = r"https://api-ap.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines/{}/items".format(self.po_line)
		#spi_sb = "l8xx5d24fa2ed92248dfb913722b8e3fb2d6"
		xml_record_data = xml_record_data.replace("\\", "")
		parameters = {"apikey": self.api_key, "generate_description":True}
		r = requests.post(url, params = parameters, headers=headers, data=xml_record_data.encode("utf-8"),verify= False)
		print(r.text)
		try:
			item_pid= re.findall(r"<pid>(.*?)</pid>", r.text)[0]
			return item_pid
		except:
			return None
	def get_holding(self):

		url = r"https://api-ap.hosted.exlibrisgroup.com/almaws/v1/bibs/{}/holdings".format(self.mms_id)
		params = {"apikey": self.api_key}
		r = requests.get(url, params = params,verify= False)
		print(r.url)
		try:
			holding_id= re.findall(r"<holding_id>(.*?)</holding_id>", r.text)[self.ind]
			print(holding_id)
			return holding_id
		except Exception as e:
			print(str(e))
			return None

	def make_item(self, pub_name, mms_id, po_line,  enum_a=None, enum_b=None, enum_c=None, chron_i=None, chron_j=None, chron_k=None,  api_key= None):
		"""

		Main function for making Alma item record with existing template and parameters, writes down report and prints item_id
		Parameters:
			pub_name (str) - magazine name
			enum_a (str) - enumeration a
			enum_b (str) - enumeration b
			enum_c (str) - enumeration c
			chron_i (str) - chronology i
			chron_j (str) - chronology j
			chron_k (str) - chronology k
		Returns:
			None


		"""
		print("#"*50)
		print(pub_name)
		self.mms_id = mms_id
		self.po_line = po_line
		self.api_key = api_key
		chron_i_stat = "<chronology_i></chronology_i>"
		chron_j_stat = "<chronology_j></chronology_j>"
		chron_k_stat = "<chronology_k></chronology_k>"
		enum_a_stat = "<enumeration_a></enumeration_a>"
		enum_b_stat = "<enumeration_b></enumeration_b>"
		enum_c_stat = "<enumeration_c></enumeration_c>"
		polstring = "<po_line>{}</po_line>".format(po_line)

		if chron_i:
			chron_i_stat = "<chronology_i>{}</chronology_i>".format( chron_i )
		if chron_j:
			chron_j_stat = "<chronology_j>{}</chronology_j>".format( chron_j )
		if chron_k:
			chron_k_stat = "<chronology_k>{}</chronology_k>".format( chron_k )
		if enum_a:
			enum_a_stat = "<enumeration_a>{}</enumeration_a>".format( enum_a )
		if enum_b:
			enum_b_stat = "<enumeration_b>{}</enumeration_b>".format( enum_b)
		if  enum_c:
			enum_c_stat = "<enumeration_c>{}</enumeration_c>".format( enum_c)
		time_substitute_statement = "<creation_date>{}</creation_date>".format(str(dt.now().strftime( '%Y-%m-%d')))
		receiving_stat = "<arrival_date>{}</arrival_date>".format(str(dt.now().strftime( '%Y-%m-%d')))
		holding_id = self.get_holding()
		holding_stat = "<holding_id>{}</holding_id>".format(holding_id)
		item_data = """<item>
							  <holding_data>
							       <holding_id></holding_id>
							  </holding_data>
							  <item_data>
							    <pid></pid>
							    <creation_date></creation_date>
							    <physical_material_type desc="Digital File">KEYS</physical_material_type>
							    <policy>HERITAGE</policy>
							    <po_line></po_line>
							    <arrival_date></arrival_date>
							    <enumeration_a></enumeration_a>
							    <enumeration_b></enumeration_b>
							    <enumeration_c></enumeration_c>
								<chronology_i></chronology_i>
							    <chronology_j></chronology_j>
							    <chronology_k></chronology_k>
							    <receiving_operator>korotesv_API</receiving_operator>
								<library desc="Alexander Turnbull Library">ATL</library>
							    <location desc="Alexander Turnbull Library">ATL.DA</location>
							    <requested>false</requested>
							  </item_data>
							</item>
						"""
		print(item_data)
		item_data = item_data.replace("<creation_date></creation_date>", time_substitute_statement)
		item_data = item_data.replace("<po_line></po_line>", polstring )
		item_data = item_data.replace("<enumeration_a></enumeration_a>", enum_a_stat )
		item_data = item_data.replace("<enumeration_b></enumeration_b>", enum_b_stat )
		item_data = item_data.replace("<enumeration_c></enumeration_c>", enum_c_stat )
		item_data = item_data.replace("<chronology_i></chronology_i>", chron_i_stat )
		item_data = item_data.replace("<chronology_j></chronology_j>", chron_j_stat )
		item_data = item_data.replace("<chronology_k></chronology_k>", chron_k_stat )
		item_data = item_data.replace("<holding_id></holding_id>", holding_stat )
		print(item_data)

		sg.Print("Creating item")
		
		item_pid = self.create_item_by_po_line(item_data)
		if item_pid:
			sg.Print("Item created ",item_pid)
		else:
			self.ind+=1
			sg.Print("Could not create item")
			holding_id = self.get_holding()
			print(holding_id)
			holding_stat_new = "<holding_id>{}</holding_id>".format(holding_id)
			print(item_data)
			item_data = item_data.replace(holding_stat, holding_stat_new )
			print(item_data)

			sg.Print("Creating item")
			
			item_pid = self.create_item_by_po_line(item_data)
			
			item_data = self.get_item(mms_id,holding_id, item_pid)
			description,status_code = self.update_item(mms_id,holding_id,item_pid,item_data)
			
			if str(status_code).startswith("2"):
				sg.Print("Item updated with description ",description)



# # Volume = dcterms:bibliographicCitation
# # Issue = dcterms:issued
# # Number = dcterms:accrualPeriodicity
# # Year = dc:date
# # Month = dcterms:available
# # Day = dc:coverage




	def make_SIP(self, pub_name, mms_id, policy="200", output_folder=None,  sip_output_folder =None,  enum_a=None, enum_b=None, enum_c=None, chron_i=None, chron_j=None, chron_k=None ):

			"""Method is used for making SIPs from description information

			Returns:
				bool  - True, if built, False otherwise
			"""
			description = make_description(enum_a, enum_b, enum_c, chron_i, chron_j, chron_k)
			self.output_folder= str(output_folder)
			current_dir = os.getcwd()
			os.chdir(self.output_folder)
			self.sip_output_folder = os.path.join(sip_output_folder, (pub_name + " " + description).replace("(","").replace(")","").replace(" ","_").replace(",","").replace("\\","_").replace("/","_"))
			sg.Print("Making sips")
			sg.Print(sip_output_folder)
			try:
				build_sip(
									ie_dmd_dict=[{"dc:date":chron_i, "dcterms:available":chron_j, "dcterms:issued":enum_c, "dc:coverage":chron_k,"dcterms:bibliographicCitation":enum_a,  "dc:title":pub_name,"dcterms:accrualPeriodicity":enum_b, "dcterms:bibliographicCitation":enum_a}],
									pres_master_dir=".",
									generalIECharacteristics=[{"IEEntityType":"PeriodicIE","UserDefinedA":"yumpu"}],
									objectIdentifier= [{"objectIdentifierType":"ALMAMMS", "objectIdentifierValue":mms_id}],
									accessRightsPolicy=[{"policyId":policy}],
									input_dir=".",
									digital_original=True,
									sip_title=pub_name+"_"+description,
									output_dir=self.sip_output_folder,
									#exclude_file_char = ['fileOriginalPath','fileSizeBytes', 'fileModificationDate','fileCreationDate']
								)
				sg.Print('Done in', sip_output_folder)
			except Exception as e:
				sg.Print(str(e))
			os.chdir(current_dir)

	def download(self, my_link, output_folder):
		"""This function downloads YUMPU images from link"""

		self.output_folder = output_folder
		end_flag = False
		size_dictionary = {}
		r = requests.get(my_link, verify=False)
		doc_id = my_link.split("/")[-2]
		base_url = f"https://img.yumpu.com/{doc_id}/1/1200x1645/{doc_id}.jpg?quality=200"

		maximum_pages = 0
		for i in range(500):
			if end_flag:
			    break

			try:
				my_url_page = f"/{i+1}/"
				my_link = base_url.replace("/1/", my_url_page)
				formatted_page_number = str(i+1).zfill(3)
				new_filename = f"{doc_id}_page_{formatted_page_number}.jpg"
				full_path = os.path.join(output_folder, new_filename)

				# Download the image
				wget.download(my_link, out=full_path)
				r = requests.get(my_link, verify=False)	    

				# Check if the image is predominantly white, indicating end of content
				if is_image_predominantly_white(full_path):
				    os.remove(full_path)  # Remove the image if it's predominantly white
				    end_flag = True
				    break
				else:
				    maximum_pages += 1
				    size_dictionary[new_filename] = r.headers["Content-Length"]
				    print(r.headers)

			except Exception as e:
				print(str(e))
		my_filenames = os.listdir(output_folder)
		file_folder = str(output_folder)
		if len(my_filenames)<maximum_pages:
			print("!"*20)
			print("Attention! Number of pages of collected is ",len(my_filenames), ", but expected - ", maximum_pages)
			print("Clean the download folder and run script again.")
			print("!"*20)
		print(my_filenames)
		print(size_dictionary)
		for image in my_filenames:
				fileinfo = filetype.guess(os.path.join(file_folder, image))# new
				extens = fileinfo.extension#new
				print(os.path.getsize(os.path.join(file_folder, image)))
				if os.path.getsize(os.path.join(file_folder, image)) == int(size_dictionary[image]):
					pass
				else:
					quit()


def main():

	my_link = r"https://issuu.com/issuu-ncc/docs/annual_plan_consultation_doc_-_f.a_-_march_22?fr=sZTg1Mjc0MTI4OA"
	sip_output_folder = None
	output_folder = None
	window = None
	

	values = None
	while True:
			try:
				if window:
					window.close()
				if not os.path.exists("api_file.txt"):
					sg.Print()
					sg.Print("Cannot find api_file.txt in the same directory. Please place it there and restart the app.")
					sg.Print("You can also create api_file.txt and insert the following info.")
					sg.Print("#############################################################################")
					sg.Print('name = "Yourname"')
					sg.Print('apikey = "your digit key"')
					sg.Print('out_folder = r"C:\\Users\\Username\\ympu_test"')
					sg.Print('sip_out_folder = r"C:\\Users\\Username\\yumpu_SIP"')
					sg.Print('themes = ["LightBlue2", "LightGrey2", "GrayGrayGray", "Default1"]')
					sg.Print("#############################################################################")
					sg.Print('All information about api keys here https://developers.exlibrisgroup.com/manage/keys.')
					sg.Print('Add and delete your color schemes, use this link https://www.geeksforgeeks.org/themes-in-pysimplegui.')
					time.sleep(30)  # Pause for 30 seconds
					break
				values,window,event= my_gui(values = values)
				print(values)
				if event == sg.WIN_CLOSED:
						break
				if event in (sg.WIN_CLOSED, 'Quit'):
					break

				title = values["dc_title"]
				mms_id = values["mms_id"].rstrip(" ")
				api_key = values["api_key"].rstrip(" ")
				po_line = values["po_line"].rstrip(" ")
				chron_i = values["chron_i"].rstrip(" ")
				chron_j = values["chron_j"].rstrip(" ")
				chron_k = values["chron_k"].rstrip(" ")
				enum_a = values["enum_a"].rstrip(" ")
				enum_b = values["enum_b"].rstrip(" ")
				enum_c = values["enum_c"].rstrip(" ")
				access =values['access'].rstrip(" ")
				url = values["url"].rstrip(" ")
				output_folder = values["output_folder"].rstrip(" ")
				sip_output_folder = values["output_sip_folder"].rstrip(" ")
				if_download = values["if_download"]
				if_sip = values["if_sip"]
				if_item = values["if_item"]
				if_sb = values["if_sb"]


				if not os.path.isdir(output_folder):
					os.mkdir(output_folder)
				if not os.path.isdir(sip_output_folder):
					os.mkdir(sip_output_folder)				
				sg.Print("Alma MMS: ", mms_id)
				if not mms_id.endswith("2836"):
					sg.Print("Enter valid mms_id" ,text_color = "red")
					window.close()
				sg.Print("Alma PO line: ", po_line)
				if po_line =="po_line" or po_line =="":
					sg.Print("Enter po_line number",text_color = "red")
					window.close()
				sg.Print("Year: ", chron_i)
				if chron_i == "":
					sg.Print("Enter the year",text_color = "red")
					window.close()
				if len(chron_i)!=4:
					sg.Print("Year is not correct",text_color = "red")
					window.close()
				sg.Print("Title: ", title)
				if title == "Title" or title == "":
					sg.Print("Enter sip title",text_color = "red")
					window.close()
				sg.Print()
				if if_item:
					if if_sb:
						api_key = "l8xx5d24fa2ed92248dfb913722b8e3fb2d6"
						sg.Print("SANDBOX API key",text_color = "darkgreen")
						sg.Print(api_key,text_color = "darkgreen")



				yt = YumpuTool()
				if if_download:
					if len(os.listdir(output_folder))!=0:
						for fl in os.listdir(output_folder):
							os.remove(os.path.join(output_folder, fl))
					yt.download(url, output_folder)
				description = make_description(enum_a, enum_b, enum_c, chron_i, chron_j, chron_k)
				if description.startswith("(") and description.endswith(")"):
					description = description.lstrip("(").rstrip(")")
				sip_detailed_output_folder = os.path.join(sip_output_folder, (title + " " + description).replace("(","").replace(")","").replace(" ","_").replace(",",""))
	
				if if_sip:
					if os.path.isdir(sip_detailed_output_folder):
						shutil.rmtree(sip_detailed_output_folder)
					yt.make_SIP( pub_name = title, output_folder= output_folder, sip_output_folder = sip_output_folder, mms_id=mms_id, policy=access, chron_i=chron_i,chron_j=chron_j, chron_k=chron_k, enum_a = enum_a, enum_b = enum_b,enum_c = enum_c)
				if if_item:
					yt.make_item(pub_name =title, mms_id=mms_id, po_line=po_line,chron_i=chron_i, chron_j=chron_j, chron_k=chron_k, enum_a = enum_a, enum_b = enum_b,enum_c = enum_c,api_key = api_key)
			except Exception as e:
				sg.Print(str(e))
				window.close()
	window.close()




if __name__ == "__main__":			
	main()
