## Care Giver User Interface Description ##
####Overview ####
The "care giver user interface" module is an interactive interface for care givers to set up the domain knowledge for the intelligent assistance agent. The basic operations on this interface is:

 - **Create** new goals;
 - **Modify** on existing tasks;
 - **Specify** sensor for furniture;

####UI Explanation####
Based on needs, the caregiver plan to add the task network of a new goal to the system. This expand the recognition capacity of the intelligent system. The domain knowledge should be stored  
He/she should go through the following steps. 

 - Click on "add new goal"
 - Input goal name
 - Configure the **task network** of the goal according to user interface prompt
	 - Step 1: For each task int the network, ask the user "Does this task can to decomposed into sub-tasks?
	 - Step 2: If yes, ask the user to input all the sub-tasks and specify the **order relations** (for details please refer to "order relations of sub-tasks" section) of the sub-tasks. 
	 - Repeat Step 1 and Step 2 until the user specified the complete task network for the goal. 
	 - Attention that **if a sub-tasks or step already exist in the domain knowledge**, the system should be able to suggest the existing one , and ask the user's confirmation. This step is designed to keep the clean of domain knowledge. 
 - Configure a **primitive step**. When the user says the current node cannot be decomposed into sub-tasks, then this node is a leaf node, it stands for a primitive step in real world, and will change the states of some real objects. 
	 - Step 1: Prompt user with "Please drag the related objects of this step to the operating window"
	 - Step 2: For each objects in the window:
		 - Identify the category of the object based on the **furniture** table in the database
		 - Identify associated sensors for the object by searching on the  **sensor** table in the database
		 - Ask the user to specify the **step name**  by looking into the popped steps selection lists associated with this sensor, and select one of the **step name**. When a step name is select, its preconditions and effects are also specified by searching on the **step_precondition_effects** table. 
		 - If the user already has the sensor, ask the user register the sensor on the system (this information will be stored into the **sensor-furniture** table in database) and attach the sensor to the above-mentioned object. 
		 - If the user do not have the sensor yet, suggest the online purchase choices for the user. If the user confirm, the order will be made automatically by the system. At the same time, in **sensor-furniture** table, this furniture is recorded as "no attached sensor". 

####Order relations of sub-tasks####
An hierarchical task network indicates how a composite task can be decomposed into simpler
subtasks. The sub-tasks of a composite task can have the following relations.

 - Alternative sub-tasks: the composite tasks have multiple ways to decompose, which way to choose depends on the current environment states.
 - **Ordered sub-tasks**: the sub-tasks must be implemented in order.
 - **Un-ordered sub-tasks**: the implementation order of sub-tasks does not matter.
 - **Partially ordered subtasks**: some of the subtasks must be implemented in order, when to
implement the other sub-tasks does not matter.	
	 
####Domain Knowledge Processing####
The newly added goal and its corresponding task network should be firstly processed and then added into the **knowledge base**. The domain knowledge should be stored into the knowledge base in the format of Hierarchical Task Network (HTN). The main purpose of domain knowledge processing is to automatically generate preconditions for higher level tasks by reasoning on preconditions of primitive steps. Details about this abstracting process is illustrate in Latex file.

####Domain Knowledge Storing

...to be defined;

####Database associated issues
#####Required data from the Expert Interface module
 - Furniture category-Furniture
 - Furniture category-Sensor
 - Sensor-Step
 - Step-Precondition/Effects

#####Required data from Home Environment
 - object in the environment. The images(or tags) in the interface should be associated to an real object in the environment. 

#####Generated data 
 - sensor-furniture object (This table will be used to tracking the system states)
 - knowledge base
 
