'''
OPERATING SYSTEMS - HOMEWORK 2
PROCESS MANAGEMENT SIMULATION SYSTEM

Zachary Vanderzee
Rocco Del Priore
Caitlin Connerney
'''

import random

# Process Class
class process:
	pid 			= 0		# Process ID
	burst 		= 0		# Time it takes to complete
	turn 			= 0		# Total Time taken to complete
	wait 			= 0		# Time spent in Queue
	priority 	= 0		# Priority Level


#	Shortest Job First without Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def SJFN( processes, time ):
	


#	Shortest Job First with Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def	SJFP( processes, time ):


# Round Robin algorithm
# Takes in a list of processes and puts them into a que to run
def RR( processes, time ):


#	Preemptive Priority alorithm
# Takes in a list of processes and puts them into a que to run
def PP( processes, time ):


# Function to incrememnt the times for the process in the queue
def inc( processes ):
	for p in processes:
		turn += 1


#	Simulate takes in 2 parameters and runs simulates all scheduling algorithms
#		int m = number of CPUs. Should be be 1 or 4
#		int n = number of Processes. The default value is 12
def simulate( m, n ):
