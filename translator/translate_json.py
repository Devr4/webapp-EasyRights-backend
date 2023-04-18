# import deepl
from googletrans import Translator
import json


# translation = translator.translate("ciao mondo")
# print(translation)

translator = Translator()

def trans(a: str):
    global translator
    # return deepl.translate(source_language="EN", target_language="AR", text=a)
    translated = translator.translate(a, src='en', dest='ta')
    return translated.text


with open("english.json", encoding="utf-8") as f:
    json_en=json.load(f)

# translate to Italian
for k in json_en["questions"]:
    if "label" in k.keys():
        k["label"] = trans(k["label"])
    if "title" in k.keys():
        k["title"] = trans(k["title"])
    if "answers" in k:
        for j in k["answers"]:
            if "label" in j.keys():
                j["label"] = trans(j["label"])
            if "helperText" in j.keys() and j["helperText"]!="":
                try:
                    j["helperText"] = trans(j["helperText"])
                except:
                    pass

with open("tamil.json", "w", encoding="utf-8") as f:
    json.dump(json_en, f)