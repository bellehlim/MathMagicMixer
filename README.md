# Math Magic Mixer Solver

![](https://images-na.ssl-images-amazon.com/images/I/51I%2BBA18wzL._AC_.jpg)

Math Magic Mixer is a toy intended to teach children basic arithmetic. It consists of a flower-shaped “mixer” with six surrounding dice and one in the center. The six outer dice have the numbers 1 through 6 on their sides, and one of these dice is black. The black die in the center has numbers 5-30 in increments of 5. The objective of the game is to sum the black dice to get a “target” and then combine the remaining 5 dice using various arithmetic operations (addition, subtraction, multiplication, and division) to achieve the target. The player must use all 5 dice in their solution and cannot repeat dice 

Utilizing Z3 Solvers, our project can find all possible solutions to a standard game of Math Magic Mixer.


# Setup 
## Installing Python 3.9.4
Python 3.9.4 can be downloaded [here](https://www.python.org/downloads/release/python-394/)

## Installing the Z3 theorem prover on MacOS via terminal.
Building Z3 using make and GCC/Clang

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

# Running the Program
Open up a Python IDE like IDLE. Download **MathMagicMixer_v2.py** and Run it. You can now call the function *for5terms* and provide it your target number, a number 6 through 36, and your list of five other dice values, 1 through 6, in an array with square brackets. 

An example call would be *for5terms(23, [1,2,4,5,6])* representing a target number of 23 and the 5 remanining numbers as 1, 2, 4, 5, and 6. Running this command begins the program which currently takes on the magnitude of 3 minutes to run.
