from constants import ROOT_DIR, PUBLIC_DIR, STATIC_DIR
import os 
import shutil

def copy_directory(src = STATIC_DIR, dst = PUBLIC_DIR):

    for entry in os.listdir(src):
        entry_src = os.path.join(src, entry)
        if os.path.isdir(entry_src):
            entry_dst = os.path.join(dst, entry)
            os.mkdir(entry_dst)
            copy_directory(entry_src, entry_dst)
        elif os.path.isfile(entry_src):
            shutil.copy(entry_src, dst)

def clean_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)