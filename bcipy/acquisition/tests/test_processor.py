
from bcipy.acquisition.processor import FileWriter
from bcipy.acquisition.device_info import DeviceInfo
from mock import mock_open, patch
import pytest
import unittest


class TestFilewriter(unittest.TestCase):

    def test_filewriter(self):
        """Test FileWriter functionality"""

        data = [[i + j for j in range(3)] for i in range(3)]
        expected_csv_rows = ['0,1,2\r\n', '1,2,3\r\n', '2,3,4\r\n']

        filewriter = FileWriter('foo.csv')
        filewriter.set_device_info(DeviceInfo(name='foo-device', fs=100,
                                              channels=['c1', 'c2', 'c3']))

        m = mock_open()
        with patch('bcipy.acquisition.processor.open', m):
            with filewriter:
                m.assert_called_once_with('foo.csv', 'w', newline='')

                handle = m()
                handle.write.assert_called_with('timestamp,c1,c2,c3\r\n')

                for i, row in enumerate(data):
                    timestamp = float(i)
                    filewriter.process(row, timestamp)
                    handle.write.assert_called_with(
                        str(timestamp) + "," + str(expected_csv_rows[i]))

            m().close.assert_called_once()

    def test_filewriter_setup(self):
        """
        Test that FileWriter throws an exception if it is used without setting
        the device_info.
        """

        filewriter = FileWriter('foo.csv')

        with pytest.raises(Exception):
            with filewriter:
                pass
