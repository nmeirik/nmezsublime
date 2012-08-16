import sublime
import sublime_plugin
import ezsettings
from BeautifulSoup import BeautifulSoup
import re


class TranslateStringsCommand(sublime_plugin.WindowCommand):
    
    def run(self):

        # get the current contents of the file
        self.html = self.window.active_view().substr(sublime.Region(0, self.window.active_view().size()))

        # instantiate
        self.soup = BeautifulSoup(self.html)

        # get all the strings in the document
        self.elementList = self.soup(text=True) 

        # set counter
        self.counter = 0
        self.found_counter = 0
        self.translated_counter = 0

        if len(self.elementList) > 0:
            # request the translation context
            self.request_context()
        else:
            self.complete_translation()
        

    def request_context(self):

        self.window.show_input_panel('Please provide the translation context ', 'translation/context', self.context_done, None, self.context_cancel)

    def context_done(self, input):

         # store the context
        self.context = input

        # request the first translation
        self.request_translation()

    def context_cancel():
        self.complete_translation()

    def request_translation(self):

        elements_remain = True

        # making sure the element exists
        try:
            self.elementList[self.counter]
        except IndexError:
            elements_remain = False

        if elements_remain:

            self.cur_element = self.elementList[self.counter].strip()

            # unless the element is empty
            if self.cur_element != '':

                # unless the string is ez template code
                if '{' not in self.cur_element and '}' not in self.cur_element:

                    self.found_counter += 1
                    self.window.show_input_panel('Translate: ' + self.cur_element, self.cur_element, self.translation_done, self.translation_change, self.translation_cancel)

                else:
                    self.translation_cancel()

            else:
                self.translation_cancel()
        else:
            self.complete_translation()

    def translation_change(self, input):
        pass

    def translation_cancel(self):

        # continue on to next translation
        self.counter += 1
        self.request_translation()

    def translation_done(self, input):

        # if the user has selected to end the translation process
        if '!end' in input:

            # complete the translation
            self.complete_translation()
        else:

            # insert the translation string
            translation_string = '{"' + input + '"|i18n("' + self.context + '")}'
            self.html = self.html.replace(str(self.cur_element), translation_string)

            self.translated_counter += 1

            # continue on to next translation
            self.counter += 1
            self.request_translation()

    def complete_translation(self):

        # begin edit
        edit = self.window.active_view().begin_edit()

        # deleted the current contents of the file
        self.window.active_view().erase(edit, sublime.Region(0, self.window.active_view().size()))

        # insert new html
        self.window.active_view().insert(edit, 0, self.html)

        # end edit
        self.window.active_view().end_edit(edit)

        sublime.status_message( str(self.found_counter) + ' translateable strings found. ' + str(self.translated_counter) + ' strings translated.' )