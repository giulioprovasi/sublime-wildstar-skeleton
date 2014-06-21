import sublime
import sublime_plugin
import os
import shutil
import xml.etree.cElementTree as et
from xml.etree import ElementTree as Element


class WildstarAddonBuilderCommand(sublime_plugin.TextCommand):

    WILDSTAR_PATH = 'AppData\\Roaming\\NCSOFT\\WildStar'

    def run(self, edit):

        # check whether Wildstar is installed, if not, raise an exception
        if not os.path.exists(self.wildstar_path()):
            sublime.error_message('Wildstar must be installed before using this plugin.')
            raise Exception('Wildstar not installed.')

        # create addon directory if doesn't exists
        addon_dir = os.path.join(self.wildstar_path(), 'Addons')
        if not os.path.exists(addon_dir):
            os.makedirs(addon_dir)

        self.counter = 0
        self.keys = ['name', 'author', 'description', 'invoke', 'list', 'timer', 'repeat']
        self.available_addons = []
        self.dictionary = {
            'name': Bunch(name='Name', value='eee'),
            'author': Bunch(name='Author', value=''),
            'description': Bunch(name='Description', value=''),
            'invoke': Bunch(name='Invoke command', value=None),
            'list': Bunch(name='Include list of items', value=False),
            'timer': Bunch(name='Timer', value=0),
            'repeat': Bunch(name='Repeating timer', value=False),
            'replace': Bunch(name='Replace addon', value=None)
        }

        try:
            self.show_prompt()
        except FileExistsError:
            sublime.error_message('An error occured while creating the plugin, check the console for more info.')
            raise

    def __replaceaddon(self):
        # toc.xml, adding ReplaceAddon
        file = os.path.join(self.wildstar_path(), 'Addons.xml')
        tree = et.parse(file)
        for ch in tree.getroot().getchildren():
            self.available_addons.append(ch.attrib['Folder'])
        self.view.window().show_quick_panel(self.available_addons, self.__on_replaceaddon_done)

    def __on_replaceaddon_done(self, pos):
        self.dictionary['replace'].value = (None if -1 == pos else self.available_addons[pos])
        self.create_skeleton()

    def on_done(self, content):
        self.dictionary[self.keys[self.counter]].value = self.check_user_input(self.keys[self.counter], content)
        self.counter += 1
        if self.counter < (len(self.dictionary)-1):  # skip last index
            self.show_prompt()
        else:
            self.input_done()

    def check_user_input(self, key, content):
        return {
            'name': lambda s: s,
            'author': lambda s: s,
            'description': lambda s: s,
            'invoke': lambda s: s or None,
            'list': lambda s: True if (s.lower() in ['yes', '1', 'true', 'ok']) else False,
            'timer': lambda s: ("%0.1f" % float(s)) if self.is_number(s) else False,
            'repeat': lambda s: True if (s.lower() in ['yes', '1', 'true', 'ok']) else False,
        }[key](content)

    def input_done(self):
        # for k in self.dictionary:
        #     value = self.dictionary[k].value
        #     if (value is None):
        #         print(k+': None')
        #     elif (value is True):
        #         print(k+': true')
        #     elif (value is False):
        #         print(k+': false')
        #     else:
        #         print(k+': '+value)
        self.__replaceaddon()

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def show_prompt(self):
        self.view.window().show_input_panel(self.dictionary[self.keys[self.counter]].name, '', self.on_done, None, None)

    def wildstar_path(self):
        return os.path.join(os.getenv('userprofile'), self.WILDSTAR_PATH)

    def create_skeleton(self):

        dest_dir = os.path.join(self.wildstar_path(), 'Addons', self.dictionary['name'].value)

        try:
            os.makedirs(dest_dir)
        except FileExistsError:
            sublime.error_message('An addon named '+self.dictionary['name'].value+' already exists.')
            raise Exception('Addon '+self.dictionary['name'].value+' already exists.')

        files = ['Addon.lua', 'Addon.xml', 'toc.xml']
        for file in files:
            print('Copying '+file+' to '+dest_dir)
            file = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
            shutil.copy(file, dest_dir)

        # replace all placeholders in each file
        self.parse_files()

        # update project files
        self.__update_project()

    def __update_project(self):
        dir_name = os.path.join(self.wildstar_path(), 'Addons', self.dictionary['name'].value)
        project_data = self.view.window().project_data()
        folder = {
            'follow_symlinks': True,
            'path': dir_name,
            'folder_exclude_patterns': ['.*'],
            # maybe, we need to edit .gitignore,
            # so do not exclude files that it's name begin with dot
            # 'file_exclude_patterns': ['.*'],
        }

        try:
            folders = project_data['folders']
            for f in folders:
                if f['path'] == dir_name:
                    return
            folders.append(folder)
        except:
            folders = [folder]
            if project_data is None:
                project_data = {}
            project_data['folders'] = folders
        self.view.window().set_project_data(project_data)
        self.view.window().open_file(os.path.join(dir_name, 'Addon.lua'))

    def parse_files(self):

        addon_dir = os.path.join(self.wildstar_path(), 'Addons', self.dictionary['name'].value)

        # Addon.xml
        file = os.path.join(addon_dir, 'Addon.xml')
        tree = et.parse(file)
        n = tree.getroot().getchildren()[0]
        n.attrib['Name'] = self.dictionary['name'].value+'Form'
        tree.write(file, xml_declaration=True, encoding='UTF-8')

        # toc.xml
        file = os.path.join(addon_dir, 'toc.xml')
        tree = et.parse(file)
        n = tree.getroot()
        n.attrib['Author'] = self.dictionary['author'].value
        n.attrib['Name'] = self.dictionary['name'].value
        n.attrib['Description'] = self.dictionary['description'].value
        n.find('Script').attrib['Name'] = self.dictionary['name'].value+'.lua'
        n.find('Form').attrib['Name'] = self.dictionary['name'].value+'.xml'
        if (self.dictionary['replace'].value is not None):
            n.append(Element.fromstring('<ReplaceAddon name="%s"/>' % self.dictionary['replace'].value))
        tree.write(file, xml_declaration=True, encoding='UTF-8')

        # Addon.lua
        file = os.path.join(addon_dir, 'Addon.lua')
        hasinvokecmd = self.dictionary['invoke'].value is not None
        hastimer = self.dictionary['timer'].value is not False
        haslist = self.dictionary['list'].value is True
        lines_to_remove = []

        with open(file, 'r+') as fh:
            data = fh.readlines()
            for i in range(len(data)):
                if ('<IFTIMER>' in data[i] and hastimer is False):
                    lines_to_remove.append(i)
                    continue
                else:
                    data[i] = data[i].replace('<IFTIMER>', '')

                if ('<IFLIST>' in data[i] and haslist is False):
                    lines_to_remove.append(i)
                    continue
                else:
                    data[i] = data[i].replace('<IFLIST>', '')

                # CMD must be the last tested because of nested <IF>
                if ('<IFCMD>' in data[i] and hasinvokecmd is False):
                    lines_to_remove.append(i)
                    continue
                else:
                    data[i] = data[i].replace('<IFCMD>', '')

                if ('<WSNAME>' in data[i]):
                    data[i] = data[i].replace('<WSNAME>', self.dictionary['name'].value)

                if ('<WSTIMER>' in data[i]):
                    data[i] = data[i].replace('<WSTIMER>', self.dictionary['timer'].value)

                if ('<WSREPEAT>' in data[i]):
                    data[i] = data[i].replace('<WSREPEAT>', 'true' if self.dictionary['timer'].value else 'false')

                if ('<WSCMD>' in data[i] and self.dictionary['invoke'].value is not None):
                    data[i] = data[i].replace('<WSCMD>', self.dictionary['invoke'].value)

            for i in sorted(lines_to_remove, reverse=True):
                del data[i]

            fh.seek(0)
            fh.writelines(data)
            fh.truncate()
            fh.close()


class Bunch(object):

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
