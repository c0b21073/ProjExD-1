from random import choice
from datetime import datetime


def shutudai(questions):
    question = choice(questions)
    ans = input(question[0]+': ').strip()
    if ans in question[1]:
        print("正解!")
    else:
        print('間違い!')

if __name__ == '__main__':
    questions = (('サザエさんの旦那の名前は？', ('マスオ','ますお')),
             ('カツオの妹の名前は?',('ワカメ','わかめ')),
             ('タラオはカツオからみてどんな関係?',('甥','おい','甥っ子','おいっこ'))
            )

    st = datetime.now()
    shutudai(questions)
    ed = datetime.now()
    print(f'所要時間は{(ed-st).seconds}秒')