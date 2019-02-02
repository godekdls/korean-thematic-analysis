from konlpy.tag import Twitter
from konlpy.utils import pprint

twitter = Twitter()


def extract_nouns(text):
    nouns = twitter.nouns(text)
    return ' '.join(nouns)


if __name__ == '__main__':
    pprint(extract_nouns('비티랑 토리가 그랬잖아. 네, 안녕하세요.'))
