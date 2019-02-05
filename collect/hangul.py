import re

hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')


def filter(text):
    filtered = hangul.sub('', text)
    return ' '.join(filtered.split())


if __name__ == '__main__':
    print(filter('abcd한글 b 한글'))
    print(filter('abcd한글 b 한글'))
