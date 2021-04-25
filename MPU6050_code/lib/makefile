CC = gcc

default: libMPU6050.a

libMPU6050.a: MPU6050.o
	ar rcs $@ $^

MPU6050.o: MPU6050.c MPU6050.h
	$(CC) -c $<

clean:
	rm *.o *.a

