import sublime
import sublime_plugin
import ezsettings
import os

class CreateOverrideCommand(sublime_plugin.WindowCommand):

    def run(self):
        
        # instantiate settings
        self.settings = ezsettings.eZSettings(self)

        self.tpl_map = {'node/view/full.tpl': 'full', 'node/view/line.tpl': 'line'}

        # if we know the location of the settings file
        if self.settings.settings_location:

            # prepare a list of the templates we can override
            self.tpl_list = []
            
            for key, value in self.tpl_map.items():
                self.tpl_list.append(key)

            self.window.show_quick_panel(self.tpl_list, self.on_selected_tpl)

    def on_selected_tpl(self, input):
        
        # if a template was selected
        if input > -1:

            self.selected_tpl   = self.tpl_list[input]
            self.tpl_index      = input

            self.class_list = []
            self.class_map = {}

            # get the class list
            self.data = self.settings.get_class_list()

            i = 0

            # for each class group
            for class_group in self.data:

                # for each content class
                for content_class in class_group['class_list']:

                    self.class_list.append(content_class['details']['name'] + ' (' + content_class['details']['identifier'] + ')')
                    self.class_map[i] = content_class['details']['identifier']
                    i += 1

            self.window.show_quick_panel(self.class_list, self.on_selected_class)

    def on_selected_class(self, input):

        # if a class was selected
        if input > -1:

            self.selected_class = self.class_list[input]
            self.class_index    = input

            design_path = os.path.join(self.settings.settings_location, 'design')

            self.design_dir_list = []

            for design_dir in os.listdir(design_path):
                
                if design_dir.startswith('.'):
                    pass
                else:
                    self.design_dir_list.append(design_dir)

            # if there is more than one design folder
            if len(self.design_dir_list) > 1:

                self.window.show_quick_panel(self.design_dir_list, self.on_selected_design)
            else:

                self.on_selected_design(0)

    def on_selected_design(self, input):

        # if a design was selected
        if input > -1:

            self.selected_design    = self.design_dir_list[input] 

            override_file       = os.path.join(self.settings.settings_location, 'settings/override.ini.append.php')
            new_tpl_name        = self.tpl_map[self.selected_tpl] + "/" + self.class_map[self.class_index] + ".tpl"
            new_tpl_base_path   = os.path.join(self.settings.settings_location, 'design', self.selected_design, 'override/templates', self.tpl_map[self.selected_tpl])
            new_tpl_path        = os.path.join(self.settings.settings_location, 'design', self.selected_design, 'override/templates', new_tpl_name) 

            # check to make sure the override template doesn't already exist
            if os.path.exists(new_tpl_path):

                sublime.status_message( 'Could not create override. The template ' + new_tpl_name + ' already exists in the design ' + self.selected_design)

            else:

                if not os.path.isdir(new_tpl_base_path):
                    os.mkdir(new_tpl_base_path)

                # create the override template
                file(new_tpl_path, 'w').close()

                # fill the template with all the attributes of the class
                tpl_content = ''

                # for each class group
                for class_group in self.data:

                    # for each content class
                    for content_class in class_group['class_list']:

                        if self.class_map[self.class_index] in content_class['details']['identifier']:

                            for attribute in content_class['attributes']:

                                tpl_content += '{attribute_view_gui attribute=$node.data_map.' + attribute['identifier'] + '}' + "\n\n"

                tpl_f = open(new_tpl_path, 'w')
                tpl_f.write(tpl_content)
                tpl_f.close()

                # check to see if the override file exists, if not, create it
                if not os.path.exists(override_file):
                    file(override_file, 'w').close()

                file_contents = "\n\n[" + self.tpl_map[self.selected_tpl] + "_" + self.class_map[self.class_index] + "]\n" + \
                "Source=" + self.selected_tpl + "\n" + \
                "MatchFile=" + new_tpl_name + "\n" + \
                "Subdir=templates\n" + \
                "Match[class_identifier]=" + self.class_map[self.class_index]

                # write to override file
                f = open(override_file, 'a')
                f.write(file_contents)
                f.close()

                # open override template
                self.window.open_file(new_tpl_path)

                sublime.status_message( 'Override template created')
