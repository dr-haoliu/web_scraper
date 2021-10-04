# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re
import os
import csv

# read a file

import spacy
from pysbd.utils import PySBDFactory

def sentence_segment(sents_text):
    nlp = spacy.blank('en')

    # explicitly adding component to pipeline
    # (recommended - makes it more readable to tell what's going on)
    nlp.add_pipe(PySBDFactory(nlp))

    # or you can use it implicitly with keyword
    # pysbd = nlp.create_pipe('pysbd')
    # nlp.add_pipe(pysbd)
    # sents = 'My name is Jonas E. Smith. Please turn to p. 55.'
    doc = nlp(sents_text)
    for sen in list(doc.sents):
        print(sen)
    # [My name is Jonas E. Smith., Please turn to p. 55.]
    return list(doc.sents)


def test_re(filename=''):
    path = "data/extracted"
    filenames = []
    pmid_sents_list=[]
    error_files_list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            # filenames.append(os.path.join(root, file))
            if file.endswith(".txt"):
                filenames.append(os.path.join(root, file))

    print("Processing txt in {} files".format(len(filenames)))


    for filename in filenames:
        print('processing file: ', filename)

        results = re.search('\d+', filename)
        if results:
            pmid = results.group()
            print(pmid)
        # f = open(filename, encoding='utf8')
        # filename = 'data/extracted/abstract-32496357.txt'
        # filename = 'data/extracted/abstract-32501511.txt'
        textfile = open(filename, 'r')
        filetext = textfile.read()
        textfile.close()
        p = re.compile(r'(^CONCLU.*):((?:[^\n][\n]?)+)', re.M)
        matches = re.findall(p, filetext)
        if matches:
            for match in matches:
                my_text = '{}: {}'.format(match[0], match[1].replace('\n', '').strip())
                my_text_2 = '{}'.format(match[1].replace('\n', '').strip())
                print(my_text)
                sent_list = sentence_segment(my_text_2)
                for sent_i in sent_list:
                    pmid_sents_list.append([pmid, sent_i])
        else:
            error_files_list.append(filename)

    print('*********************************************')
    write_to_tsv(pmid_sents_list)
    print('*********************************************')
    for err_file in error_files_list:
        print(err_file)


def write_to_tsv(mylist, out_file=''):
    out_file = 'data/output_2.tsv'
    with open(out_file, mode='w', newline='', encoding='utf8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['pmid', 'sentence'])
        for ps in mylist:
            print(ps)
            csv_writer.writerow(ps)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    test_re()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
