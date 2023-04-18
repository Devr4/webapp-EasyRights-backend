# import deepl
from googletrans import Translator
import json
import re


# translation = translator.translate("ciao mondo")
# print(translation)

translator = Translator()

def trans(a: str):
    global translator
    # return deepl.translate(source_language="EN", target_language="AR", text=a)
    translated = translator.translate(a, src='en', dest='uk')
    return translated.text


with open("to_trans", encoding="utf-8") as f:
    lines = f.read().splitlines()

regex = r"\"(.+)\","
for i, line in enumerate(lines):
    if "label:" in line or "helperText:" in line or "title:" in line:
        x = re.findall(regex, line)
        if x:
            string = x[0]
            translated = trans(string)
            lines[i]=line.replace(string, translated)





with open("ukranian", "w", encoding="utf-8") as f:
    f.write('\n'.join(lines))