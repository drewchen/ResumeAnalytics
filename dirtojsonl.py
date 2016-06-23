try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile
import os
import json

"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

def _docx_to_txt(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    try:
        document = zipfile.ZipFile(path)
    except BadZipFile as e:
        print (path)
        print (" is not a valid zip file")
        raise e
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)

"""
End Module
"""

def _pdf_to_txt(root_dir):
    ''' convert all pdfs in root_dir to text including sub dirs
    '''
    for root, _, files in os.walk(root_dir):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext == '.pdf':
                 os.system(('pdftotext "%s"') % os.path.join(root, f))


def _txt_to_jsonl(root_dir, outpath):
    ''' collect textfiles in root_dir and write them to jsonl
        remove textfiles after writing content to file
    '''
    def _file_path_iter(source_dir):
        ''' keep only one file in memory at a time
        '''
        return ((f, os.path.join(root, f))
                for root, dirs, files in os.walk(source_dir)
                for f in files if os.path.splitext(f)[1] == '.txt'
               )

    with open(outpath, 'w') as outf:
        for f, path in _file_path_iter(root_dir):
            with open(path, 'r', encoding='utf-8', errors='ignore') as inf:
                    json.dump({'name': f, 'content': inf.read()}, outf)
                    outf.write('\n')
            os.remove(path)
        ## Also here, add all found docx files to the outf file
        for root, _, files in os.walk(root_dir):
            for f in files:
                _, ext = os.path.splitext(f)
                if ext == '.docx':# or ext == '.doc':
                    json.dump({'name': f, 'content': _docx_to_txt(os.path.join(root, f))}, outf)
                    outf.write('\n')


def process_directory(in_dir, out_path):
    ''' wrap it all up
    '''
    _pdf_to_txt(in_dir)
    _txt_to_jsonl(in_dir, out_path)


