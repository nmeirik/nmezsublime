The eZ Publish plugin for Sublime Text 2 provides various functionality for speeding up
eZ Publish development, including:

* Syntax highlighting for templates and INI files
* Template snippets
* Various template manipulation features

# Demo
Check out http://vimeo.com/user8236717/review/29975170/9b4e2a9f1d for a video demo.


# Credits

Thanks to Ole Morten Halvorsen (http://www.omh.cc/) for the TextMate bundle which was used
as the basis for this package.


# Installation and setup

Place the package in the Packages folder of Sublime Text 2. On OSX, this is usually:

	~/Library/Application Support/Sublime Text 2/Packages

In order for syntax highlighting and template snippets to work, this is all you need. However,
if you also want to make use of the more advanced template manipulat


Create a file named .sublime_settings.json in the root of your design extension. The contents
of this file, should be as follows:

	{
		"ez_url": "http://yoursite.com/"
	}

Replace the URL with the actual URL of your eZ installation (trailing slash included).


# Dependencies

Several features in this package work by accessing a view in the nmcontent extension
(http://projects.ez.no/nmcontent). That means that this extension needs to be setup on the
eZ installation to which the ez_url setting points.


# Features

* Insert attribute
* Create override
* Translate strings


## Insert attribute

The insert attribute feature makes it quick and easy to insert a node attribute into a template
with the correct identifier, without ever leaving Sublime to look it up.

The feature is accessible from the keyboard shortcut Ctrl + I (for OSX).

When triggered, it produces a list of all the content class attributes that currently exists on
the installation in question. Scroll or do a keyword search to find the desired attribute, and
hit Enter to have it inserted into your template.


## Create override

The create override functionality provides a GUI for quickly creating override templates. Currently,
the function supports overriding the following templates:

* node/view/line.tpl
* node/view/full.tpl

The feature is accessible from the keyboard shortcut Ctrl + O (for OSX).

When triggered, you will be prompted with the following:

* The template you want to override
* The class for which you want the override to take effect
* The design in which you want to create the override (if several exist)


## Translate strings

This feature marks strings for translation by parsing the currently open template file.

The feature is accessible from the keyboard shortcut Ctrl + J (OSX).

When triggered, the function will ask for the translation context which should be used for the 
strings in the template, and will then continue on to ask for the original translation string of
the strings that were found, suggesting the original string as the default.

* If the original string matches the one that should be used as the original translation string
  (meaning it is in English), you can continue by hitting Enter.

* If the string is in another language, provide the English translation of the string, and hit Enter.

* If the string should not be translated, hit the Esc key.

* If you want to kill the translation process (meaning that no more strings will be translated), 
  write "!end" (without the quotes) and hit Enter.