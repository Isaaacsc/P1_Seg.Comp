import string
from typing import List, Dict, Tuple

class VigenereCipher:
    def __init__(self):
        self.alphabet = string.ascii_uppercase
        self.base_ord = ord('A')
        self.eng_probabilities = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
        self.pt_probabilities = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]

    def text_alphabet(self, text):
        only_letters_text = ""
        for letter in text:
            if letter in self.alphabet:
                only_letters_text += letter
        return only_letters_text

    def generate_keystream(self, text, key):
        only_letters_text = list(self.text_alphabet(text))
        keystream = ""
        key_len = len(key)
        for i in range(len(only_letters_text)): 
            keystream += key[i % key_len]
        return keystream

    def crypt_decrypt(self, text, key, option):
        if option in ('C', 'D') and (len(text) <= 0 or len(key) < 2):
            raise ValueError('Invalid text or key length.')
        
        if option == 'C':
            operacao = 1
        elif option == 'D':
            operacao = -1
        else:
            raise ValueError("Option must be 'C' or 'D'.")
            
        keystream = self.generate_keystream(text, key)
        
        result = []
        key_index = 0

        for c in text: 
            if c in self.alphabet:
                c_key = keystream[key_index]
                
                val_text = ord(c) - self.base_ord
                val_key = ord(c_key) - self.base_ord
                
                final_value = (val_text + operacao * val_key) % 26
                
                result.append(self.alphabet[final_value])

                key_index += 1
            else:
                result.append(c)

        return "".join(result)
    
    def key_size(self, text):
        text = self.text_alphabet(text)
        spacing = []
    
        for i in range(len(text)-2):
            trigram = text[i] + text[i+1] + text[i+2]
            for j in range(i+1, len(text)-2):
                aux = text[j] + text[j+1] + text[j+2]
                if aux == trigram:
                    spacing.append((trigram, j-i))
        
        spacing = list(set(spacing))

        key_size_votes = {}

        for _, distance in spacing:
            for size in range(2, 26):
                is_a_divisor = (distance % size == 0)

                if is_a_divisor:
                    current_votes = key_size_votes.get(size, 0)
                    key_size_votes[size] = current_votes + 1

        best_key_size = 0 
        highest_vote_count = 0

        print("\n--- Key Size Analysis ---")
        for candidate_size, number_of_votes in key_size_votes.items():
            if number_of_votes >= highest_vote_count:
                highest_vote_count = number_of_votes
                best_key_size = candidate_size
            print(f"Size: {candidate_size:2d} -- Votes: {number_of_votes}")

        print("\n-------------------------------------------")
        print(f"The most probable key size is: {best_key_size}")
        print("-------------------------------------------")

        user_rsp = input("Do you want to continue with this key size? (Y/N)\n>>> ")
        if user_rsp.lower() == 'n':
            user_chosen_size = int(input("Enter the key size you want to test (between 2 and 25): "))
            while user_chosen_size > 25 or user_chosen_size < 2:
                user_chosen_size = int(input("Invalid size. Please enter a number between 2 and 25: "))
            return user_chosen_size
        return best_key_size
    
    def discover_break_keyword(self, key_length, ciphertext, language):
        letter_only_text = self.text_alphabet(ciphertext)
        
        if language == 'EN':
            language_frequencies = self.eng_probabilities
        else:
            language_frequencies = self.pt_probabilities
            
        found_keyword = ""
        for column_number in range(key_length):
            letters_in_this_column = letter_only_text[column_number::key_length]
            
            letter_counts = {}
            for letter in letters_in_this_column:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1
            probabilities_for_this_column = []
            total_letters_in_column = len(letters_in_this_column)
            
            for letter_of_alphabet in self.alphabet:
                count = letter_counts.get(letter_of_alphabet, 0)
                percentage = (count / total_letters_in_column) * 100
                probabilities_for_this_column.append(percentage)
            
            best_letter_for_this_column = ''
            smallest_difference_found = float('inf')

            for i in range(26):
                candidate_key_letter = self.alphabet[i]
                total_difference_for_this_candidate = 0
                
                for j in range(26):
                    observed_probability = probabilities_for_this_column[(i + j) % 26]
                    expected_probability = language_frequencies[j]

                    total_difference_for_this_candidate += abs(observed_probability - expected_probability)
                
                if total_difference_for_this_candidate < smallest_difference_found:
                    smallest_difference_found = total_difference_for_this_candidate
                    best_letter_for_this_column = candidate_key_letter
            
            found_keyword += best_letter_for_this_column
        return found_keyword
    