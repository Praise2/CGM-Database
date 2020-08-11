"""
This is just a test for pull request on pycharm
"""

import base64

with open("Exit_icon.jpg", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string)

new1 = base64.b64decode(my_string)
#new1 = my_string.decode('utf-8')
print(new1)


