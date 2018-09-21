# -*- coding: utf-8 -*-
'''
State will write or delete macOS preferences.

Below is a general guide to where the preferences will be written if you
specify a user and host. If you don't specify a runas user it will be written to
root's directory, otherwise the given Users directory.

{'file': ('/var/root/Library/Preferences/ByHost/domain.xxxx.plist'),
    'domain': domain,
    'user': kCFPreferencesCurrentUser,
    'host': kCFPreferencesCurrentHost
},
{'file': '/var/root/Library/Preferences/domain.plist',
    'domain': domain,
    'user': kCFPreferencesCurrentUser,
    'host': kCFPreferencesAnyHost
},
{'file': '/Library/Preferences/domain.plist',
    'domain': domain,
    'user': kCFPreferencesAnyUser,
    'host': kCFPreferencesCurrentHost
},


.. code-block:: yaml
    write_burrito_location_preference:
      prefs.write:
        - name: BurritoLocation
        - value: The Mission
        - domain: com.rounded.edges.corp

.. code-block:: yaml
    write_burrito_location_preference:
      prefs.delete:
        - name: BurritoLocation
        - domain: com.rounded.edges.corp
        - user: True
'''

import salt.utils.platform
import logging
import sys

log = logging.getLogger(__name__)


__virtualname__ = 'prefs'


def __virtual__():
    if salt.utils.platform.is_darwin():
        return __virtualname__

    return (False, 'states.prefs only available on macOS')


def write(name, value, domain, user=None, host=None, runas=None):
    '''
    Set a preference value using CFPreferences. This is deprecated in
    favor of exists and will be removed in a future version.

    name
        The preference key to write.

    value
        The value to which the key should be set, type will match the types
        passed via the state.

    domain
        The domain to which the key and value should be set in.

    user
        The user domain to use, either 'current' or 'any'.

    host
        The host domain to use, either 'current' or 'any'.

    runas
        The user to run as should be a short username.
    '''
    return exists(name, value, domain, user, host, runas)


def exists(name, value, domain, user=None, host=None, runas=None):
    '''
    Set a preference value using CFPreferences.

    name
        The preference key to write.

    value
        The value to which the key should be set, type will match the types
        passed via the state.

    domain
        The domain to which the key and value should be set in.

    user
        The user domain to use, either 'current' or 'any'.

    host
        The host domain to use, either 'current' or 'any'.

    runas
        The user to run as should be a short username.
    '''
    ret = {'name': name,
           'result': False,
           'changes': {},
           'comment': ''}

    # Currently, no validation is performed.

    old_value = __salt__['prefs.read'](name, domain, user, host, runas)

    # check if we are set correctly
    if old_value == value:
        ret['result'] = True
        ret['comment'] = '{} {} is already set to {}'.format(
            domain, name, value)
        return ret

    ret['changes'].update({name: {'old': old_value, 'new': value}})

    # See if we're in test mode and report if so.
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = '{} {} would be set to {}'.format(
            domain, name, value)
        return ret

    set_val = __salt__['prefs.set'](name, value, domain, user, host, runas)

    if not set_val:
        ret['comment'] = 'Failed to set {} {} to {}'.format(
            domain, name, value)
    else:
        ret['result'] = True
        ret['comment'] = '{} {} is set to {}'.format(domain, name, value)
    return ret


def delete(name, domain, user=None, host=None, runas=None):
    '''
    Delete a Preference Key. This is deprecated in
    favor of absent and will be removed in a future version.

    name
        The preference key to delete.

    domain
        The domain the key should be removed from.

    user
        The user domain to use, either 'current' or 'any'.

    host
        The host domain to use, either 'current' or 'any'.

    runas
        The user to run as should be a short username.
    '''
    return absent(name, domain, user, host, runas)


def absent(name, domain, user=None, host=None, runas=None):
    '''
    Delete a Preference Key.

    name
        The preference key to delete.

    domain
        The domain the key should be removed from.

    user
        The user domain to use, either 'current' or 'any'.

    host
        The host domain to use, either 'current' or 'any'.

    runas
        The user to run as should be a short username.
    '''

    ret = {'name': name,
           'result': False,
           'changes': {},
           'comment': ''}

    old_value = __salt__['prefs.read'](name, domain, user, host, runas)

    if old_value is None:
        ret['result'] = True
        ret['comment'] = '{} {} is already removed.'.format(domain, name)
        return ret

    ret['changes'].update({name: {'old': old_value, 'new': None}})

    # See if we're in test mode and report if so.
    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = '{} {} would be removed.'.format(domain, name)
        return ret

    set_val = __salt__['prefs.set'](name, None, domain, user, host, runas)

    if not set_val:
        ret['comment'] = 'Failed to remove {} {}.'.format(domain, name)
    else:
        ret['result'] = True
        ret['comment'] = '{} {} has been removed.'.format(domain, name)
    return ret
