import os,shutil
import glob


def clean_build():
    paths=[f"./build",f'./*.egg-info']
    for p in paths:
        for path in glob.glob(p):
            shutil.rmtree(path, ignore_errors=True)


def build_package(outdir = "dist" ,only_wheel = False, clean=True):
    outdir = "dist"
    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    
    opt=""
    if only_wheel:
        opt += "--wheel"
    opt += f" --outdir {outdir}"
    os.system(f"python -m build {opt}")

    if clean:
        clean_build()

def install_wheels(wheels_dir = "dist"):
    
    weels=[w for w in os.listdir(wheels_dir) if w.endswith('.whl')]
    for we in weels:
          os.system(f'pip install --force-reinstall {wheels_dir}/{we} ')
    
    clean_build()

outdir = "dist"   

build_package(outdir=outdir)
# install_wheels(wheels_dir=outdir)
