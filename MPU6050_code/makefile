LIB_DIR = lib

default: pyMPU6050

pyMPU6050: setup.py pyMPU6050.pyx $(LIB_DIR)/libMPU6050.a
	python3 setup.py build_ext --inplace && rm -f pyMPU6050.c && rm -Rf build

$(LIB_DIR)/libMPU6050.a:
	make -C $(LIB_DIR) libMPU6050.a

clean:
	rm *.so