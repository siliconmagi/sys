import re

str = 'beginning middle end'
print(re.findall(r'beginning(.*?)end', str)[0])
