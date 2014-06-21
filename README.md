sublime-ws-skeleton
===================

A Sublime Text 3 plugin to generate the Wildstar addon skeleton as in Houston

Provides the following features:

* Creating an addon as in Houston, with name, author, description and any other option
* Build the Addon folder and install it to Wildstar game directory

Plugin should work in all three platforms (MacOS X, Windows and Linux).


Installing
----------
**With the Package Control plugin:** The plugin isn't actually on Package Control plugin

**Without Git:** Download the latest source from `GitHub <https://github.com/kitensei/sublime-wildstar-skeleton>`_ and copy the whole directory into the Packages directory.

**With Git:** Clone the repository in your Sublime Text Packages directory, located somewhere in user's "Home" directory::

    git clone git://github.com/kitensei/sublime-wildstar-skeleton


The "Packages" packages directory is located differently in different platforms. To access the directory use:

* OS X::

    Sublime Text -> Preferences -> Browse Packages...

* Linux::

    Preferences -> Browse Packages...

* Windows::

    Preferences -> Browse Packages...


Configuring
-----------
Shortcut can be set in the User Keymap File Settings as follows::

    {
        "keys": ["alt+w"], 
        "command": "wildstar_addon_builder"
    }


Troubleshooting
---------------

Actually I didn't found a way to select multiple **ReplaceAddon** addons, so once you have selected one, the quick panel will close and further addons can be added manually into the xml


Building
--------

Building process is no longer distributed with this repository. You need to get SublimeCodeIntel/`CodeIntelSources <https://github.com/SublimeCodeIntel/CodeIntelSources/>`_ to run ``build.sh``.

More information in SublimeCodeIntel/CodeIntelSources/`src <https://github.com/SublimeCodeIntel/CodeIntelSources/src>`_.


License
-------
The plugin is on MIT License.