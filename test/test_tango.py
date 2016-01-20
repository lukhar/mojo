from tango import Crawler


class TestCrawler:

    def test_given_empty_directory_return_empty_file_map(self):
        assert Crawler().crawl(path='resorces/dir1') == {}

    def test_given_directory_with_one_file_return_file_paths_to_hashes(self):
        assert Crawler().crawl(path='resorces/dir1') == {}

    def test_given_directory_with_files_return_file_paths_to_hashes(self):
        discovered_files = Crawler().crawl(path='resources/dir3').keys()

        assert {'resources/dir3/two', 'resources/dir3/three'} == set(discovered_files)

    def test_given_nested_directory_return_file_paths_to_hashes(self):
        discovered_files = Crawler().crawl(path='resources/dir4').keys()

        assert {'resources/dir4/four', 'resources/dir4/dir7/five'} == set(discovered_files)
