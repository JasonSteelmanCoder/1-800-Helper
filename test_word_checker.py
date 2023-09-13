"""This program will test the proper functioning of word_checker.py."""

import unittest
import word_checker as wc

class TestWC(unittest.TestCase):

    def test_word_list_exists(self):
        self.assertIsNotNone(wc.word_list)

    def test_letter_assignments_correct(self):
        self.assertEqual({
                '0':[], 
                '1':[],
                '2':['a', 'b', 'c'], 
                '3':['d', 'e', 'f'], 
                '4':['g', 'h', 'i'], 
                '5':['j', 'k', 'l'], 
                '6':['m', 'n', 'o'], 
                '7':['p', 'q', 'r', 's'], 
                '8':['t', 'u', 'v'], 
                '9':['w', 'x', 'y', 'z']
            }, wc.letter_assignments)

        self.assertEqual({
                '0':['0'], 
                '1':['1'],
                '2':['a', 'b', 'c', '2'], 
                '3':['d', 'e', 'f', '3'], 
                '4':['g', 'h', 'i', '4'], 
                '5':['j', 'k', 'l', '5'], 
                '6':['m', 'n', 'o', '6'], 
                '7':['p', 'q', 'r', 's', '7'], 
                '8':['t', 'u', 'v', '8'], 
                '9':['w', 'x', 'y', 'z', '9']
            }, wc.letter_assignments_plus_nums)
        
    def test_prepare_phone_number(self):
        prepared_phone_num = wc.prepare_phone_number("18003334444")
        self.assertEqual(prepared_phone_num, ['3', '3', '3', '4', '4', '4', '4'])
        self.assertEqual(type(prepared_phone_num), list)
        self.assertEqual(type(prepared_phone_num[0]), str)
        self.assertEqual(len(prepared_phone_num), 7)

    def test_find_words_for_num(self):
        words_spelled_by_num = wc.find_words_for_num(['3', '3', '3', '4', '4', '4', '4'])
        self.assertEqual(type(words_spelled_by_num), list)
        self.assertEqual(type(words_spelled_by_num[0]), str)
        self.assertIn("high", words_spelled_by_num)

    def test_find_num_for_word(self):
        peach_lower_result = wc.find_num_for_word("peach")
        peach_upper_result = wc.find_num_for_word("Peach")
        peach1_result = wc.find_num_for_word("peach1")
        peach_dot_result = wc.find_num_for_word("peach.")
        peach_space_result = wc.find_num_for_word("pe ach")
        plum_result = wc.find_num_for_word("plum")
        blank_result = wc.find_num_for_word("")

        results = [peach_lower_result, peach_upper_result, peach1_result, peach_dot_result, peach_space_result, plum_result]
        expected_results = ['73224', '73224', '732241', '73224', '73224', '7586']

        for result in results:
            self.assertEqual(type(result), str)
            self.assertIsNotNone(int(result))
        
        self.assertEqual(results, expected_results)
        self.assertEqual(blank_result, "")

    def test_search_available_nums_for_word(self):
        test_word1 = "puppy"
        test_word2 = "dog"
        available_nums_with_test_words = ["18002278779", "18004444364"]
        available_nums_without_test_words = ["18007777777", "180088888888"]

        positive_results1 = wc.search_available_nums_for_word(test_word1, available_nums_with_test_words)
        self.assertEqual(positive_results1, "18002278779")
        positive_results2 = wc.search_available_nums_for_word(test_word2, available_nums_with_test_words)
        self.assertEqual(positive_results2, "18004444364")

        negative_results1 = wc.search_available_nums_for_word(test_word1, available_nums_without_test_words)
        self.assertEqual(negative_results1, None)
        negative_results2 = wc.search_available_nums_for_word(test_word2, available_nums_without_test_words)
        self.assertEqual(negative_results2, None)

if __name__ == "__main__":
    unittest.main()