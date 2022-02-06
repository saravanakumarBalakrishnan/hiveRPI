# Created by anuj.kumar at 07/09/2017
Feature: Dynamic Troubleshooting for Leak
  # Enter feature description here

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_01
  Scenario: SC-LD-DT_01_Validate High Water Usage Pop up
    Given A Leak sensor is paired with the user along with alert settings
      | Alert Type             | Alert Status   |
      | PushNotification       | Active         |
      | SendEmail              | Active         |
      | SendSubscriptionSMS    | Active         |
    When High Water Usage Notification is triggered
    Then The banner appears on the product page

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_02
  Scenario: SC-LD-DT_02_Validate Low Water flow Pop up
    Given A Leak sensor is paired with the user along with alert settings
      | Alert Type             | Alert Status   |
      | PushNotification       | Active         |
      | SendEmail              | Active         |
      | SendSubscriptionSMS    | Active         |
    When Low Water Flow Notification is triggered
    Then The banner appears on the product page

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_03
  Scenario: SC-LD-DT_03_Validate Low Water flow troubleshooting navigation
    Given A Leak sensor is paired with the user
    When Leak status is set as Low Water Flow
    Then Load troubleshooting screen

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_04
  Scenario: SC-LD-DT_04_Validate High Water usage troubleshooting navigation
    Given A Leak sensor is paired with the user
    When Leak status is set as High water usage
    Then Load troubleshooting screen

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_05
  Scenario:SC-LD-DT_05_Validate the intentional usage
    Given A Leak sensor is paired with the user
    When Leak status is set as High water usage
    And It is an intended usage
    Then The leak status should be displayed as expected

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_06
  Scenario: SC-LD-DT_06_Validate if the user chooses to remind me later
    Given A Leak sensor is paired with the user
    When Leak status is set as Low Water Flow
    And user inputs to remind me later
    Then The leak status should be displayed as expected
    When User navigates around the app
    Then the pop is not reappeared

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_07
  Scenario: SC-LD-DT_07_Validate if the user fixes the low water flow
    Given A Leak sensor is paired with the user
    When Leak status is set as Low Water Flow
    Then Load troubleshooting screen
    When User is fixing the problem
    Then The leak status should be displayed as expected

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_08
  Scenario: SC-LD-DT_08_Validate if the user fixes high water usage
    Given A Leak sensor is paired with the user
    When Leak status is set as High water usage
    Then Load troubleshooting screen
    When User is fixing the problem
    Then The leak status should be displayed as expected

   @LeakSensor @DynamicTroubleshooting @SC-LD-DT_09
  Scenario: SC-LD-DT_09_Validate if the user ignores the low water flow
    Given A Leak sensor is paired with the user
    When Leak status is set as Low Water Flow
    Then Load troubleshooting screen
    When User ignores the leak after troubleshooting
    Then The leak status should be displayed as expected

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_10
  Scenario: SC-LD-DT_10_Validate if the user ignores high water usage
    Given A Leak sensor is paired with the user
    When Leak status is set as High water usage
    Then Load troubleshooting screen
    When User ignores the leak after troubleshooting
    Then The leak status should be displayed as expected

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_11
  Scenario: SC-LD-DT_11_Validate if the user calls plumber for the low water flow
    Given A Leak sensor is paired with the user
    When Leak status is set as Low Water Flow
    Then Load troubleshooting screen
    When User is calling a plumber
    Then The leak status should be displayed as expected

  @LeakSensor @DynamicTroubleshooting @SC-LD-DT_12
  Scenario: SC-LD-DT_12_Validate if the user calls plumber for high water usage
    Given A Leak sensor is paired with the user
    When Leak status is set as High water usage
    Then Load troubleshooting screen
    When User is calling a plumber
    Then The leak status should be displayed as expected