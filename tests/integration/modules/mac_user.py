# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Nicole Thomas <nicole@saltstack.com>`
'''

# Import Python Libs
import os
import random
import string

# Import Salt Testing Libs
from salttesting import skipIf
from salttesting.helpers import (
    destructiveTest,
    ensure_in_syspath,
    requires_system_grains
)
ensure_in_syspath('../../')

# Import Salt Libs
import integration
from salt.exceptions import CommandExecutionError


class MacUserModuleTest(integration.ModuleCase):
    '''
    Integration tests for the mac_user module
    '''

    def setup(self):
        '''
        Sets up test requirements
        '''
        super(MacUserModuleTest, self).setUp()
        os_grain = self.run_funtion('grains.item', ['kernel'])
        if os_grain['kernel'] not in ('Darwin'):
            self.skipTest(
                'Test not applicable to \'{kernel}\' kernel'.format(
                    **os_grain
                )
            )

    def __random_string(self, size=6):
        '''
        Generates a random username
        '''
        return 'RS-' + ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for x in range(size)
        )

    @destructiveTest
    @skipIf(os.geteuid() != 0, 'You must be logged in as root to run this test')
    @requires_system_grains
    def test_mac_users_add(self):
        '''
        Tests the add function
        '''
        user_name = self.__random_string()

        try:
            self.run_function('mac_user.add', [user_name, True, True])
            user_info = self.run_function('mac_user.info', [user_name])
            self.assertIn(user_name, user_info['name'])
        except CommandExecutionError:
            self.run_function('mac_user.delete', [user_name, True, True])
            raise


if __name__ == '__main__':
    from integration import run_tests
    run_tests(MacUserModuleTest)
