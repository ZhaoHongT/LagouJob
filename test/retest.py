import re


def match_quote(str_to_match):
    if re.search(r':"\w\'\w"', str_to_match, re.I):
        print('match successfully!')
    else:
        print('match failed!')


if __name__ == '__main__':
    print(':"哈哈\'s科技时尚男装"')
    match_quote(':"哈哈\'s科技时尚男装"')
