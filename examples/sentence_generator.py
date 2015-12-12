# -*- coding: utf-8 -*-

from markhov import MarkhovChain
import string
import re
import pdb

some_file = './some_text.txt'
text = open(some_file, 'r', encoding='utf-8').read()

TERMINATORS = "?!."
THROW_AWAYS = string.punctuation.translate(dict((ord(x), None) for x in TERMINATORS))
text = text.translate(dict((ord(x), None) for x in THROW_AWAYS if x not in ",;"))
text = re.sub("([" + string.punctuation + "])", " \\1", text)
text = text.split()
mc = MarkhovChain()

last = ""
for i in range(len(text)):
    mc.add_transition(last, text[i])
    last = text[i]

if not mc.has_state(text[-1]) or not mc.has_next_state(text[-1]):
	mc.add_transition(text[-1], "")

mc.set_state("")

print(re.sub(" ([" + "\\".join(string.punctuation) + "])", \
	"\\1", " ".join(mc.next_state() for _ in range(35))))
