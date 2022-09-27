from platform import libc_ver
from random import randint


num_of_target_char = 15
num_of_missing_char = 3
num_of_max_repeat = 3

def make_chara():
    char_list = []
    while num_of_target_char > len(char_list):
        rand = randint(65,90)
        char = chr(rand)
        if char not in char_list:
            char_list.append(char)
    return char_list

def split_chara(char_list):
    delete_char = []
    for i in range(num_of_missing_char):
        rand = randint(0,len(char_list)-1)
        delete_char.append(char_list.pop(rand))
    return char_list, delete_char

def print_char(list_):
    for i in range(len(list_)):
        rand = randint(0,len(list_)-1)
        print(list_.pop(rand),end=' ')

def game_start(target_char, split_char):
    print('対象文字 : ')
    print_char(target_char)
    print('\n表示文字 : ')
    print_char(split_char[0])
    ans_num = int(input('\n\n欠損文字はいくつあるでしょうか? : '))
    if ans_num == num_of_missing_char:
        print('正解です． 具体的に欠損文字を1つずつ入力してください')
        char1 = input('1つ目の文字を入力してください : ')
        char2 = input('2つ目の文字を入力してください : ')
        char3 = input('3つ目の文字を入力してください : ')
        if char1 != char2 != char3 and char1 in split_char[1] and char2 in split_char[1] and char3 in split_char[1]:
            return True
    return False
    


if __name__ == '__main__':
    for i in range(num_of_max_repeat):
        list_ = make_chara()
        split_charactor = split_chara(list_.copy())
        result = game_start(list_,split_charactor)
        if result:
            print("正解です")
            break
        elif i != num_of_max_repeat -1:
            print('不正解です．もう一度やり押してください')
        else:
            print('不正解です． チャンスを使い切りました')
        print('--------------------------------------------')

    