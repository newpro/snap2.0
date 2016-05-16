[&#xf0eb;] **Design Control Documentation**
-------------
&#xf040; By Aaron Li, May 10, 2016. 

### [&#xf192;] **Targets and Requirements**
Design Control is the **interface** that responsible for **set up the knowledge base**. Targeted for two kinds of users:  medical personnel and administration engineers. 

* Medical Personnel
	* People presume to have no knowledge of the system, or knowledge of components of the system. Which the system should fit for the following principles:
		* No knowledge: no knowledge of the system is required.
		* Easy Adapted: first time user should be able to use right away without instructions.
		* Time Constricted: should be able to set up with the shortest time possible. 
* Administration Experts
	* People presume to have partial knowledge of the system, have at least one of the followings:
		* Industry knowledge: necessary knowledge of the sensor communication protocol, error rates. 
		* Field experience: knowledge of how to set up a working module with correct trigger, environment, target, reward, and probability.
		* Medical knowledge: knowledge of patience behaviour.

### [&#xf0c0;] **Roles**

Rules are the safe guards against modify the model without the knowledge of the part, as well as separation of the responsibilities.

### Administration Class
Administration class users are responsible to make sure the system and the model running correctly. Each roles have the following properties:

* Required knowledge: knowledge required for the person to take the role. 
* Responsibilities: the responsibilities of the role.
* Access rights: which portion of the system can the role modify.

#### Super User
Super user is the core admin of the system. This role should lead by developers with high knowledge of the system. This roles are limited to have a maximum of three instances.

* Required knowledge:
	* computer science
	* working knowledge of the system
* Responsibilities: 
	* system health monitoring
	* debugging and damage control
* Access rights: all rights granted

#### HR Specialist
HR specialist is a role that allow to add user into the system.

 * Required knowledge: 
	 * HR
	 * Structure of this role system
 * Responsibilities:
	 * appointing roles
 * Access rights
	 * appoint any roles except super user
 
#### Hardware Engineer

* Required knowledge: 
	* sensors communication protocols
	* 