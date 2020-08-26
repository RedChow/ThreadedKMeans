<h1>Threaded KMeans - Jython</h1>
[Jython](https://www.jython.org) is the Java implementation of Python. One advantage of Jython over CPython is
the lack of the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (GIL) and thus can fully
exploit multiprocessor systems. Threading in Jython is super easy, just follow the steps:
<ol>
	<li>Import the Thread module from threading</li>
	<li>sub-class Thread</li>
	<li>Override the run function from Thread</li>
	<li>Create an instance of the class</li>
	<li>Call start()</li>
</ol>
Congratuations, you are now multithreading in Jython!
