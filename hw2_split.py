''' OPERATING SYSTEMS - HOMEWORK 2
		PROCESS MANAGEMENT SIMULATION SYSTEM

		Zachary Vanderzee
		Rocco Del Priore
		Caitlin Connerney
'''

import random
import operator
import sys
import heapq
import copy

class process:
	""" Process Class
	"""
	def __init__(self, a, b, c ):
		""" Constructor for a Process with 
					* ID a 
					* priority level b
					* c bursts
				All other attributes default to zero
		"""
		self.pid								= a #Process ID
		self.completion					=	0 #Required CPU time to complete burst
		self.turnaround					=	0 #Total time taken	to complete burst	
		self.wait								=	0 #Total time spent in ready queue waiting for burst
		self.priority						=	b #Priority Level
		self.burstsRemaining		=	c #Number of CPU bursts remaining (-1 for Interactive)
		self.timeSlice					=	0 #Time alloted in CPU
		self.block							=	0 #Time spent waiting for human input or I/O blocking
		self.initpri						= b #Initial priority so we can reset priority if it changes
		#The Following are lists to keep track of the history of attributes through different bursts
		self.totalWaits					= [] #List of wait times
		self.totalTurns					= [] #List of turn around times

	def __cmp__(self, other):
		"""	Overoaded cmp operator for priority queue application
				Prioritizes time left blocking -> time remaining in CPU burst -> Completion Time -> 
				When not waiting, wait should be set to 0 and when not in CPU, burst should be set to 0 
		"""
		return cmp((self.block, self.priority, self.completion), (other.block, other.priority, other.completion))

	def __hash__(self):
		"""	Makes processes hashable by its unique process ID
		"""
		return self.pid

	def averageTurn(self):
		""" Returns the average Turnaround time for the process
		"""
		return sum(self.totalTurns)/float(len(self.totalTurns))

	def averageWait(self):
		""" Returns the average wait time for the process
		"""
		return sum(self.totalWaits)/float(len(self.totalWaits))

	def totalCPU(self):
		""" Returns the total time spent in the CPU across all bursts
		"""
		return sum(self.totalTurns)-sum(self.totalWaits)

	def totalWait(self):
		""" Returns the total time spent waiting in the ready queue
		"""
		return sum(self.totalWaits)

	def assignCompletion(self):
		""" Assigns a completion time depending on process type
				Uses random.randint(a,b)
		"""
		if self.burstsRemaining < 0:
			self.completion = random.randint(20,200)
		else:
			self.completion = random.randint(200,3000)

	def assignBlock(self):
		""" Assigns a wait time depending on process type
				Uses random.randint(a,b)
		"""
		if self.burstsRemaining <= -1:
			self.block = random.randint(1000,4500)
		else:
			self.block = random.randint(1200,3200)

	def output(self,case,flag,time):
		""" Prints the out put for our SIMULATION
				Cases:
					1: Process Entry
					3: CPU burst completion
					4: Process termination
					5: Aging Event
				Flag:
					0: Display Priority
					1: Do not display Priority
		"""
		s = ""
		if case == 1:
			if self.burstsRemaining >= 0:
				s += ("[time "+str(time)+"ms] CPU-bound process ID "+str(self.pid)+" entered ready queue (requires "+str(self.completion)+" CPU time")
			else:
				s += ("[time "+str(time)+"ms] Interactive process ID "+str(self.pid)+" entered ready queue (requires "+str(self.completion)+" CPU time")
			if flag != 1:
				s += (")")
			else:
				s += ("; priority "+str(self.priority)+")")
		elif case == 3:
			if self.burstsRemaining >= 0:
				s += ("[time "+str(time)+"ms] CPU-bound process ID "+str(self.pid)+" CPU burst done (turnaround time "+str(self.turnaround)+"; total wait time "+str(self.wait)+")")
			else:
				s += ("[time "+str(time)+"ms] Interactive process ID "+str(self.pid)+" CPU burst done (turnaround time "+str(self.turnaround)+"; total wait time "+str(self.wait)+")")
		elif case == 4:
			s += ("[time "+str(time)+"ms] CPU-bound process ID "+str(self.pid)+" terminated (avg turnaround time "+str(self.averageTurn())+"; avg total wait time "+str(self.averageWait())+")")
		elif case == 5:
			if self.burstsRemaining >= 0:
				s = "[time "+str(time)+"ms] Increased priority of CPU-bound process ID "+str(self.pid)+" to "+str(self.priority)+" due to aging"
			else:
				s = "[time "+str(time)+"ms] Increased priority of Interactive process ID "+str(self.pid)+" to "+str(self.priority)+" due to aging"
		else:
			print("Error with output() function, invalid case")
			assert(1==0)
		print(s)

	def isCPUBound(self):
		""" Returns True if self is a CPU bound process
		"""
		if self.burstsRemaining < 0:
			return False
		else:
			return True

def printContextSwitch( p1, p2, TIME ):
	print("[time %dms] Context switch (swapping out process ID %d for process ID %d)" % (TIME,p1.pid,p2.pid))

#####################################################################################

class PriorityQueue(object):
  """ Wrapper Class for PriorityQueue using heapq
		  Combined priority queue and set data structure. Acts like
		  a priority queue, except that its items are guaranteed to
		  be unique.

		  Important: the items of this data structure must be both
		  comparable and hashable (i.e. must implement __cmp__ and
		  __hash__). This is true of Python's built-in objects, but
		  you should implement those methods if you want to use
		  the data structure for custom objects.
  """
  def __init__(self, items=[]):
    """ Create a new PriorityQueue.

        items:
            An initial item list - it can be unsorted and 
            non-unique. The data structure will be created in
            O(N).
    """
    self.heap = items
    heapq.heapify(self.heap)

  def __iter__(self):
  	""" Allows us to itterate through the Queue in a for loop
  	"""
  	return self.heap.__iter__()

  def __len__(self):
  	""" Allows us to find the size of our queue
  	"""
  	return len(self.heap)  	

  def __getitem__(self,index):
  	"""Allows indexing
  	"""
  	return self.heap[index]

  		
  def pop(self):
    """ Remove and return the smallest item from the queue
    """
    if len(self.heap) != 0:
	  	return heapq.heappop(self.heap)

  def add(self, item):
    """ Add *item* to the queue. 
    """
    heapq.heappush(self.heap, item)

  def empty(self):
  	""" Returns whether or not a Queue is empty
  	"""
  	if len(self.heap) == 0:
  		return True
  	else:
  		return False

  def completed(self):
  	""" Will return true if there are no CPU bound processes in queue
  	"""
  	if self.empty():
  		return True
  	for p in self.heap:
  		if p.isCPUBound():
  			return False
  	return True

  def largest(self):
  	""" Returns the largest process in the queue
  			Used when checking for preemption
  	"""
  	largest = heapq.nlargest(1,self.heap)
  	assert(len(largest) == 1)
  	return largest[0]

  def contextSwitch(self):
  	temp = []
  	for p in range(0,len(self.heap)):
  		temp.append(heapq.heappop(self.heap))
  	temp.sort()
  	old = temp.pop()
  	for p in temp:
  		heapq.heappush(self.heap,p)
  	return old

  def resort(self):
  	""" Removes and readds all items on the queue
  	"""
  	temp = []
  	for p in range(0,len(self.heap)):
  		temp.append(heapq.heappop(self.heap))
  	for p in temp:
  		heapq.heappush(self.heap,p)

#####################################################################################

def analysis(completedProcess,time):
	""" Analyzes the performance of the algorithm given the completion time and the list of processes
	"""
	turnarounds = [] #List of all Turnaround Times
	waits = []	#List of all Wait Times
	CPUtimes = [] #List of total CPU Times (1 per process)
	for p in completedProcess:
		for t in p.totalTurns:
			turnarounds.append(t)
		for t in p.totalWaits:
			waits.append(t)
		CPUtimes.append(p.totalCPU())
	mint = min(turnarounds)
	maxt = max(turnarounds)
	avgt = sum(turnarounds)/len(turnarounds)
	minw = min(waits)
	maxw = max(waits)
	avgw = sum(waits)/len(waits)
	print("Turnaround time: min %d ms; avg %d ms; max %d ms" % (mint,avgt,maxt))
	print("Total wait time: min %d ms; avg %d ms; max %d ms" % (minw,avgw,maxw))
	temp = float(sum(CPUtimes))/float(sum(CPUtimes)+sum(waits))*100
	print("Average CPU utilization: %.2f%%" %  temp) 
	for p in completedProcess:
		temp = float(p.totalCPU())/float(p.totalCPU()+sum(p.totalWaits))*100
		print("Process ID %d: %.2f%%" % (p.pid,temp))

#####################################################################################

def randomProcessList(n):
	""" Will create a list of n process
			2/10 processes will be cpu bound (randomly)
			will retry if at least1 process is not CPU bound
	"""
	processes = []
	for i in range(0,n):
		if(random.randint(0,10) < 2):
			processes.append(process(i,random.randint(0,5),8))
		else:
			processes.append(process(i,random.randint(0,5),-1))
	flag = False
	for p in processes:
		p.assignCompletion()
		if p.isCPUBound():
			flag = True
	if flag:
		return processes
	else:
		return randomProcessList(n)

#####################################################################################

def SJFN(processes, m ):
	"""	Shortest Job First without Preemption. 
			Ready Queue is sorted by burst time of all ready processes.
			Takes in a list of processes and m CPUs
	"""
	for p in processes:
		p.priority = 0
	TIME = 0
	completedProcess = []
	# Create 3 queues
	inCPU = PriorityQueue([])
	ready = PriorityQueue(processes)
	blocked = PriorityQueue([])
	# Adjust the contents of the Ready Queue
	for p in ready:
		p.timeSlice = p.completion
		p.output(1,0,TIME)
	# Populate our inCPU queue
	for i in range(0,m):
		if not ready.empty:
			inCPU.add(ready.pop())
	# Loop until all CPU Bound processes are completed
	while(not(ready.completed() and inCPU.completed() and blocked.completed())):
		# Check if blocked processes are ready
		if not blocked.empty():
			if blocked[0].block <= 0:
				# Pop it from blocked, assign a completion time and burst time, send it to ready queue
				p = blocked.pop()
				p.block = 0
				p.assignCompletion()
				p.timeSlice = p.completion
				p.output(1,0,TIME)
				ready.add(p)
			#INSERT PREEMPTOIN HERE LATER
		# Check if CPU processes are completed
		if not inCPU.empty():
			while inCPU[0].timeSlice == 0:
				# Pop it, check its type/whether it needs I/O
				p = inCPU.pop()
				p.totalTurns.append(p.turnaround)
				p.totalWaits.append(p.wait)
				p.burstsRemaining -= 1
				if p.burstsRemaining == 0:
					# Register the processes completion
					p.output(4,0,TIME)
					completedProcess.append(p)
				else:					
					# Assign it an I/O time, clear other attr, and send it to blocked
					p.output(3,0,TIME)
					p.turnaround = 0
					p.wait = 0
					p.assignBlock()					
					blocked.add(p)
				if len(inCPU) == 0:
					break
		# Add processes to the CPU from Ready if there is room
		while len(inCPU) < m:
			if not ready.empty():
				inCPU.add(ready.pop())
			else:
				break
		# Increment All processes
		for p in inCPU:
			p.completion-=1
			p.timeSlice-=1
			p.turnaround+=1
			assert(p.block==0)
		for p in ready:
			p.turnaround+=1
			p.wait+=1
			assert(p.block==0)
		for p in blocked:
			p.block-=1
			assert(p.completion == 0)
			assert(p.turnaround == 0)
			assert(p.wait == 0)
			assert(p.timeSlice == 0)
		TIME += 1
	for i in range(0,len(blocked)):
		completedProcess.append(blocked.pop())
	for i in range(0,len(ready)):
		completedProcess.append(ready.pop())
	for i in range(0,len(inCPU)):
		completedProcess.append(inCPU.pop())
	analysis(completedProcess,TIME)

#####################################################################################

def SJFP(processes,m):
	""" Shortest Job First with Preemption
			Ready Queue is sorted by process completion time
			If a job enters the ready queue and is smaller the remaining time
				on the current job there is a context switch
	"""
	for p in processes:
		p.priority = 0
	TIME = 0
	CT = 2
	completedProcess = []
	# Create 3 queues
	inCPU = PriorityQueue([])
	ready = PriorityQueue(processes)
	blocked = PriorityQueue([])
	# Adjust the contents of the Ready Queue
	for p in ready:
		p.timeSlice = p.completion
		p.output(1,0,TIME)
	# Populate our inCPU queue
	for i in range(0,m):
		if not ready.empty:
			inCPU.add(ready.pop())
	# Loop until all CPU Bound processes are completed
	while(not(ready.completed() and inCPU.completed() and blocked.completed())):
		# Check if blocked processes are ready
		if not blocked.empty():
			if blocked[0].block <= 0:
				# Pop it from blocked, assign a completion time and burst time, send it to ready queue
				p = blocked.pop()
				p.block = 0
				if p.completion == 0:
					p.assignCompletion()
					p.timeSlice = p.completion
				p.output(1,0,TIME)
				if len(inCPU) < m:
					inCPU.add(p)
				elif p.timeSlice >= inCPU.largest().timeSlice:
					ready.add(p)
				else:
					old = inCPU.contextSwitch()
					p.timeSlice+=CT
					p.completion+=CT
					old.block=CT
					printContextSwitch(old,p,TIME)
					inCPU.add(p)
					blocked.add(old)				
		# Check if CPU processes are completed
		if not inCPU.empty():
			while inCPU[0].timeSlice == 0:
				# Pop it, check its type/whether it needs I/O
				p = inCPU.pop()
				p.totalTurns.append(p.turnaround)
				p.totalWaits.append(p.wait)
				p.burstsRemaining -= 1
				if p.burstsRemaining == 0:
					# Register the processes completion
					p.output(4,0,TIME)
					completedProcess.append(p)
				else:					
					# Assign it an I/O time, clear other attr, and send it to blocked
					p.output(3,0,TIME)
					p.turnaround = 0
					p.wait = 0
					p.assignBlock()					
					blocked.add(p)
				if len(inCPU) == 0:
					break
		# Add processes to the CPU from Ready if there is room
		while len(inCPU) < m:
			if not ready.empty():
				inCPU.add(ready.pop())
			else:
				break
		# Increment All processes
		for p in inCPU:
			p.completion-=1
			p.timeSlice-=1
			p.turnaround+=1
			assert(p.block==0)
		for p in ready:
			p.turnaround+=1
			p.wait+=1
			assert(p.block==0)
		for p in blocked:
			p.block-=1
		TIME += 1
	for i in range(0,len(blocked)):
		completedProcess.append(blocked.pop())
	for i in range(0,len(ready)):
		completedProcess.append(ready.pop())
	for i in range(0,len(inCPU)):
		completedProcess.append(inCPU.pop())
	analysis(completedProcess,TIME)

#####################################################################################

def RR(processes,m):
	""" Round Robin priority algorithm
			All ready processes are given a time slice (default 100ms) to be in the CPU
			After that time slice, Preemption occurs
			There is no context switch for a smaller process entering the ready queue
	"""
	# Tracker allows us to rotate through the queue overiding the the priority on completion time
	tracker=0
	for p in processes:
		p.priority = 0
	TIME = 0
	CT = 2
	TS = timeLimit
	completedProcess = []
	# Create 3 queues
	inCPU = PriorityQueue([])
	ready = PriorityQueue(processes)
	blocked = PriorityQueue([])
	# Adjust the contents of the Ready Queue
	for p in ready:
		p.timeSlice = min(p.completion,TS)
		p.output(1,0,TIME)
	# Populate our inCPU queue
	for i in range(0,m):
		if not ready.empty:
			inCPU.add(ready.pop())
	# Loop until all CPU Bound processes are completed
	while(not(ready.completed() and inCPU.completed() and blocked.completed())):
		# Check if blocked processes are ready
		if not blocked.empty():
			if blocked[0].block <= 0:
				# Pop it from blocked, assign a completion time and burst time, send it to ready queue
				p = blocked.pop()
				p.block = 0
				if p.completion == 0:
					p.assignCompletion()
				p.timeSlice = min(p.completion,TS)
				p.output(1,0,TIME)
				ready.add(p)
		# Check if CPU processes are completed
		if not inCPU.empty():
			while inCPU[0].timeSlice == 0:
				# Pop it, check its type/whether it needs I/O
				p = inCPU.pop()
				if p.completion == 0:
					p.totalTurns.append(p.turnaround)
					p.totalWaits.append(p.wait)
					p.burstsRemaining -= 1
					if p.burstsRemaining == 0:
						# Register the processes completion
						p.output(4,0,TIME)
						completedProcess.append(p)
					else:					
						# Assign it an I/O time, clear other attr, and send it to blocked
						p.output(3,0,TIME)
						p.turnaround = 0
						p.wait = 0
						p.assignBlock()					
						blocked.add(p)
				else:
					# Context Switch
					tracker+=1
					p.priority=tracker
					p.block = CT
					blocked.add(p)
					if not ready.empty():
						q = ready.pop()
						q.timeSlice = min(q.completion,TS)
						q.completion+=CT
						q.timeSlice+=CT
						inCPU.add(q)
						printContextSwitch(p,q,TIME)
					else:
						printContextSwitch(p,p,TIME)
				if len(inCPU) == 0:
						break
		# Add processes to the CPU from Ready if there is room
		while len(inCPU) < m:
			if not ready.empty():
				inCPU.add(ready.pop())
			else:
				break
		# Increment All processes
		for p in inCPU:
			p.completion-=1
			p.timeSlice-=1
			p.turnaround+=1
			assert(p.block==0)
		for p in ready:
			p.turnaround+=1
			p.wait+=1
			assert(p.block==0)
		for p in blocked:
			p.block-=1
		TIME += 1
	for i in range(0,len(blocked)):
		completedProcess.append(blocked.pop())
	for i in range(0,len(ready)):
		completedProcess.append(ready.pop())
	for i in range(0,len(inCPU)):
		completedProcess.append(inCPU.pop())
	analysis(completedProcess,TIME)

#####################################################################################

def PP(processes,m):
	""" Preemptive Priority algorithm
			All processes are assigned a priority level at random. Processes run until
			they are completed and the queue is sorted by priority level. A process that has
			been waiting for more than 1200ms, its priority increases
	"""
	TIME = 0
	CT = 2
	completedProcess = []
	# Create 3 queue
	inCPU = PriorityQueue([])
	ready = PriorityQueue(processes)
	blocked = PriorityQueue([])
	# Adjust the contents of the Ready Queue
	for p in ready:
		p.timeSlice = p.completion
		p.output(1,1,TIME)
	# Populate our inCPU queue
	for i in range(0,m):
		if not ready.empty:
			inCPU.add(ready.pop())
	# Loop until all CPU Bound processes are completed
	while(not(ready.completed() and inCPU.completed() and blocked.completed())):
		# Check if blocked processes are ready
		if not blocked.empty():
			if blocked[0].block <= 0:
				# Pop it from blocked, assign a completion time and burst time, send it to ready queue
				p = blocked.pop()
				p.block = 0
				if p.completion == 0:
					p.assignCompletion()
					p.timeSlice = p.completion
				p.priority = p.initpri
				p.output(1,1,TIME)
				if len(inCPU) < m:
					inCPU.add(p)
				else:
					ready.add(p)		
		# Check if CPU processes are completed
		if not inCPU.empty():
			while inCPU[0].timeSlice == 0:
				# Pop it, check its type/whether it needs I/O
				p = inCPU.pop()
				p.totalTurns.append(p.turnaround)
				p.totalWaits.append(p.wait)
				p.burstsRemaining -= 1
				if p.burstsRemaining == 0:
					# Register the processes completion
					p.output(4,1,TIME)
					completedProcess.append(p)
				else:					
					# Assign it an I/O time, clear other attr, and send it to blocked
					p.output(3,1,TIME)
					p.turnaround = 0
					p.wait = 0
					p.assignBlock()					
					blocked.add(p)
				if len(inCPU) == 0:
					break
		# Add processes to the CPU from Ready if there is room
		while len(inCPU) < m:
			if not ready.empty():
				inCPU.add(ready.pop())
			else:
				break
		# Check for aging
		if not ready.empty():
			for p in ready:
				if (p.wait != 0) and (p.wait%1200 == 0) and (p.priority != 0):
					p.priority -= 1
					p.output(5,1,TIME)
			ready.resort() 
		# Check for context switches
		if not (ready.empty() or inCPU.empty()):
			while ready[0].priority < inCPU.largest().priority:
				p = ready.pop()
				old = inCPU.contextSwitch()
				p.timeSlice+=CT
				p.completion+=CT
				old.block=CT
				printContextSwitch(old,p,TIME)
				inCPU.add(p)
				blocked.add(old)
				if ready.empty():
					break
		# Increment All processes
		for p in inCPU:
			p.completion-=1
			p.timeSlice-=1
			p.turnaround+=1
			assert(p.block==0)
		for p in ready:
			p.turnaround+=1
			p.wait+=1
			assert(p.block==0)
		for p in blocked:
			p.block-=1
		TIME += 1
	for i in range(0,len(blocked)):
		completedProcess.append(blocked.pop())
	for i in range(0,len(ready)):
		completedProcess.append(ready.pop())
	for i in range(0,len(inCPU)):
		completedProcess.append(inCPU.pop())
	analysis(completedProcess,TIME)

#####################################################################################

def main(m,n):
	""" Main Function where test functions will be called
	"""
	processes = randomProcessList(n)
	SJFN(copy.deepcopy(processes),m)
	SJFP(copy.deepcopy(processes),m)
	RR(copy.deepcopy(processes),m)
	PP(copy.deepcopy(processes),m)

#####################################################################################

if __name__ == '__main__': 
	""" First arguement is number of cores, m
			Second is number of processes ran, n
			Third is time limit, timeLimit
	"""
	skip = 1;
	m = 1 						#Number of Cores used
	n = 12						#Number of Processes ran
	timeLimit = 100		#Time limit given for Algoritms like Round Robin
	for arguement in sys.argv:
		if skip == 1:
			skip = 0
		elif arguement[0] == 'm' and len(arguement)>2:
			m = int(arguement[2:len(arguement)])
		elif arguement[0] == 'n' and len(arguement)>2:
			n = int(arguement[2:len(arguement)])
		elif arguement[0:4] == "time" and len(arguement)>5:
			timeLimit = int(arguement[5:len(arguement)])
		pass

	main(m,n)