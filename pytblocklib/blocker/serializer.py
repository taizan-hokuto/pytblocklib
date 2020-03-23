import base64
import json
import os
import pickle
import re

PATTERN  = re.compile(r"(.*)\(([0-9]+)\)$")

class Serializer:
    '''
    Serializer saves any objects as base64 encoded text file.
    Parameter
    ---------
    filepath : str :
        The path of file to save objects.
    '''
    def __init__(self,filepath):
        self.filepath = filepath

    def _serialize_obj(self,obj) -> str:
        return base64.b64encode(pickle.dumps(obj)).decode("utf-8")

    def _deserilize_obj(self, string):
        return pickle.loads(base64.b64decode(string.encode()))

    def save(self, obj):
        '''
        Save objects. 
        Parameter
        ---------
        obj :
            Object to be saved. 
            If specified object is list, each item in object is saved. 
        '''
        with open(self.filepath,encoding='utf-8',mode='a',newline="\n") as f:
            if isinstance(obj,list):
                f.write('\n'.join([self._serialize_obj(o) for o in obj]))
                f.write('\n')
            else:
                f.writelines(self._serialize_obj(obj))
                f.write('\n')

    def load(self):
        '''
        Load objects. 
        '''
        try:
            with open(self.filepath, encoding='utf-8', mode='r') as f:
                return [self._deserilize_obj(line) for line in f]
        except FileNotFoundError:
            print("File not found:",self.filepath)

    def _checkpath(self, filepath):
        splitter = os.path.splitext(os.path.basename(filepath))
        body = splitter[0]
        extention = splitter[1]
        newpath = filepath
        counter = 0
        while os.path.exists(newpath):
            match = re.search(PATTERN,body)
            if match:
                counter=int(match[2])+1
                num_with_bracket = f'({str(counter)})'
                body = f'{match[1]}{num_with_bracket}'
            else:
                body = f'{body}({str(counter)})'
            newpath = os.path.join(os.path.dirname(filepath),body+extention)
        return newpath

