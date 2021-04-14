# Installing Python 3.9.4
Python 3.9.4 can be downloaded [here](https://www.python.org/downloads/release/python-394/)

# Installing the Z3 theorem prover on MacOS via terminal.
## Building Z3 using make and GCC/Clang

```
git clone https://github.com/Z3Prover/z3.git
cd z3
python3 scripts/mk_make.py --python
cd build
make
sudo make install
```

## Install the Python wrapper
```
pip3 install z3-solver
```

## Check if installed correctly
```
z3 --version
```

Note: For code to compile correctly, z3 version must be 4.8.11
