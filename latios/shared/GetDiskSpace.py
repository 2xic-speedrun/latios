import shutil

def get_free_disk_space_in_gb():
    _, _, free = shutil.disk_usage("/")

    return free // (2**30)
