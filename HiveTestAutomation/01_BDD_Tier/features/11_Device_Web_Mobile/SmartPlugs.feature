Feature: Contains all the scenario related to Smart Plugs

  @SC-SP-SH01-01 @SmartPlug
  Scenario: SC-SP-SH01-01_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_1						| 96             |
    
     @SC-SP-SH01-02 @SmartPlug
  Scenario: SC-SP-SH01-02_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_2					| 8             |
    
    
     @SC-SP-SH01-03 @SmartPlug
  Scenario: SC-SP-SH01-03_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_3					| 48             |
    
    
     @SC-SP-SH01-04 @SmartPlug
  Scenario: SC-SP-SH01-04_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_4					| 2             |
    
    
     @SC-SP-SH01-05 @SmartPlug
  Scenario: SC-SP-SH01-05_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2_1					| 4             |

    @SC-SP-SH01-06 @SmartPlug
  Scenario: SC-SP-SH01-06_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2b_1				| 4             |

       @SC-SP-SH01-07 @SmartPlug
  Scenario: SC-SP-SH01-07_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2c_1				| 4             |

       @SC-SP-SH01-08 @SmartPlug
  Scenario: SC-SP-SH01-08_Set Schedule for the Smart Plugs and continuously validate the same
    Given The Smart Plugs are paired with the Hive Hub
    When The schedule for the below smart plugs are set and continuously validated via Hub
    |SmartPlug 			| NoOfEvents |
    |SLP2d_1				| 4             |
    
      @SC-SP-SH02-02 @SmartPlug @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-SP-SH02-02_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State |
      | 06:30      | ON              |
      | 08:30      | OFF             |
      | 12:00      | OFF             |
      | 14:00      | OFF             |
      | 16:00      | ON              |
      | 21:30      | OFF             |
    Then Verify if the Schedule is set

    Examples: 
      |Device  | Day   | 
      |SLP2_1 | Today |
      

      
    @SC-SP-SH02-03 @SmartPlug @ScheduleTest @6_Event @Verify @APITest
  Scenario Outline: SC-SP-SH02-03_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
       | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      |Device  | Day   | 
      |SLP2_1 | Today |

      @SC_Pl_PT_01 @AppPlug @PlugNavigation
    Scenario Outline: SC_Pl_PT_01_Validate the title of the plug screen.
    Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
    When User is navigated to <PlugName> Screen.
    Then Validate the <PlugName> title of the Plug Screen.
    Examples:
    | PlugName | | ModelNo |
    | Plug     | | SLP2    |

    @SC_Pl_PS_02 @AppPlug @Plug_ON_OFF
      Scenario Outline: SC_Pl_PS_02_Switch On and Off the Plug.
      Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
      When User is on the <PlugName> Screen.
      When User clicks on the <PlugName> toggle button.
      Then <PlugName> should be switched on or off.
      Then Validate the <PlugName> state change in Dashboard and Device Screen.

      Examples:
      | PlugName | | ModelNo |
      | Plug     | | SLP2    |

      @SC_Pl_PM_03 @AppPlug @Plugmode
      Scenario Outline: SC_Pl_PM_03_Change Plug mode from manual to schedule and vice versa.
        Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
      When User is on the <PlugName> Screen.
      When User clicks on the <PlugName> arrow button from the bottom of plug screen.
      Then <PlugName> Mode should be changed either to Manual or Schedule.

      Examples:
      | PlugName | | ModelNo |
      | Plug     | | SLP2    |


    @SC_Pl_PN_04 @AppPlug @PlugScreen_Navigation
      Scenario Outline: SC_Pl_PN_04_Validate the navigation to control,schedule and recipes Plugs screen.
      Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
      When User is on the <PlugName> Screen.
      When User clicks on the Schedule icon in Plugs Screen.
      Then User should be navigated to the Schedule page of Plugs Screen.
      When User clicks on the Recipes icon in Plugs Screen.
      Then User should be navigated to Recipes Page of Plugs Screen.
      When User clicks on the Control icon in Plugs screen.
      Then User should be navigated to the control page of Plugs Screen.

      Examples:
      | PlugName | | ModelNo |
      | Plug     | | SLP2    |


  @SC-AP-SCHE-01 @ActivePlugScheduleChanges
  Scenario: SC-AP-SCHE-01
    Given The Hive product is paired and setup for Active Plug with API Validation
    When Mode is automatically changed to MANUAL on the Client plug
    #Then Automatically validate current mode as MANUAL


  @SC-AP-MODE-01 @ActivePlugStateAndModeChanges
  Scenario: SC-AP-MC-01_Change the mode of the plug from Manual to Schedule(with expected state) to Manual and validate the same 
    Given The Hive product is paired and setup for Active Plug with API Validation
    When Mode is automatically changed to MANUAL on the Client plug
    Then Automatically validate current mode as MANUAL
    When Mode is automatically changed to AUTO on the Client plug
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to MANUAL on the Client plug
    Then Automatically validate current mode as MANUAL

  @SC-AP-STATE-01 @ActivePlugStateAndModeChanges @AndroidRegression
  Scenario: SC-AP-SC-01
  #Change the state of the plug from OFF to ON to OFF when plug is in manual mode and validate the same 
    Given The Hive product is paired and setup for Active Plug with API Validation
    When Mode is automatically changed to MANUAL on the Client plug
    Then Automatically validate current mode as MANUAL
    When State is automatically changed to OFF on the Client plug while in Manual mode
    Then Automatically validate current state as OFF while in Manual mode
    When State is automatically changed to ON on the Client plug while in Manual mode
    Then Automatically validate current state as ON while in Manual mode
    When Mode is automatically changed to AUTO on the Client plug
    Then Automatically validate current mode as AUTO
    When State is automatically changed to OFF on the Client plug while in AUTO mode
    Then Automatically validate current state as OFF while in AUTO mode
    When State is automatically changed to ON on the Client plug while in AUTO mode
    Then Automatically validate current state as ON while in AUTO mode

  @SC-AP-MODE-STATE-01 @ActivePlugStateAndModeChanges
  Scenario Outline: SC-AP-MC-SC-01_Changing from Manual to Schedule and override the plug status and then move to manual and check for plug status.
  Again move to schedule mode to see if appropriate schedule event is reflected in state
    Given The Hive product is paired and setup for Active Plug with API Validation
    When Mode is automatically changed to AUTO on the Client plug
    Then Automatically validate current mode as AUTO
    When State is automatically changed to <Override State> on the Client plug while in AUTO mode
    Then Automatically validate current state as <Override State> while in AUTO mode
    When Mode is automatically changed to MANUAL on the Client plug
    Then Automatically validate current mode as MANUAL
    Then Automatically validate current state as <Override State> while in Manual mode
    When Mode is automatically changed to AUTO on the Client plug
    Then Automatically validate current mode as AUTO
    Then Automatically validate current state as Expected State while in Manual mode

    Examples:
      | Override State   |
      | OFF              |
      | ON               |


  @SC-AP-SH03-01 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-01_Set the given 'four' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State |
      | OFF             |
      | ON              |
      | OFF             |
      | ON              |
    Then Validate the schedule that is set

    Examples:
      | Day   |
      | Today |

    @SC-AP-SH03-02 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-02_Set the given 'four' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State |
      | ON              |
      | OFF               |
      | OFF               |
      | OFF               |
    Then Validate the schedule that is set

    Examples:
      | Day   |
      | Today |

  @SC-AP-SH03-03 @ActivePlugScheduleValidation
    #This needs to be implemented properly, as this scenario fails in DD_Web page - # Get Last events position statements - Failing in set schedue itself.
  Scenario Outline: SC-AP-SH03-03_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State |
      | OFF             |
      | ON              |
      | OFF             |
      | ON              |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples:
      | Day   |
      | Today |


  @SC-AP-SH03-04 @ActivePlugScheduleValidation
  Scenario Outline: SC-HW-SH03-04_Set the given 'four /six' event schedule with 15 minutes time difference between events with given 'Event Position' for the given day of the week and validate the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule for below 'Active Plug State' is set with current time lying on the <Event position> event, for <Day> on the Client
      | Active Plug State |
      | OFF             |
      | ON              |
      | OFF             |
      | ON              |
      | ON              |
      | OFF             |
    Then Verify if the Schedule is set

    Examples:
      | Day   | Event position |
      | Today | First          |
      | Today | Second         |
      | Today | Third          |
      | Today | Fourth         |
      #| Today | Fifth          |
      #| Today | Sixth          |

  @SC-AP-SH03-05 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-05_Set the given 'two' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State |
      | ON              |
      | OFF             |
    Then Validate the schedule that is set

    Examples:
      | Day     |
      | Tuesday |

  @SC-AP-SH03-06 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-06_Set the given customized 'four' event schedule for the given day and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State | Start Time |
      | ON                | 08:30      |
      | OFF               | 12:00      |
      | ON                | 14:00      |
      | OFF               | 16:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Friday |


  @SC-AP-SH03-07 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-07_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 00:00      |
      | OFF                | 06:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |


    @SC-AP-SH03-08 @ActivePlugScheduleValidation @AndroidRegression
  Scenario Outline: SC-AP-SH03-08_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 00:00      |
      | OFF                | 06:00      |
      | ON                 | 10:00      |
      | OFF                | 14:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |


  @SC-AP-SH03-09 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-09_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day> on the Client
      | Active Plug State  | Start Time |
      | OFF                | 12:00      |
      | ON                 | 14:00      |
      | ON                 | 16:30      |
      | OFF                | 23:45      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |


  @SC-AP-SH03-10 @ActivePlugScheduleValidation @AndroidRegression
  Scenario Outline: SC-AP-SH03-10_Reset Schedule for the given day of the week and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule is reset for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | OFF                | 08:30      |
      | ON                 | 16:00      |
      | OFF                | 21:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Friday |
      | Monday|

  @SC-AP-SH03-11 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-11_Copy the schedule of given day to another day in the app and verify the same for Active Plug
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The below schedule is set for <Day 2> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | ON                 | 08:30      |
      | ON                 | 12:00      |
      | ON                 | 14:00      |
      | ON                 | 16:30      |
      | OFF                | 22:00      |
    And The below schedule is set for <Day 1> on the Client
      | Active Plug State   | Start Time |
      | OFF                 | 06:30      |
      | OFF                 | 08:30      |
      | OFF                 | 12:00      |
      | OFF                 | 14:00      |
      | OFF                 | 16:30      |
      | OFF                 | 22:00      |
    And The schedule is copied to <Day 2> from <Day 1> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day 1  | Day 2   |
      | Friday | Monday  |

  @SC-AP-SH03-12 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-12_Create a new time slot with status as OFF and verify if other slots are affected
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule is reset for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | OFF                | 08:30      |
      | ON                 | 16:00      |
      | OFF                | 21:30      |
    And Add a time slot of <Start Time> with state as <State> for <Day> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day     |Start Time|State |
      | Today  |09:30     |OFF   |

  @SC-AP-SH03-13 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-13_Set 4 event schedule and add 3rd event today and 5th event next day
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule is reset for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | OFF                | 08:30      |
      | ON                 | 16:00      |
      | OFF                | 21:30      |
    And Add a time slot of <Start Time> with state as <State> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time|State |
      | Today     |09:30     |OFF   |
      | Tommorow  |22:00     |ON    |

  @SC-AP-SH03-14 @ActivePlugScheduleValidation @AndroidRegression
  Scenario Outline: SC-AP-SH03-14_Delete a 3rd event from today and 2nd event from next day
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule is reset for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | OFF                | 08:30      |
      | ON                 | 16:00      |
      | OFF                | 21:30      |
    And Delete a time slot of <Start Time> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time|
      | Today     |16:00     |
      | Tommorow  |21:30     |

  @SC-AP-SH03-15 @ActivePlugScheduleValidation
  Scenario Outline: SC-AP-SH03-15_Set 4 event schedule and add 3rd event today and 5th event next day
    Given The Hive product is paired and setup for Active Plug with API Validation
    When The schedule is reset for <Day> on the Client
      | Active Plug State  | Start Time |
      | ON                 | 06:30      |
      | OFF                | 08:30      |
      | ON                 | 16:00      |
      | OFF                | 21:30      |
    And Add a time slot of <Start Time> with state as <State> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time|State |
      | Today     |12:00     |OFF   |
      | Tommorow  |22:30     |ON    |