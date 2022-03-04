# 2D Soccer Simulation xG
This repo contains a baseline implementation for an expected goals model for the 2D simulation category of the RoboCup.

## Dataset
Over 400 log files from matches between 2019 and 2021 were analyzed producing 2 different datasets:
* [2019+2021 without Anonymous Challenge](https://github.com/tta13/2D-soccer-simulation-xG/blob/main/database/data/database_2019%2B2021.csv): contains just under 6000 entries (shots)
* [2021 with Anonymous Challenge](https://github.com/tta13/2D-soccer-simulation-xG/blob/main/database/data/database_2021(%2BAnonymousChallenge).csv): contains just over 6200 entries (shots).

The datasets are separated because the Anonymous Challenge produced more random results and situations, but both have the same **features**:
* x: x position on the pitch (absolute value)
* y: y position on the pitch (if the shot ocurred on the left side, the value is multiplied by -1)
* distance: distance from the shot position to the goal center
* angle: angle between player, left post and right post
* players_in_between: players inside the triangle with vertices used by the angle described above
* goal: was it a goal?

## Model
Implemented used the logistic function and based on the variables _angle_, _distance_ and _players_in_between_, since those minimized the p-values from the model and gave it good predictive power.

## What can improve?
* Shooting identification algorithm
* Introduce more variables: _counter-attack_, _came_from_cross_, _score_, _time_...
