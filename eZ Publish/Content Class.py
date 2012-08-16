import sublime
import sublime_plugin
import ezsettings

class InsertAttributeCommand(sublime_plugin.WindowCommand):
    
    def run(self):

        # get the settings
        settings = ezsettings.eZSettings(self)
        data = settings.get_class_list()
        
       	# prepare data list
        self.item_list 			= []
        self.identifier_list	= []

       	# for each class group
        for class_group in data:

       		# for each content class
			for content_class in class_group['class_list']:

				# for each attribute
				for attribute in content_class['attributes']:
					
					self.item_list.append([content_class['details']['name'] + ': ' + attribute['name'], 'Type: ' + attribute['type_name'] + ' | Group: ' + class_group['details']['name'] ])
					self.identifier_list.append(attribute['identifier'])

        self.window.show_quick_panel(self.item_list, self.on_done)
    
    def on_done(self, input):
        
        # unless the input was cancelled
        if input > -1:

            # print the attribute view qui
            attribute = '{attribute_view_gui attribute=$node.data_map.' + self.identifier_list[input] + '}'
            edit = self.window.active_view().begin_edit()
            self.window.active_view().insert(edit, self.window.active_view().sel()[0].begin(), attribute)
            self.window.active_view().end_edit(edit)

            # status msg
            sublime.status_message( 'Attribute inserted' )