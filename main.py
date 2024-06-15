#Password Generator

import random
import os

word_small = 'abcdefghijklmnopqrstuvwxyz'
word_caps = word_small.upper()
number = '1234567890'
symbols = '!@#$%&*()_-+='
password = ''
show = ''
length = ''



print('Hello!')
print()
print('Select what`s password do you want:')
print('1) Words lower case')
print('2) Words upper case')
print('3) Numbers')
print('4) Symbols')
print('5) countinue to next step')

print('\n')


while True:
    select = input('Select: ')

    if select == '1':
        print('Word lower case: True')
        password += word_small
        show += 'Lower case    '

    elif select == '2':
        print('Word upper case: True')
        password += word_caps
        show += 'Upper case    '


    elif select == '3':
        print('Number: True')
        password += number
        show +=  'Number    '

    elif select == '4':
        print('Symbol: True')
        password += symbols
        show +=  'Symbol    '


    elif select == '5':
        break

    else:
        print('You must select between number 1 to 5!')
        continue




os.system('cls')
print(f'your password will be create with: {show}')

try:
    length = int(input('Enter your desired password length: '))

    generated_password = ''.join(random.sample(password, length))
    
    print(f'Your generated password is: {generated_password}')

except ValueError:
    print('Invalid input. Please enter a valid number for password length.')