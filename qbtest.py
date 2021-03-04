# hr test.py

import re

xp = r"(http(s)?:\/\/([a-z0-9-_]+\.([a-z0-9]*\.)*[a-z]{2,}))"
tstr = "blah blah http://foo.com is my mom and https://www.foostar.net or https://first.second.third.net nad http://banana.foo.com/bar dont match.me.com"

print('tstr',tstr)
all = re.findall(xp, tstr)
print(all)
print (list(m[0] for m in all))


print('tstr',tstr)
s = re.search(xp, tstr)
print(s)
print(s.groups())
