#  Minimize Surprise: Self-Assembly Scenario (2D torus grid world)

## Running one Evolutionary Run in the Simulation

```
.\main EVOL [Grid length in x-direction] [Grid length in y-direction] PRED [Manipulation: None / MAN / PRE ] [Manipulation Parameter]
```

## Manipulation

* None: Minimize Surprise with complete freedom
* MAN: partially predefined predictions
* PRE: predefined predictions



## Manipulation Parameter

* if Manipulation = None: specify random parameter (will be ignored)
* LINE: aiming for grouping and lines (MAN) and for lines (PRE)
* PAIR: aiming for pairs 
* DIAMOND: aiming for triangular lattices
* SQUARE: aiming for squares
* AGGREGATION: aiming for grouping
* DISPERSION: aiming for dispersion 

## Sensor Models

The sensor model is set by default to STDL. 
Changing the sensor model is possible by including the respective header file in main.c. 

* STD6: 6 sensors in heading direction 

            . . .
            . . .
              X

* STD14: 14 sensors 

        . . .
        . . .
        . X .
        . . .
        . . .

* STD8: 8 sensors (Moore neighborhood)

        . . .
        . X .
        . . .
