from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

MPU6050_extension = Extension(
    name="pyMPU6050",
    sources=["pyMPU6050.pyx"],
    libraries=["MPU6050"],
    library_dirs=["lib"],
    include_dirs=["lib"]
)

setup(
    name="pyMPU6050",
    ext_modules=cythonize([MPU6050_extension])
)