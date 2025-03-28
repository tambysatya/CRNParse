
# CRNParse: a tool to parse and simulate SBML files and build the corresponding ODE system

## Extracting the symbolic ODEs

```
python crnsym.py -i <input> -o <output>
```

example:

```
python main.py -i example1.xml -o example1.txt
```

## Simulating an SBML file

```
python datagen.py -i <input> -o <output> -ts <time points>
```

example:

```
python datagen.py -i example1.xml -o example1.pt -ts 1 2 5 7
```

other options include `-t0 <initial time point>` and `-dt0 <initial time step`

see `--help` for a list of options


## TODO

- custom starting point
- parameter optimization
- JIT compilation 
- better API interface

