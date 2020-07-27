from taxonomizer import Taxonomizer


class TestTaxonomizer:

    tx = Taxonomizer()

    def test_compare_nodes(self):
        res = self.tx.compare_nodes(p='', g='', threshold=90)
        assert res is not None

    def test_compare_tokens_sort(self):
        res = self.tx.compare_tokens_sort(p='', g='', threshold=90)
        assert res is not None

    def test_compare_tokens_set(self):
        res = self.tx.compare_tokens_set(p='', g='', threshold=90)
        assert res is not None

    def test_set_review_level(self):
        res = self.tx.set_review_level(score=100)
        assert res is not None
        assert type(res) == str

    def test_add_file_contents_to_list(self):
        res = self.tx.add_file_contents_to_list(filename='')
        assert res is not None

    def test_get_unique_taxonomy_words(self):
        res = self.tx.get_unique_taxonomy_words(tax='')
        assert res is not None
        assert type(res) == str

    def test_get_taxonomy_words_and_symbols(self):
        res = self.tx.get_taxonomy_words_and_symbols(tax='')
        assert res is not None
        assert type(res) == str

    def test_get_taxonomy_nodes(self):
        res = self.tx.get_taxonomy_nodes(taxonomy='', selector=0, index=-1)
        assert res is not None

    def test_get_most_frequent_word(self):
        res = self.tx.get_most_frequent_word(source=[])
        assert res is not None

    def test_compare_taxonomies(self):
        list1, list2 = self.tx.compare_taxonomies(pub=[], goog=[], index=-1, threshold=95)
        assert list1 is not None
        assert list2 is not None

    def test_compare_taxonomies_by_token(self):
        list1, list2 = self.tx.compare_taxonomies_by_token(pub=[], goog=[], index=-1, threshold=95)
        assert list1 is not None
        assert list2 is not None

    def test_map_bucket_taxonomies(self):
        res = self.tx.map_bucket_taxonomies(pub=[])
        assert res is not None

    def test_is_in_bucket(self):
        res = self.tx.is_in_bucket(item='', taxonomy='')
        assert res is not None

    def test_map_vintage_taxonomies(self):
        res = self.tx.map_vintage_taxonomies(pub=[])
        assert res is not None

    def test_map_books(self):
        res = self.tx.map_books(pub=[])
        assert res is not None

    def test_map_gifts(self):
        res = self.tx.map_gifts(pub=[])
        assert res is not None
