import unittest

from src.utilities.UrlUtilities import UrlUtilities


class UrlUtilitiesTest(unittest.TestCase):

    def test_relative_path_no_slash_successfully(self):

        previous_url = "https://test.com/sub_part/test"
        url = "2021/"
        domain = "DOMAIN"

        fixedUrl = UrlUtilities.fix_url(previous_url, url, domain)

        self.assertEqual("https://test.com/sub_part/test/2021/", fixedUrl)

    def test_relative_path_with_current_directory_slash_successfully(self):

        previous_url = "https://test.com/sub_part/test"
        url = "./2021"
        domain = "DOMAIN"

        fixedUrl = UrlUtilities.fix_url(previous_url, url, domain)

        self.assertEqual("https://test.com/sub_part/test/2021", fixedUrl)

    def test_relative_path_with_direct_file_name_successfully(self):

        previous_url = "https://test.com/"
        url = "index.php"
        domain = "DOMAIN"

        fixedUrl = UrlUtilities.fix_url(previous_url, url, domain)

        self.assertEqual("https://test.com/index.php", fixedUrl)

    def test_relative_path_with_one_directory_back_successfully(self):

        previous_url = "https://test.com/"
        url = "../index.php"
        domain = "https://test.com"

        fixedUrl = UrlUtilities.fix_url(previous_url, url, domain)

        self.assertEqual("https://test.com/index.php", fixedUrl)