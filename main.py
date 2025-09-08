from vigenere import VigenereCipher

def menu():
    print('----- Vigenere Cipher -----')
    print('\t1 - Encrypt message')
    print('\t2 - Decrypt message')
    print('\t3 - Attack ciphertext')
    print('\t4 - Quit')

vigenere = VigenereCipher()

def main():
    while True:
        menu()
        opcao = input('Select an option: ').strip()
        
        match opcao:
            case "1" | "2":
                try:
                    msg = input("Enter message: ").upper()
                    key = input("Enter key: ").upper()
                    if opcao == "1":
                        cipher = vigenere.crypt_decrypt(msg, key, 'C')
                        print("Encrypted message: ", cipher)
                    else:
                        decrypted_msg = vigenere.crypt_decrypt(msg, key, 'D')   
                        print("Decrypted message: ", decrypted_msg)
                except ValueError as e:
                    print(f"\nErro: {e}")
                    input()
        
            case "3":
                msg = input("Enter the ciphertext to attack: ").upper()
                if msg:
                    language_choice = input("Is the original message in Portuguese or English (PT/EN)? ").upper().strip()
                if language_choice not in ("PT", "EN"):
                    print("Invalid language choice. Please enter 'PT' or 'EN'.")
                    continue

                try_again = True
                while try_again:
                    key_length = vigenere.key_size(msg)
                    print("\nAttempting to break the keyword...")
                    found_keyword = vigenere.discover_break_keyword(key_length, msg, language_choice)
                    print("\n--- Attack Results ---")
                    print(f"Keyword found: '{found_keyword}'")
                    print("Decrypted message:")
                    decrypted_message = vigenere.crypt_decrypt(msg, found_keyword, 'D')
                    print(f"{decrypted_message}")
                    print("----------------------")

                    user_ans = input("\nRun the attack again with a different key size (Y/N)?\n>>> ")
                    try_again = (user_ans.upper() == 'Y')

            case "4":  
                break
            
            case _:  
                print("Opcao invalida!")
        
        input("\n")

main()











