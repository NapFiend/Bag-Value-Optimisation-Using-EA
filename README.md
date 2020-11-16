# Bag-Value-Optimisation-Using-EA
This evolutionary algorithm seeks to find an optimal solution to fitting as many bags of varying values and wights into a van with a weigth limit

Working for a bank, you have been asked to develop an evolutionary algorithm basedsystemwhich will find the largest amount of money that can be packed into a security van. 

The money is separated into 100 bags of different denominations and the weight and value of the money of each bag is shown on the outside of the bag.  
e.g.  Bag 1 Value = £94, Weight = 5.7KgBag 2 Value = £74, Weight = 9.4Kg...Bag N Value = £x, Weight = iKg

The security van can carryonly a limited weight, so your system must try and decide which bags to put on the van, and which ones to leave behind.  The best solution will be the one which packs the most money (in terms of value) into the van without overloading it. 
Your system shouldread in the 100 bag values

The file contains the weight limit for the security van and the values and weights for each bag of money.  Weights are all in kilos and the values are all in pounds sterling.

You must decide how to represent this problem to the evolutionary algorithm, you must also decide what the fitness function should be.
