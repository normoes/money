# coding: utf8

class ServerConfiguration():
    pass

def get_additional_files_to_watch(path):
    extra_dirs = [path,]
    extra_files = extra_dirs[:]
    import os
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            filenames = [os.path.join(dirname, name) for name in files if os.path.splitext(os.path.join(dirname, name))[1] == '.py' ]
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)
    return extra_files
