from konlpy.tag import Kkma
from konlpy.utils import pprint

kkma = Kkma()


def extract_nouns(text):
    nouns = kkma.nouns(text)
    return ' '.join(nouns)


if __name__ == '__main__':
    pprint(extract_nouns('비티랑 토리가 그랬잖아. 네, 안녕하세요.'))
