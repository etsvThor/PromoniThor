import os
import uuid

def get_ext(filename):
    return filename.split(".")[-1].lower()

def file_delete_default(sender, instance, **kwargs):
    try:
        instance.File.delete(False)
    except:
        #in case the file is locked by another process.
        print("Error in removing the file. Only the object will be removed.")


def metro_icon_default(object):
    extension = get_ext(object.File.name)
    if extension == 'pdf':
        return 'pdf'
    elif extension in ['doc', 'docx', 'odf','rtf']:
        return 'word'
    elif extension in ['jpg', 'jpeg','png','bmp','gif']:
        return 'image'
    elif extension in ['xls', 'xlsx', 'ods']:
        return 'excel'
    elif extension in ['ppt','pptx','odp']:
        return 'powerpoint'
    elif extension in ['tex']:
        return 'code'
    elif extension in ['zip','rar','gz']:
        return 'archive'
    elif extension in ['txt']:
        return 'text'
    return 'empty'

def filename_default(filename):
    ext = filename.split('.')[-1]
    return "%s.%s" % (uuid.uuid4(), ext)