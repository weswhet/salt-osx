## salt-osx ##

Manage a mac fleet with SaltStack: Salt Modules/Grains/States for Mac OS X w/PyObjC. *Alpha Quality*

The motivation for this repository is to provide SaltStack modules that call into native Foundation/Cocoa API via PyObjC.
This would theoretically give you more control over configuration than scripting alone.

There are also some modules that use command line tools but expand on the support provided by salt.

The modules are constantly at different levels of maturity.

## Installation ##

**VERY IMPORTANT:** You must disable multiprocessing on the Mac OS X minions for native modules to work. This is
because salt-minion threading does not work **at all** with CoreFoundation API. If you do not do this, the minion will 
crash without warning when trying to execute some modules. This is not the case with `salt-call` as it does not seem to 
use multiple threads.

You must edit your minion configuration file, usually `/etc/salt/minion` to include the following line:

    multiprocessing: False
    
This repository can then be added to your `file_roots` or whichever fileserver backend you happen to be using for your
master or masterless setup.

## Grains ##

- **filevault_enabled** FileVault state, True or False.
- **mac_admin_users** List of users in the local admin group.
- **mac_current_user** Currently logged in user.
- **mac_has_wireless** AirPort or WiFi device enabled, True or False.
- **mac_java_vendor** JRE vendor (Apple or Oracle)
- **mac_java_version** JRE version string
- **mac_laptop** 'mac_desktop' or 'mac_laptop', indicating the hardware type.
- **mac_timezone** Current system timezone.

## Execution Modules ##

- [ard](docs/markdown/ard.md) **mature** Remote Management service configuration.
- [authorization](docs/markdown/authorization.md) *broken* Utility module for granting authorization to CoreFoundation API.
- [bluetooth](docs/markdown/bluetooth.md) **mature** Manage bluetooth.
- [cups](docs/markdown/cups.md) **beta** Configure printers
- [desktop](docs/markdown/desktop.md) *broken* Interact with and manage the current users session.
- [dscl](docs/markdown/dscl.md) **beta** Query and modify the local directory service.
- [finder](docs/markdown/finder.md) *broken* Interact with the Finder. Query and modify sidebar items (LSSharedFileList).
- [keychain](docs/markdown/keychain.md) *broken* Add/Remove keychains and keychain items
- [launchd](docs/markdown/launchd.md) *broken* Attempt to load jobs through CoreFoundation (completely broken)
- [login](docs/markdown/login.md) **beta** Manage loginwindow preferences, Manage login items for current user.
- [plist](docs/markdown/plist.md) **beta** Manage PropertyList files/key values.
- [power](docs/markdown/power.md) **mature** Interact with system power (i.e sleep/shutdown/reboot).
 
## TODO ##

General Roadmap Notes:

- SaltStack Shortcomings:
    + **services**: launchctl.py enumeration of standard directories could potentially be faster through other API
    methods. If i want to be really pedantic then `restart()` doesnt need the `-w` flag for overrides.
    + **user**: mac_user.py Badly needs ShadowHash implementation similar to macadmin in ruby.
    + **pkg**: brew.py/macports.py No implementation for `installer` tool? Steal another implementation just so that
    Salt could be used to bootstrap other package management solutions.
    + **netstat**: No netstat implementation for osx
    + **ps**: No ps implementation for osx
    
- Stuff that should be parity with macadmin:
    + computer/computer group records (DSLocal)
    + authorization db
    + everything and anything that relates to profile installation

- Need to support configuration profile management including generation and remote enrollment.