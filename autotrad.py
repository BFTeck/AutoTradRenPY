
import os
import platform
import shutil
#from googletrans import Translator
from pygoogletranslation import Translator
import time

# On cherche les fichiers de RPY dans le répertoire donnée
# on fait un backup de ces fichiers
# on les lit et on rempli les new avec les traductions

def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


def search(pathofproject):
    listofrpyinside=[]
    chemincompletinside=""
    for path, dirs, files in os.walk(pathofproject):

        for filefound in files:
            fileName, fileExtension = os.path.splitext(os.path.basename(filefound))
            if fileExtension == ".rpy":
                if platform.system() == 'Linux':
                    chemincompletinside = path + '/' + filefound
                elif platform.system() == 'Windows':
                    chemincompletinside = path + '\\' + filefound
                else:
                    chemincompletinside = path + '/' + filefound
                listofrpyinside.append(chemincompletinside)


    return  listofrpyinside

pathofproject = input('Repertoire des fichiers ? (Generalement un truc du genre game\\tl\\french_fr) => ')

sauvegarde = input("Creation d'une sauvegarde Y/N ?")
restoration = input("Restoration d'une sauvegarde Y/N ?")

if sauvegarde == "Y" or sauvegarde == "y" or sauvegarde == "O" or sauvegarde == "o":
    sauvegarde = True
else:
    sauvegarde = False

if restoration == "Y" or restoration == "y" or restoration == "O" or restoration == "o":
    restoration = True
else:
    restoration = False

listofrpyfiles = search(pathofproject)

if sauvegarde == True:
    for file in listofrpyfiles:
        shutil.copyfile(file, file+'.bak')

if restoration == True:
    for file in listofrpyfiles:
        shutil.copyfile(file+'.bak', file)

translator = Translator()
exception=[]
print("Premier Passage: Traitement des phrases")
print("---------------------------------------")
for file in listofrpyfiles:
    #print("--Traitement de : "+file)
    #os.remove(file)
    if os.path.exists(file + '.tmp') == False:
        shutil.copyfile(file, file + '.tmp')
    fref = open(file+'.tmp', 'r', encoding="utf_8_sig")
    ftrad = open(file, 'w', encoding="utf_8_sig")
    lineprec=""
    for line in fref:
        # print(line)
        if ' ""' in line:
            #print("A Traduire:"+lineprec)
            atraduire = lineprec.strip()
            atraduire = atraduire[atraduire.find('"')+1:len(atraduire)-1]
            if "{" not in atraduire:
                if "[" not in atraduire:
                    if "(" not in atraduire:
                        atraduire = atraduire.replace(' you ',' thou ')
                        atraduire = atraduire.replace(' you.', ' thou.')
                        atraduire = atraduire.replace(' you?', ' thou?')
                        atraduire = atraduire.replace(' you!', ' thou!')

                        if len(atraduire) < 5:
                            traduction = ""
                            exception.append(atraduire)
                        elif len(atraduire) < 15 and " " not in atraduire:
                            traduction = ""
                            exception.append(atraduire)
                        else:
                            traduit = translator.translate(atraduire, dest='fr', src='en')
                            traduction = traduit.text
                            time.sleep(1)  # Sleep for 1 seconds
                        traduction = traduction.replace('...','___')
                        traduction = traduction.replace('. ', '.')
                        traduction = traduction.replace('.', '. ')
                        traduction = traduction.replace(' !', '!')
                        traduction = traduction.replace('!', ' ! ')
                        traduction = traduction.replace(' ?', '?')
                        traduction = traduction.replace('?', ' ? ')
                        traduction = traduction.replace('___', '...')
                        traduction = traduction.strip()
                        line = line.replace('""', '"'+traduction+'"')
                    else:
                        traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                        line = line.replace('""', '"' + traductionmanuelle + '"')
                else:
                    traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                    line = line.replace('""', '"' + traductionmanuelle + '"')
            else:
                traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                line = line.replace('""', '"' + traductionmanuelle + '"')
        ftrad.write(line)
        lineprec = line

    fref.close()
    ftrad.close()
    os.remove(file + '.tmp')

print("---------------------------------------")

atraduire="   "
i=0
j=0
traduit=""
easytrad={}
for element in exception:
    i = i+1
    j = j + 1
    element=element.strip()
    element=element.replace("/","__")
    if i < 16 and element !="":
        atraduire = atraduire + element + " \n "
    elif len(exception) - j < 10 and element !="":
        atraduire = atraduire + element + " \n "
    else:
        if element !="":
            atraduire = atraduire + element + " \n "
        if atraduire != "":
            atraduire = atraduire[:len(atraduire)-3]
            atraduire = atraduire.strip()
            traduction = translator.translate(atraduire, dest='fr', src='en').text

            tabatraduire = atraduire.split("\n")
            tabtraduction = traduction.split("\n")

            if len(tabatraduire) == len(tabtraduction):
                for x in range(0, len(tabtraduction)):
                    if tabatraduire[x].strip() not in easytrad.keys():
                        easytrad[tabatraduire[x].strip()] = tabtraduction[x]

            i = 0
            atraduire = ""


if atraduire != "":
    atraduire = atraduire[:len(atraduire) - 3]
    atraduire = atraduire.strip()
    traduction = translator.translate(atraduire, dest='fr', src='en').text

    tabatraduire = atraduire.split("\n")
    tabtraduction = traduction.split("\n")

    if len(tabatraduire) == len(tabtraduction):
        for x in range(0, len(tabtraduction)):
            if tabatraduire[x] not in easytrad.keys():
                easytrad[tabatraduire[x].strip()] = tabtraduction[x]




print("Deuxième Passage: Traitement des mots seuls")
print("---------------------------------------")

for file in listofrpyfiles:
    #print("--Traitement de : "+file)
    if os.path.exists(file + '.tmp') == False:
        shutil.copyfile(file, file + '.tmp')
    fref = open(file+'.tmp', 'r', encoding="utf_8_sig")
    ftrad = open(file, 'w', encoding="utf_8_sig")
    lineprec=""
    for line in fref:
        # print(line)
        if ' ""' in line:
            #print("A Traduire:"+lineprec)
            atraduire = lineprec.strip()
            atraduire = atraduire[atraduire.find('"')+1:len(atraduire)-1]
            if "{" not in atraduire:
                if "[" not in atraduire:
                    if "(" not in easytrad:
                        atraduire=atraduire.strip()
                        if atraduire in easytrad:
                            traduction=easytrad[atraduire]
                            traduction = traduction.replace('...', '___')
                            traduction = traduction.replace('. ', '.')
                            traduction = traduction.replace('.', '. ')
                            traduction = traduction.replace(' !', '!')
                            traduction = traduction.replace('!', ' ! ')
                            traduction = traduction.replace(' ?', '?')
                            traduction = traduction.replace('?', ' ? ')
                            traduction = traduction.replace('___', '...')
                            traduction = traduction.strip()
                            line = line.replace('""', '"' + traduction + '"')
                        else:
                            traductionmanuelle = input('Comment traduire "'+atraduire+'" ? => ')
                            line = line.replace('""', '"' + traductionmanuelle + '"')




                    else:
                        traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                        line = line.replace('""', '"' + traductionmanuelle + '"')
                else:
                    traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                    line = line.replace('""', '"' + traductionmanuelle + '"')
            else:
                traductionmanuelle = input('Comment traduire "' + atraduire + '" ? => ')
                line = line.replace('""', '"' + traductionmanuelle + '"')
        ftrad.write(line)
        lineprec = line

    fref.close()
    ftrad.close()
    os.remove(file + '.tmp')

print("---------------------------------------")