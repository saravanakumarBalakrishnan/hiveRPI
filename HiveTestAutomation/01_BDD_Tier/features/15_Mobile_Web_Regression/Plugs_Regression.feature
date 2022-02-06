# Created by anuj.kumar at 03/07/2017
Feature: Contains all the regression scenarios related to Smart Plugs

  @iOS_Regression
  Scenario Outline: SC_Pl_PT_01_Validate the title of the plug screen.
  Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
  When User is navigated to <PlugName> Screen.
  Then Validate the <PlugName> title of the Plug Screen.
  Examples:
  | PlugName | | ModelNo |
  | Plug     | | SLP2    |

  @iOS_Regression
    Scenario Outline: SC_Pl_PS_02_Switch On and Off the Plug.
    Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
    When User is on the <PlugName> Screen.
    When User clicks on the <PlugName> toggle button.
    Then <PlugName> should be switched on or off.
    Then Validate the <PlugName> state change in Dashboard and Device Screen.

    Examples:
    | PlugName | | ModelNo |
    | Plug     | | SLP2    |

  @iOS_Regression
  Scenario Outline: SC_Pl_PM_03_Change Plug mode from manual to schedule and vice versa.
    Given Hive product <PlugName> with <ModelNo> should be paired to the Hub.
  When User is on the <PlugName> Screen.
  When User clicks on the <PlugName> arrow button from the bottom of plug screen.
  Then <PlugName> Mode should be changed either to Manual or Schedule.

  Examples:
  | PlugName | | ModelNo |
  | Plug     | | SLP2    |


  @iOS_Regression
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


  # @C265105
  @Plugs @Android_Regression @Android_SmokeTest @C111111
  Scenario: SC-AP-SC-01_Change the state of the plug from OFF to ON to OFF when plug is in manual mode and validate the same 
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

  @C265105 @Plugs @Android_Regression
  Scenario Outline: SC-AP-SC-02_Changing from Manual to Schedule and override the plug status and then move to manual and check for plug status.
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

  @C265048 @Plugs @Android_Regression @Android_SmokeTest
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
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265052 @Plugs @Android_Regression
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

  @C265041 @Plugs @Android_Regression
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

  @C265043 @Plugs @Android_Regression
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

  @C265040 @Plugs @Android_Regression
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