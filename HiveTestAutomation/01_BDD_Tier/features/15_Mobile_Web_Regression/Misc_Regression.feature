# Created by anuj.kumar at 03/07/2017
Feature: Validate Holiday mode changes for Central Heating

    @C265115 @Android_Regression  @HolidayMode @iOS_Regression
    Scenario Outline: SC-CH-HM-01_Validate if the user can set the Holiday Mode with default duration and can cancel the same
    Given The Hive Heating is paired with the user account
    When User navigates to activate the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be set for default duration with target temperature as <targetTemperature>
    When User navigates to cancel the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be cancelled for default duration with target temperature as <targetTemperature>

    Examples:
        |targetTemperature|
        |10               |

    @C265114 @Android_Regression  @HolidayMode @iOS_Regression
    Scenario Outline: SC-CH-HM-02_Validate if the user can set the Holiday Mode with default duration and can stop the same
    Given The Hive Heating is paired with the user account
    When User navigates to set the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be set for default duration with target temperature as <targetTemperature>
    When User navigates to stop the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be stopped for default duration with target temperature as <targetTemperature>

    Examples:
        |targetTemperature|
        |12                |

    @C265113 @Android_Regression  @HolidayMode @iOS_Regression
    Scenario Outline: SC-CH-HM-03_Validate if the user can set the Holiday Mode with future duration
    Given The Hive Heating is paired with the user account
    When User navigates to set the Holiday mode with future duration as <daysFromNow> days from now for <duration> days with target temperature as <targetTemperature>
    Then The Holiday mode should be set for future duration with target temperature as <targetTemperature>
    When User navigates to edit the Holiday mode with new duration as <newDaysFromNow> days from now for <newDuration> days with target temperature as <newTargetTemperature>
    Then The Holiday mode should be set for new duration with target temperature as <newTargetTemperature>

    Examples:
        |targetTemperature|daysFromNow|duration|newTargetTemperature|newDaysFromNow|newDuration|
        |14               |3          |5       |16                  |5             |7          |