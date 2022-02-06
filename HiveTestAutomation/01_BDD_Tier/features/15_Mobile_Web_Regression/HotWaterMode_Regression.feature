# Created by anuj.kumar at 03/07/2017
Feature: Validate the various mode changes for Hot Water

  @C265077 @HotWaterMode @Android_Regression  @Android_SmokeTest @iOS_Regression
  Scenario Outline: SC-HW-MC01_Validate the Mode change for Hot Water on the Boiler Module
    Given The Hive product is paired and setup for Hot Water with API Validation
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to Always ON on the Client
    Then Automatically validate current mode as Always ON
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO
    When Mode is automatically changed to BOOST on the Client
    Then Automatically validate current mode as BOOST
    When Mode is automatically changed to Always OFF on the Client
    Then Automatically validate current mode as Always OFF

    Examples:
      | Duration | CheckInterval |
      | 120      | 20            |
