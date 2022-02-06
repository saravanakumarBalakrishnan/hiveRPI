# HiveTestAutomation
This is a Test Automation Framework developed to test Devices using ZigbeeAPI and Web/Mobile using PlatformAPI

Dependencies:
==========================
If used with pycharm then the python version to use is 3.5 <br>
![Pycharm](Assets/PyCharm.png?raw=true "Gherkin")    

Else use python 3.5 and above


Python Library Dependencies:
==========================
•	behave <br>
•	redis<br>
•	pyserial<br>
•	tqdm<br>
•	ipdb<br>
•	appium-python-client<br>
•	requests<br>
•	selenium<br>
•	nmap<br>
•	pytesseract<br>
•	pillow  (Refer for issues : https://pillow.readthedocs.io/en/latest/installation.html)<br>
•	numpy<br>
•	speechrecognition<br>
•	pysmbus<br>
•	remi<br>


Automation Framework Architecture
==================================

Architecture of our BDD Automation framework followed 3 Tier model which is written in Python and behave. (Refer : http://pythonhosted.org/behave/)

You can see below we have BDD Tier ( step definition and feature files), Manager Tier ( consist of framework level change) and Result Tier 

![Basic Structure](Assets/architecture.png?raw=true "Structure")


As per fig 2, you can see that feature file has been designed in 1st place based which is our test case. Once the feature file is defined that its comes to step definition which is implementation of feature file in python. This test script is our actual test case being automated and depending upon the device / App will make call to server either Platform API or Zigbee API. 
If we are automating our Hive app then we will use Platform API route and make a call to device through API JSON call and this is called the Appium automation. In case of web app we performed the same activity to get the response from Server via JSON call called selenium automation through Platform API. 
As per below image, semi-automated means few of the test cases cannot be automated which we will discuss later. If we are automating our real Devices, then we will use Zigbee API route and make a call to 

![Basic Structure](Assets/FrameworkArc.png?raw=true "Structure")

Framework structure
===============================
Feature file
----------------------------
Feature file are those files which contains executable specification written in a language called Gherkin(Plan text English language) OR in other words as textual story with a name that expresses the behavior to verify. Test case is written in form on
GIVEN – Given steps are used to describe the initial context of the system---the scene of the scenario.
WHEN – When steps are used to describe an event, or an action. This can be a person interacting with the system, or it can be an event triggered by another system
THEN – Then steps are used to describe an expected outcome, or result.
Ex : 
![Gherkin](Assets/Gherkin.png?raw=true "Gherkin")

Step definition
---------------------------

A Step Definition is a small piece of code with a pattern attached to it. The pattern is used to link the step definition to all the matching Steps, and the code is what behave will execute when it sees a Gherkin Step.
In our framework, Step definition are written in python programing language and implemented based on you feature file. 

Preferred IDE
---------------------------
1. Pycharm Professional Edition:

    ![Pycharm](Assets/PyCharm.png?raw=true "Gherkin")    

    PyCharm is an Integrated Development Environment (IDE) used in computer programming, specifically for the Python language. It is developed by the Czech company JetBrains.

    Download : https://www.jetbrains.com/pycharm/download/
    
    <B>Download the Professional Edition if you have License. The licensed edition only supports Behave framework<B>
    
    After installing PyCharm
    
    1.  Open the project
    2.  Verify the python Interpreter version
    3.  Verify the BDD tool is chosen as Behave
    4.  Mark the following folders are source root<br>
            1. steps<br>
            2. Function_Libraries
            3. Locators
            4. PageObjects
            5. Thermostat_Screen_Text
            
    All Done.            

2. Eclipse
    
    ![Eclipse](Assets/eclipse.png?raw=true "Gherkin")    

    Eclipse is an integrated development environment (IDE) used in computer programming, and is the most widely used Java IDE.
    
    It contains a base workspace and an extensible plug-in system for customizing the environment. 
    
    Download : http://www.eclipse.org/downloads/
    
    After installing Eclipse
    
    1.	install the following Eclipse plugin and restart eclipse<br>
        a.	PyDev<br>
        b.	Cucumber<br>
        c.	Json editor<br>
    2.  Open eclipse and set the workspace path to the parent folder of the extracted project folder.
    3.  Click on file Menu   Import
    4.  Select “Existing Projects into workspace” under “General” Category and click on next button
    5.  Select root directory as Parent folder path
    6.  Select “Advance Auto-Config” button
    7.  Select all Python35 (or Python 36 if installed python 3.6) packages as given below and click OK button
    
    All Done.

Running Tests
-------------------------------
1. Pycharm Professional Edition:

    1. Open the required feature file (*.feature Extenstion)
    2. Right click on the scenario to execute
    3. Click on Run to execute
    
2. Eclipse:

    Eclipse does not support Behave framework. Hence there is not direct way of executing the tests from Eclipse IDE.
    
    1. Note down the scenario ID tag / suite tag for the scenario / suite to be executed
    2. Navigate to features folder in Terminal / Command Prompt
    3. Enter "behave --tags=<B><i>TAG NAME</i></B>" and press enter to exeucte the test scenario / suite

Result (Run time HTML report)
-------------------------------

This is self-explanatory, once the Test scripts is executed, system will produce a result (Pass/Fail) depending on the system. In our case we generating in form of HTML

![Result](Assets/Result.png?raw=true "Result")

Platform API Class
-------------------------------

This class require when we need to access the platform/server/zigbee to get specific data as per our need for App/Webapp/device.

Zigbee API
-------------------------------

Using Zigbee API we can get device attribute values from the device and it can be also used to set values to the attribute of the device.

API JSON call
-------------------------------

All the values displayed in the Mobile/Web app must be validated against the platform data. The platform data can be retrieved / set using the APIs. GET, PUT,POST and DELETE are the operations performed.

Telegesis Stick
-------------------------------

The Telegesis stick is the USB stick which has the Zigbee tile present inside the hub. Using the Telegesis stick all the zigbee commands performed by the hub can be simulated. By which the zigbee level testing can be performed. 

Zigbee Call
-------------------------------

All the Zigbee calls use the AT commands. Using the AT commands all the readable attribute values can be obtained and all the writable attributes can be changed.

Key components of framework
===================================

Below are the key components of framework. 


Location: of this file is workspace/HiveTestAutomation/02_Manager_Tier. <br>
Purpose: We have declared the global variable for in such a way that while running your test script which client, environment, testSuite to be picked along with other details.<br>
Key parameters: <br>
"apiValidationType": "Platform API" – which API need to be connect for out script<br>
"clientList" – This will give you info which client are available and<br>
"listOfEnvironments" – Declare different set of environments ex : isopBeta, isopInternProd, isopProd and isopStaging and based on configuration will pick the right environment and there attributes which is defined in JSON.<br>
"mainClient" – Declare the primary client and your automation script first run into it. Ex : iOS App which mean script will run in iOS<br>
"secondClient" – Declare secondary client and script will run followed by primary client.<br>
"username"- Declare username to login in client while running automation test suite.<br>
"password"- Declare username to login in client while running automation test suite.<br>



Environment.py
-------------------------------
Location: of this file is /HiveTestAutomation/01_BDD_Tier/features/environment.py<br>
Purpose: This file loads/read the globalvar.json file before execution of test script. This will read all the require properties defined in global file and allows different operation like login and logout from app function, environment setup, platform API, set/update the tag, FeatureFile name & Scenario description to the summary report.<br>
Note : Please go through all the functions defined in .py <br>