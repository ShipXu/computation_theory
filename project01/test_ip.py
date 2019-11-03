#-------------------------------------
# experiment1
# the file finish the first experiment of recogizing ip addresses
# author: Ship Xu
#         Xiaohan Hou
#-------------------------------------
import re

def ip_match(input_string):
    """match string that is ip address format 

    Args:
        input_string: the string that is prepared to be tested

    Returns:
        a boolean variable to define whether the ip address was matched or not.

    Raises:
    """
    pattern_string ='(([1-9])\.|([1-9][0-9])\.|(1\d\d)\.|(2[0-4]\d)\.|(25[0-5])\.)(([1-9]?\d)\.|(1\d\d)\.|(2[0-4]\d)\.|(25[0-5])\.){2}(([1-9]?\d)|(1\d\d)|(2[0-4]\d)|(25[0-5]))$'
    match_ret = re.match(pattern_string, input_string)
    return match_ret is not None


if __name__ == '__main__':
    with open('ip.txt') as file:
        for line in file.readlines():
            if (ip_match(line)):
                print('matched and matched result {}'.format(line.replace('\n', '')))