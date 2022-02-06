#Created on 28 May 2017
#Modified on NA
#@authors: 
#iOS        - TBD
#Android    - Anuj
#Web        - TBD
Feature: Validate Leak sensor feature

    @SC-LD-AF_01 @LeakSensor @C214623
    Scenario: SC-LD-AF_01_Validate the Status of Leak Sensor
    Given A Leak sensor is paired with the user
    When User checks the current leak status in the App
    Then The leak status should be displayed as expected


    #Use Notification Simulator
    @SC-LD-AF_02 @LeakSensor @C214627
    Scenario: SC-LD-AF_02_Validate the various status updates of Leak Sensor
    Given A Leak sensor is paired with the user
    When Flow None Notification is triggered
    Then The leak status should be displayed as expected
    When Small Leak Notification is triggered
    Then The leak status should be displayed as expected
    When Flow None Notification is triggered
    Then The leak status should be displayed as expected
    When Large Flow Notification is triggered
    Then The leak status should be displayed as expected
    When Flow None Notification is triggered
    Then The leak status should be displayed as expected

    @SC-LD-AF_03 @LeakSensor @C214627
    Scenario: SC-LD-AF_03_Validate the various status updates of Leak Sensor
    Given A Leak sensor is paired with the user
    When Flow None Notification is triggered
    Then The leak status should be displayed as expected

    @SC-LD-AF_04 @LeakSensor @C214627
    Scenario: SC-LD-AF_04_Validate the Alert settings updates
    Given A Leak sensor is paired with the user
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Active       |
      | Email      | Active       |
      | Text       | Inactive     |
    Then Validate if the alert settings are set as expected


   @SC-LD-AF_05 @LeakSensor @C214627
    Scenario: SC-LD-AF_04_Validate the All Alert settings combinations
    Given A Leak sensor is paired with the user
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Active       |
      | Email      | Active       |
      | Text       | Inactive     |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Inactive     |
      | Email      | Active       |
      | Text       | Active       |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Active       |
      | Email      | Inactive     |
      | Text       | Active       |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Active       |
      | Email      | Inactive     |
      | Text       | Inactive     |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Inactive     |
      | Email      | Inactive     |
      | Text       | Active       |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Inactive     |
      | Email      | Active       |
      | Text       | Inactive     |
    Then Validate if the alert settings are set as expected
    When Alert Settings are updated as listed below
      | Alert Type | Alert Status |
      | Push       | Active       |
      | Email      | Active       |
      | Text       | Active       |
    Then Validate if the alert settings are set as expected


  @SC-LD-AF_06 @LeakSensor @C214627
    Scenario Outline: SC-LD-AF_06_Validate if the min leak duration setting is updated
    Given A Leak sensor is paired with the user
    When Min Leak duration is set as <minLeakdDuration> mins
    Then Validate if the Min Leak duration is set as expected
    Examples:
        |minLeakdDuration   |
        |25                 |

   #Use Notification Simulator and alert settings API call
    #Use Notification Simulator
    @SC-LD-AF_07 @LeakSensor @C214627
    Scenario Outline: SC-LD-AF_05_Validate the various status updates of Leak Sensor
    Given A Leak sensor is paired with the user along with alert settings
      | Alert Type             | Alert Status   |
      | PushNotification       | <Push>         |
      | SendEmail              | <Email>        |
      | SendSubscriptionSMS    | <Text>         |
    When Small Leak Notification is triggered
    Then The leak status should be displayed as expected
    When Large Flow Notification is triggered
    Then The leak status should be displayed as expected
    When Flow None Notification is triggered
    Then The leak status should be displayed as expected

      Examples:
        |Push       |Email        |Text       |
        |Active     |Active       |Active     |
        |Active     |Inactive     |Inactive   |
        |Active     |Active       |Inactive   |
        |Active     |Inactive     |Active     |
        |Inactive   |Active       |Active     |
        |Inactive   |INACTIVE     |Active     |
        |Inactive   |Active       |INACTIVE   |