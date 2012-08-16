import sublime
import json
import os
from urllib2 import urlopen
import time

class eZSettings:

	def __init__(self, sublime):

        # specify the name of the file we're looking for
		self.settings_file 		= '.sublime_settings.json'
		self.cache_class_file	= '.content_class.cache'

		self.sublime 		= sublime 

		self.get_path_location()

	def get_path_location(self):

		# for each open folder
		for folder in self.sublime.window.folders():
	        
			# walk the path
			for root, dirs, names in os.walk(folder):

				# if the settings file was found
				if self.settings_file in names:
	                
					# save location of settings file
					self.settings_location = root
					return self.settings_location

		# if the settings location was not found
		sublime.status_message( 'Unable to locate a settings file specifying the path to the eZ installation.' )
		return False

	def get_file_location(self):
		return os.path.join(self.settings_location, self.settings_file)

	def get_class_list(self):

		cached_data = self.get_class_list_from_cache()

		# if we did not get the settings data from the cache
		if not cached_data:

			# get the settings data
			settings_data = self.get()

			# if we got the settings data
			if settings_data:
				
				# get the url of the content class list
				url = settings_data['ez_url']

				if(url == False or url == ''):
					
					self.sublime.status_message( 'Please specify the URL to your eZ installation in your settings file' )
					return False

				else:

					# get content classes from url
					class_list_data = urlopen(url + 'nmcontent/classlist')

					# cache content classes for later use
					file(self.cache_path, 'w').close()
					cache_f = open(self.cache_path, 'w')
	                cache_f.write(class_list_data.read())
	                cache_f.close()

	                cached_data = self.get_class_list_from_cache()


		return cached_data
		
	def get_class_list_from_cache(self):

		# check if a cached file exists
		self.cache_path = os.path.join(self.settings_location, self.cache_class_file)
		class_list_data = False
		if os.path.exists(self.cache_path):

			# make sure that the cached file is not too old (older than a day)
			cache_timestamp = os.path.getmtime(self.cache_path)
			now = time.time()
			now -= 60*60*24

			# if the cache file has expired
			if now > cache_timestamp:

				# delete cache file
				os.remove(self.cache_path)

			else:
				# get file from cache
				class_list_data = open(self.cache_path)
				return json.load(class_list_data)
		
		return False

	def get(self):
		
		# get the url of the content class list
		settings_contents = open(self.get_file_location())
		return json.load(settings_contents)
	