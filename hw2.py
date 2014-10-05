'''
OPERATING SYSTEMS - HOMEWORK 2
PROCESS MANAGEMENT SIMULATION SYSTEM

Zachary Vanderzee
Rocco Del Priore
Caitlin Connerney
'''

import random
import operator

numberOfProcesses = 12

# Process Class
class process:
	# Constructor for a Process
	def __init__(self, p, t, b, i):
		self.pid 	= p      		# Process ID
		self.time = t 				# Time it takes to complete 20-200ms or 200-3000ms
		self.turn = 0				# Total Time taken to complete
		self.wait = 0				# Time spent in Queue
		self.priority = 0			# Priority Level
		self.bursts = b 			# Bursts it takes to complete
		self.inter = i 				# Interactive Process or not

	# Simple print function for debugging
	def printP(self):
		print(self.pid,self.time,self.turn,self.wait,self.priority,self.bursts,self.inter)
	
	# Returns whether a process has finished or not
	def done(self):
		if self.bursts == 0:
			True
		else:
			False

def printProcess(time, p, pType):
	print "[time ",time,"ms] ",pType," with process ID ",p.pid," has terminated (turnaround time ", p.turn, "ms wait time ", p.wait,"ms)"
	pass

#	Shortest Job First without Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def SJFN( processes ):
	# Put all processes in Queue
	queue = []
	for p in processes:
		queue.append(p)
	# Sort the list by the completion time
	queue.sort(key=operator.attrgetter('time'))
	for p in queue:
		pType = ""
		if p.inter:
			pType = "Interactive"
		else:
			pType = "CPU-bound"
		printProcess(0, p, pType)
	# Simulate processing
	time = 0
	while len(queue) != 0:
		p = queue.pop(0)
		p.wait = time
		time += p.time
		p.turn = time
		printProcess(time, p, "Process")

'''
#	Shortest Job First with Preemption algorithm
# Takes in a list of processes and puts them into a que to run
def	SJFP( processes, time ):'''


# Round Robin algorithm
# Takes in a list of processes and puts them into a que to run
def RR( processes):
	# Put all processes in Queue
	queue = []
	for process in processes:
		queue.append(p)
		pType = ""
		if process.inter:
			pType = "Interactive"
		else:
			pType = "CPU-bound"
		printProcess(0, process, pType)

	tLimit = 100 											#This is the time in miliseonds spent on each portion of the RR
	totalTime = 0											#This is the total time spent on the operation
	while len(processes) > 0:								#While there are active processes run
		for process in processes:							#Each Round Robin loop
			timeDifference = process.time-process.turn
			if timeDifference > tLimit:
				process.turn +=tLimit
				totalTime += tLimit;
			else:
				process.turn = process.time
				totalTime += timeDifference;
				queue.remove(process)
				printProcess(totalTime, process, "Process")


#	Preemptive Priority alorithm
# Takes in a list of processes and puts them into a que to run
'''def PP( processes, time ):


# Function to incrememnt the times for the process in the queue
def inc( processes ):
	for p in processes:
		turn += 1


#	Simulate takes in 2 parameters and runs simulates all scheduling algorithms
#		int m = number of CPUs. Should be be 1 or 4
#		int n = number of Processes. The default value is 12
def simulate( m, n ):

'''

def main():
	one 	= process(1,100,1,True)
	two 	= process(2,3000,8,False)
	three = process(3,350,8,False)
	processes = [one,two,three]
	SJFN(processes)

if __name__ == '__main__': 
	main()