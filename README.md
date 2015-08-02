# README #

Demo.py includes a use case.  This has not been submitted to PyPi yet.


!!! requires multicore processor or multiple processors, minimum 2 !!!


### Daisy Cutter ###

The main objective of this module was to create a reusable request server framework that would take advantage of multicore-processors to reduce latency in the handling of complex server requests. The server utilizes a single entry point that defers the processing and return of the result to a spawned process running on a separate execution core. 

* Request Server that uses Spawned Processes
* Based on built-in classes
* Alpha


### How do I get set up? ###

* Requires Python 3 for best results(written with 3.4 in mind)
* Download the files
* edit the demo.py to setup a request server
   -create your request handler
   -set options


### Why this server? ###

The python GIL (global interpreter lock) is a bottleneck for both threaded and forked servers. With those type of servers even though a request is being processed on a separate thread or fork it must wait for the gil until it can be processed by the interpreter.  

It is a different story with spawned processes. A spawned process has its own interpreter (and gil) so it does not need to wait.


### How it works ###

There are a few parts each with a specific function. Each of these parts can be modified by extending the base class. In this release there are 2 variations of each part so you can modify the operation of the server to best suite your implementation.

* Distributor - the distributor listens for incomming connections and then passes that connection to an available handler vis shared memory. it comes in two flavors queued and oipped.

* Handler - reads the data from an incoming connection , performans the requested operation and then sends the result back through the connection and closes the connection. There are two different types of handlers auto scaling and pooled.


### Options ###



### contact info ###
* dawsonmv@gmail.com