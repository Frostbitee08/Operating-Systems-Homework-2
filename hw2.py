'''
OPERATING SYSTEMS - HOMEWORK 2
PROCESS MANAGEMENT SIMULATION SYSTEM

Zachary Vanderzee
Rocco Del Priore
Caitlin Connerney
'''

import random
import operator

# Process Class
class process:
	# Constructor for a Process
	def __init__(self, p, t, b, i):
		self.pid 	= p      		# Process ID
		self.time = t 				# Time it takes to complete 20-200ms or 200-3000ms
		self.turn = 0					# Total Time taken to complete
		self.wait = 0					# Time spent in Queue
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

# Print Function to handle all the if statements when printing
# Case 1: Process entry 
# Case 2: Context switch
# Case 3: Process CPU burst completion
# Case 4: Process termination
# Case 5: Aging event
def masterPrint(time,case,p):
	if case == 1:
		if p.inter:
			print "[time",time,"ms] Interactive process ID",p.pid,"entered ready queue (requires",p.time,"ms CPU time)"
		else:
			print "[time",time,"ms] CPU-bound process ID",p.pid,"entered ready queue (requires",p.time,"ms CPU time)"
	elif case == 2:
		print "To be implimented"
	elif case == 3:
		print "To be implimented"
	elif case == 4:
		if p.inter:
			print "[time",time,"ms] Interactive process ID",p.pid,"has terminated (turnaround time", p.turn, "ms wait time", p.wait,"ms)"
		else:
			print "[time",time,"ms] CPU-bound process ID",p.pid,"has terminated (turnaround time", p.turn, "ms wait time", p.wait,"ms)"
	else:
		print "To be implimented"

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
		masterPrint(0,1,p)
	# Simulate processing
	time = 0
	while len(queue) != 0:
		p = queue.pop(0)
		p.wait = time
		time += p.time
		p.turn = time
		masterPrint(time,4,p)

'''
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

'''

def main():
	# Just some test stuff
	processes = []
	for pid in range(1,13):
		q = random.randint(1,101)
		if q < 21:
			processes.append(process(pid,random.randint(200,3001),8,False))
		else:
			processes.append(process(pid,random.randint(20,201),1,True))
	SJFN(processes)

if __name__ == '__main__': 
	main()