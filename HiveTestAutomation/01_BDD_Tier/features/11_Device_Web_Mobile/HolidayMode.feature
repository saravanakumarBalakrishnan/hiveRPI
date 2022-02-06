#Created by selvaraj.kuppusamy at 04/01/2017
#Modified on 04 Apr 2017
#@authors:
#iOS        - Meenakshi
#Android    - Anuj
#Web        - Selva

Feature: Validate Holiday mode changes for Central Heating

    @SC-HM-01 @C196131 @HolidayMode
    Scenario Outline: SC-CH-HM-01_Validate if the user can set the Holiday Mode with default duration and can cancel the same
    Given The Hive Heating is paired with the user account
    When User navigates to activate the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be set for default duration with target temperature as <targetTemperature>
    When User navigates to cancel the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be cancelled for default duration with target temperature as <targetTemperature>

    Examples:
        |targetTemperature|
        |10               |

    @SC-HM-02 @C57822 @C196129 @HolidayMode
    Scenario Outline: SC-CH-HM-02_Validate if the user can set the Holiday Mode with default duration and can stop the same
    Given The Hive Heating is paired with the user account
    When User navigates to set the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be set for default duration with target temperature as <targetTemperature>
    When User navigates to stop the Holiday mode with default duration with target temperature as <targetTemperature>
    Then The Holiday mode should be stopped for default duration with target temperature as <targetTemperature>

    Examples:
        |targetTemperature|
        |12                |

    @SC-HM-03 @C196127 @HolidayMode @C196130
    Scenario Outline: SC-CH-HM-03_Validate if the user can set the Holiday Mode with future duration
    Given The Hive Heating is paired with the user account
    When User navigates to set the Holiday mode with future duration as <daysFromNow> days from now for <duration> days with target temperature as <targetTemperature>
    Then The Holiday mode should be set for future duration with target temperature as <targetTemperature>
    When User navigates to edit the Holiday mode with new duration as <newDaysFromNow> days from now for <newDuration> days with target temperature as <newTargetTemperature>
    Then The Holiday mode should be set for new duration with target temperature as <newTargetTemperature>

    Examples:
        |targetTemperature|daysFromNow|duration|newTargetTemperature|newDaysFromNow|newDuration|
        |14               |3          |5       |16                  |5             |7          |