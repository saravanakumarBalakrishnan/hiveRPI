# Created by Rajeshwari.Srinivasan at 30/08/2017
Feature: Smart Home Skill - Active Heating features
  Contains the scenarios for controlling Hive active heating via Alexa Smart home skills

  @Alexa_SHS_T01
  Scenario: Alexa_SHS_T01_To verify setting temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa set <Active Heating> to 20 degrees
    Then I get a confirmation response from Alexa on heating
    And validate mode as MANUAL with Target Temperature as 20.0

  @Alexa_SHS_T02
  Scenario: Alexa_SHS_T02_To verify setting invalid temperature on active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa set <Active Heating> to 1 degree
    Then I get a error response from Alexa on heating

  @Alexa_SHS_T03
  Scenario: Alexa_SHS_T03_To verify setting outbound temperature on active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa set <Active Heating> to 36 degrees
    Then I get a error response from Alexa on heating

  @Alexa_SHS_T04
  Scenario: Alexa_SHS_T04_To verify turn off active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa turn off <Active Heating>
    Then I get a confirmation response from Alexa on heating

  @Alexa_SHS_T05
  Scenario: Alexa_SHS_T05_To verify temperature query on active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa what is the <Active Heating> set to
    Then I get a confirmation response from Alexa on heating

  @Alexa_SHS_T06
  Scenario: Alexa_SHS_T06_To verify setting temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa set <Active Heating> to 15 degrees
    Then I get a confirmation response from Alexa on heating
    And validate mode as MANUAL with Target Temperature as 15.0

  @Alexa_SHS_T07
  Scenario: Alexa_SHS_T07_To verify increase temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa increase <Active Heating> by 5 degrees
    Then I get a confirmation response from Alexa on heating
    And validate mode as MANUAL with Target Temperature as 20.0

  @Alexa_SHS_T08
  Scenario: Alexa_SHS_T08_To verify increase invalid temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa increase <Active Heating> by 25 degrees
    Then I get a error response from Alexa on heating

  @Alexa_SHS_T09
  Scenario: Alexa_SHS_T09_To verify decrease temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa decrease <Active Heating> by 5 degrees
    Then I get a confirmation response from Alexa on heating
    And validate mode as MANUAL with Target Temperature as 20.0

  @Alexa_SHS_T10
  Scenario: Alexa_SHS_T10_To verify decrease invalid temperature for active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa decrease <Active Heating> by 25 degrees
    Then I get a error response from Alexa on heating

  @Alexa_SHS_T11
  Scenario: Alexa_SHS_T11_To verify turning on active heating
    Given Alexa user is setup with Hive devices and <Active Heating> for SmartHome skill validation
    And Rename <Active Heating> to DeviceName
    When For Heating I say Alexa turn on my <Active Heating>
    Then I get a error response from Alexa on heating