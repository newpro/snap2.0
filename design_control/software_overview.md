[&#xf085;] **Software Overview - DESIGN CONTROL**
-------------

&#xf040; By Aaron Li, June 2, 2016. 

### [&#xf1cb;] **Software Framework Overview**

In general, the software framework should be able to allow for one expert to do the following tasks, along with non-functional requirements:

* Role Based Management
	* Role registration system ([audit & control](#audit-and-control), [Certification](#certification))
	* Login ([Privacy](#privacy) & [Security](#security))
* Information Management
	* Input information
		* Enforced standards ([Compliance](#compliance))
		* Information close to real world environment ([Configuration management](#configuration-management))
		* Useful Formatted Data ([Dependency](#dependency-on-other-parties), Effectiveness)
	* Automatic Validation ([Testability](#testability))
		* Check for error when input, reject input if error
		* Check error in runtime ( [Fault tolerance, Robustness, Resilience](#fault-tolerance-robustness-resilience))
	* Version Control
		* Control several versions of the same system ([Extensibility](#maintainability-modifiability-extensibility))
			* Tracking the versions
			* Testing a versions
			* Comment on one version ([Reporting](#reporting))
			* Commit a version to master
	* Data Peeking
		* Access necessary data to build relative part
* Testing ([Maintainability & Modifiability](#maintainability-modifiability-extensibility))
	* System will automatically run in simulate environment to see if the parameters can fit in
		* Human control panel for when to run checking
	* Human can test the system ([Failure management](#failure-management))
		* Testing engineer can test parameters
	* Safety inspector can check the security of the system ([Safety](#safety))
		* Shut down one execution plan in an emergency unsafety situations
		* Able to file report to ask for other experts to correct security issues

### [&#xf0e4;] **Non-functional requirements Listing**

#### Audit and control

Every new member should pass audit by a human member in the system in order to be added in.

#### Availability

This subsystem should be able to be online most of times, and still be available under the following extreme situations:

* Large traffic load
* Large calculation load
* Without maintenance for long time
* Bad hardware conditions
* Different part of SNAP system breakdown

#### Backup

DB should be automatic backup in a short time period.

#### Capacity

Fitful for a large data storage.

#### Certification

All members that is in the system / will be added in the system should pass certification check.

#### Compliance

All data stored inside DB have to comply with international standards, if there is one. 

#### Configuration management

The parameters provided by experts should be as close as real world configuration as possible.

#### Dependency on other parties

Other system should be able to use data in DB directly, and at the same time this part should not have any dependency.

#### Documentation

All parts of the system that involve with human interaction should be clearly documented.

#### Efficiency

Server should be able to handle large load without crash.

#### Failure management

If any information that did not set up initially, no matter it is caused by failure in initial consideration, or human operator error, can be corrected easily. This require **decoupling with other DB table, and other part of system, and platform integrated for human to check failures.**.

#### Fault tolerance (Robustness, Resilience)

Experts should not allow to input false information, or incorrect format information in the first place. But if somehow they did, the system should **be able to recognize it**, as much as possible, and either **issue warning and ignore the information**, or **find the closest match**, if it has confidence that it is a correct match.

The definition of the false information are including the following:

* incorrect information
* incorrect formatted information
	* incorrect number format
	* incorrect unit

#### Interoperability

Any experts without computer science knowledge can operate through UI without much confusion.

#### Network topology

The data should input and output correctly, no matter what the low level system it relays on. 

#### Operability

The system should be operated by people with no knowledge of the system, or computer science.

#### Maintainability (Modifiability, Extensibility)

Use version control system to track all versions, so it is easy to track, change, test, and remove information.

#### Platform compatibility

The web framework should support and behave universally across all platforms, include:
 
* UI universal
* Functional universal

#### Privacy

The information in database should not access by unauthorized personnel, include read and write access.

#### Reporting

Under the situation of failures get detected, the system should be able to send reports to relative personnel(s).

#### Safety

The Safety inspection should enforce security. See Safety Inspector. 

#### Scalability

Scalability is a future consideration. The system should be able to hold under traffic stress.

#### Security

Security is a future consideration. The system should be able to defence security attacks.

#### Stability

The overall structure and design of the system should not require a lot of changes in future releases.

#### Testability

Any variations of the data in database should attach at least one method for testing.