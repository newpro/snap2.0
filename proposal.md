
[&#xf15c;] **SNAP 2.0 Project Proposal**
-------------
&#xf040; Aaron Li, April 28, 2016.

###[&#xf192;] **Targets**
New SNAP interface is expect to have  unified interface links to physical sensors. Allow the users to do the followings:

* visualize and change the status, probability, and transations by graphs
	* status by uml boxes
	* probability by labels
	* transactions by arrows
* trigger devices in testing environment
	* trigger individual devices to follow a command for device testing
	* trigger group of devices to follow a sets of commands for testing:
		* feed forward testing: device response
		* feed backward testing: SNAP
		* processing logic: a set of commands to test one logic set

###  [&#xf19c;] **Standards and Grounds** 

* Graph Interface
	* The graph is represented in UML, expected to follow [UML Standards 2.5](http://www.omg.org/spec/UML/2.5/)
		>  Design decision: why UML  [&#xf059;]
		>  UML allows ppl to communicate better, giving the following advantages in this project:
		> * Language and API independent: allow UI too isolated with backend logic modules
		> * Universal and easy: UML is easy to understand by both developer and none developer, fit for both situations, good for convey unambiguous work flows
		> * Built for OO: since we are focus on mapping situations and devices to real world, a OO approach is the way to go
		> * Standardized 
		
	* 