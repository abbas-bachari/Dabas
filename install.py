import os,shutil
import glob

def clean_pycache(root_dir="."):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            cache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(cache_path)
            print(f"📌 Deleted: {cache_path}")

def clean_build():
    paths=[f"./build",f'./*.egg-info']
    for p in paths:
        for path in glob.glob(p):
            shutil.rmtree(path, ignore_errors=True)
            print(f"📌 Deleted: {path}")


def build_package(outdir = "dist" ,only_wheel = False):
    outdir = "dist"
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
        print(f"📌 Deleted: {outdir}")
    
    opt=""
    if only_wheel:
        opt += "--wheel"
    opt += f" --outdir {outdir}"
    os.system(f"python -m build {opt}")

    

def install_wheels(wheels_dir = "dist"):
    
    weels=[w for w in os.listdir(wheels_dir) if w.endswith('.whl')]
    for we in weels:
          os.system(f'pip install --force-reinstall {wheels_dir}/{we} ')
    
    clean_build()



def install(install=True,upload=False, clean=True ,outdir = "dist"):
    
    clean_pycache()
    build_package(outdir=outdir)
    
    if clean is True:
        clean_build()

    
    if install is True:
        install_wheels(wheels_dir=outdir)
    
    
    
    if upload is True:
        os.system(f'twine upload --config-file .pypirc {outdir}/*')
    
    




if __name__ == "__main__":
    
    install()



