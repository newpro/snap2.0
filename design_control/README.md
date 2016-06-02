[&#xf0eb;] **Design Control Documentation**
-------------

&#xf040; By Aaron Li, May 16, 2016. 

### [&#xf192;] **Targets and Requirements**

Design Control is the **interface** that responsible for **set up the knowledge base**. Targeted for two kinds of users:  medical personnel and administration engineers. 

* Care Givers
	* Care givers are personnel who works in a hospital, private home, or other settings that are responsible for helping patiences in everyday life.
	* Care givers are presumed to have no knowledge of the system, or components of the system. Which requires the system to fits the following requirements as much as possible:
		* No knowledge: no knowledge of the system is required.
		* Easily Adapted: first time user should be able to use right away without instructions.
		* Time Constricted: should be able to set up with the shortest time possible. 
* Administration Experts
	* People presume to have partial knowledge of the system, have at least one of the followings:
		* Industry knowledge: necessary knowledge of the sensor communication protocol, error rates. 
		* Field experience: knowledge of how to set up a working module with correct trigger, environment, target, reward, and probability.
		* Medical knowledge: knowledge of patience behaviour.

### [&#xf11e;] **User Workflow**

For each role in the system, the users should be able to login as the role, and modify knowledge base limited only to the portions that they have access to. 

> **Access Decision** [&#xf084;]:
> 
> Security and correctness of the system relies on the knowledge base, which is built by content providers, in this case the care givers and Administration experts. The system should be able to give enough freedom for each parties to set up knowledge base, and not a little bit more, for the following reasons:
> * **Separate of Logic**:  each role can only access the part that they should access, in order to provide correct information to the knowledge base.
> * **Minimal Access**: each role accesses the information as little as possible, gives protection on information correctness and integrity.
> * **Bugs Tracking**: each role have their own responsibility in the system, this makes bug correction faster and easily. Increase reliability of the system as a whole.
> * **Collaboration Conflicts**: collaboration is critical in order to build the knowledge base. Each rule should only be able to modify the parts they should modify, in order to have no conflicts during collaboration.

The workflow of one user can be expressed by the diagram: 
<p align="center">
  <img src="../diagrams/interface_workflow.png" width="550"/>
</p>

### [&#xf1c0;] **Database Outline**

In order to support the knowledge base, the database have to support tracking and reasoning module, we have to first understand the relationship between human, sensors, and environment objects. 

#### A High Level View

In a high level view, human act on environment objects, trigger change of status in sensors. Which can be indicate as following: 

<p align="center">
  <img src="../diagrams/interface_db_highlevel.png" width="550"/>
</p>

But unfortunately, this is not merely enough to represent by db, there are several questions remain: 

* What category of sensor and environment objects can work together?
* What status can one particular sensor have?
* What kind of action can a human perform?
* What kind of action can trigger one kind of sensor stage change?

In order to answer those questions, we have to investigate further to build relationship. 

#### Environment Objects & Sensors

Sensors attached to environment objects, a change in environment objects reflect in change of sensors. Only one set of sensors can attach to one kind of environment objects, so we group both sensors and environment objects into groups.

![db_es](../diagrams/interface_db_es.png)

#### Human & Environment Objects

Human interact with environment objects. Only one set of environment object is allow to interact by human, and the actions are limited. Human object is divided into categories as well to represent different level of patience, to divide the ability of patience.

![db_ho](../diagrams/interface_db_ho.png)

#### Human , Sensors and Environment Objects

![db_overall](../diagrams/interface_db_overall.png)

### [&#xf0c0;] **Roles**

Rules are the safe guards against modify the model without the knowledge of the part, as well as separation of the responsibilities. <br>
The roles including the following:

* Super User
* HR Specialist
* Testing Engineer
* Safety Inspector
* Hardware Engineer
* Interior Designer
* Medical Care Experts

See the details [here](./roles.md).

### Software Framework

In general, the software framework should be able to allow for one expert to do the following tasks, along with non-functional requirements:

* Role Based Management
	* Role registration system (audit & control, Certification)
	* Login (Privacy & Security)
* Input Information
	* Enforced standards (Compliance)
	* Information close to real world environment (Configuration management)
	* Useful Formatted Data (Dependency, Effectiveness)
* Automatic Validation (Testability)
	* Check for error when input, reject input if error
	* Check error in runtime ( Fault tolerance, Robustness, Resilience)
* Version Control
	* Control several versions of the same system (Extensibility)
		* Tracking the versions
		* Testing a versions
		* Comment on one version (Reporting)
		* Commit a version to master
* Data Peeking
	* Access necessary data to build relative part
* Testing (Maintainability & Modifiability)
	* System will automatically run in simulate environment to see if the parameters can fit in
		* Human control panel for when to run checking
	* Human can test the system (Failure management)
		* Testing engineer can test parameters
	* Safety inspector can check the security of the system (Safety)
		* Shut down one execution plan in an emergency unsafety situations
		* Able to file report to ask for other experts to correct security issues

All non-functional requirements overview (Emphasis indicates already included in requirements):

##### *Audit and control*

Every new member should pass audit by a human member in the system in order to be added in.

##### Availability

This subsystem should be able to be online most of times, and still be available under the following extreme situations:

* Large traffic load
* Large calculation load
* Without maintenance for long time
* Bad hardware conditions
* Different part of SNAP system breakdown

##### Backup

DB should be automatic backup in a short time period.

##### Capacity

Fitful for a large data storage.

##### *Certification*

All members that is in the system / will be added in the system should pass certification check.

##### *Compliance*

All data stored inside DB have to comply with international standards, if there is one. 

##### *Configuration management*

The parameters provided by experts should be as close as real world configuration as possible.

##### Dependency on other parties

Other system should be able to use data in DB directly, and at the same time this part should not have any dependency.

##### Documentation

All parts of the system that involve with human interaction should be clearly documented.

##### *Efficiency*

Server should be able to handle large load without crash.

##### *Failure management*

If any information that did not set up initially, no matter it is caused by failure in initial consideration, or human operator error, can be corrected easily. This require **decoupling with other DB table, and other part of system, and platform integrated for human to check failures.**.

##### *Fault tolerance (Robustness, Resilience)*

Experts should not allow to input false information, or incorrect format information in the first place. But if somehow they did, the system should **be able to recognize it**, as much as possible, and either **issue warning and ignore the information**, or **find the closest match**, if it has confidence that it is a correct match.

The definition of the false information are including the following:

* incorrect information
* incorrect formatted information
	* incorrect number format
	* incorrect unit

##### Interoperability

Any experts without computer science knowledge can operate through UI without much confusion.

##### Network topology

The data should input and output correctly, no matter what the low level system it relays on. 

##### Operability

The system should be operated by people with no knowledge of the system, or computer science.

##### *Maintainability (Modifiability, Extensibility)*

Use version control system to track all versions, so it is easy to track, change, test, and remove information.

##### Platform compatibility

The web framework should support and behave universally across all platforms, include:
 
* UI universal
* Functional universal

##### *Privacy*

The information in database should not access by unauthorized personnel, include read and write access.

##### *Reporting*

Under the situation of failures get detected, the system should be able to send reports to relative personnel(s).

##### *Safety*

The Safety inspection should enforce security. See Safety Inspector. 

##### Scalability

Scalability is a future consideration. The system should be able to hold under traffic stress.

##### *Security*

Security is a future consideration. The system should be able to defence security attacks.

##### Stability

The overall structure and design of the system should not require a lot of changes in future releases.

##### *Testability*

Any variations of the data in database should attach at least one method for testing.
