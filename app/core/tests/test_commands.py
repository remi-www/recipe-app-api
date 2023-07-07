"""
Test custom Django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

""" To mock the behaviour of the check db """


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """" Test Django commands """

    def test_wait_for_db_ready(self, patched_check):
        """ Test waiting for db when db is available """

        # Mock the behaviour of the check db
        patched_check.return_value = True

        # Call the command
        call_command('wait_for_db')

        # Check if the command is called once with the database
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test waiting for db when getting Operationnal Error """

        # Mock a behaviour where the Psycopg2Error is called 2 times, then
        # OperationalError is called 3 times and then True is returned
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        # Call the command
        call_command('wait_for_db')

        # Check if the command is called 6 times with the database
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
