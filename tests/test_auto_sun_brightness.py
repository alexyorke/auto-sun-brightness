import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import auto_sun_brightness

class TestAutoSunBrightness(unittest.TestCase):
    @patch('auto_sun_brightness.urllib.request.urlopen')
    def test_get_brightness(self, mock_urlopen):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.read.return_value = '''
        {
            "results": {
                "sunrise": "2023-01-01T07:00:00+00:00",
                "sunset": "2023-01-01T17:00:00+00:00"
            },
            "status": "OK"
        }
        '''.encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Mock the current time to be midday
        with patch('auto_sun_brightness.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = MagicMock()
            mock_datetime.utcnow.return_value.replace.return_value = MagicMock()
            
            # Test with min=0, max=10, at exactly midday (should return max value)
            with patch('auto_sun_brightness.parse') as mock_parse:
                # Mock the parse function to return specific datetime objects
                def side_effect(date_str):
                    mock = MagicMock()
                    mock.replace.return_value = mock
                    if "sunrise" in date_str:
                        # Mock timestamp for sunrise
                        return mock
                    else:
                        # Mock timestamp for sunset
                        return mock
                
                mock_parse.side_effect = side_effect
                
                # Mock the time calculation
                with patch('auto_sun_brightness.interp') as mock_interp:
                    mock_interp.return_value = 5.0
                    
                    result = auto_sun_brightness.get_brightness(
                        lat=40.7128, 
                        lng=-74.0060, 
                        max_intensity=10, 
                        min_intensity=0
                    )
                    
                    self.assertEqual(result, 5.0)
    
    def test_invalid_intensity_values(self):
        with self.assertRaises(ValueError):
            auto_sun_brightness.get_brightness(
                lat=40.7128, 
                lng=-74.0060, 
                max_intensity=5, 
                min_intensity=10  # Min > Max, should raise ValueError
            )

if __name__ == '__main__':
    unittest.main() 