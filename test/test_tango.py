from tango import Crawler


class TestCrawler:

    def test_given_empty_directory_return_empty_file_map(self):
        assert Crawler().crawl(path='resorces/dir1') == {}

    def test_given_directory_with_files_return_file_paths_to_hashes(self):
        discovered_files = Crawler().crawl(path='resources/dir2').keys()

        assert {'resources/dir2/one', 'resources/dir2/two'} == discovered_files
