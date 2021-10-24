import shutil


def copy_files(src_dir, dest_dir):
    shutil.copytree(src_dir, dest_dir)
