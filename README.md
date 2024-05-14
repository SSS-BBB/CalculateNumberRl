## Calculate Number Environment
First, the game will random some target number, given number, current result. The goal of the Ai is to operate(+, -, *, /) the current result with the given number to get as near to the target as possible. After the action is chosen the current result will change according to the action the ai choose, and the new number will be given.
And if the Ai thinks the current result is close to the target enough, the can choose to give up and the game will end. If the difference between the target number and the current result is lower than 0.01 the game will also end.

## Result
The result is quite good, but not the best. In each step the ai tried to get as close to the target as possible and give up.
Some model decides not to give up at all because they know that if the difference between the target number and the current result is lower than 0.01, they will get 100 rewards.
