# Created by anuj.kumar at 25/05/2017
Feature: For validating Mode change for NA Thermostat
  # Enter feature description here

  @SC-NA-CO-MC01 @NAModeChange @AndroidRegression @AndoridSmokeTest
  Scenario Outline: SC-NA-CO-MC01_Validate the Mode change for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate current mode as OFF
    When Operating mode is changed to HOLD and temperature is set as 62 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is set as 90 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE

     Examples:
     | ThermostatState      |ThermostatName|
     | Cooling              |Cool          |

  @SC-NA-CO-MC02 @NAModeChange @AndroidRegression
  Scenario Outline: SC-NA-HO-MC02_Validate the Mode change for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate current mode as OFF
    When Operating mode is changed to HOLD and temperature is set as 62 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is set as 90 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to HOLD and temperature is set as 76 when stat is <ThermostatState>
    Then Validate current mode as HOLD

     Examples:
     | ThermostatState      |ThermostatName|
     | Heating              |Heat  |

  @SC-NA-CO-MC03 @NAModeChange @AndroidRegression
  Scenario Outline: SC-NA-DL-MC03_Validate the Heating Mode changes for NA thermostat operating in Dual Channel
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate current mode as OFF
    When Operating mode is changed to HOLD and temperature is set as 62 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is set as 90 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to HOLD and temperature is set as 76 when stat is <ThermostatState>
    Then Validate current mode as HOLD

     Examples:
     | ThermostatState     |ThermostatName|
     | Heating             |Heat  |

  @SC-NA-CO-MC04 @NAModeChange @AndroidRegression
  Scenario Outline: SC-NA-DL-MC04_Validate the Cooling Mode changes for NA thermostat operating in Dual Channel
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate current mode as OFF
    When Operating mode is changed to HOLD and temperature is set as 62 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is set as 90 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is set as 76 when stat is <ThermostatState>
    Then Validate current mode as HOLD

     Examples:
     | ThermostatState     |ThermostatName|
     | Cooling             |Cool  |

  @SC-NA-CO-MC05 @NAModeChange @AndroidRegression
  Scenario Outline: SC-NA-DL-MC05_Validate the Mode changes for NA thermostat operating in Dual Channel
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate current mode as OFF
    When Operating mode is changed to HOLD and temperature is bound between 85 and 60 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to HOLD and temperature is bound between 75 and 63 when stat is <ThermostatState>
    Then Validate current mode as HOLD
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    Then Validate current mode as SCHEDULE

   Examples:
     | ThermostatState      |ThermostatName|
     | Dual                 |Dual  |



  @SC-NA-CO-MC06 @NAFanSettings @AndroidRegression
Scenario Outline: SC-NA-DL-MC06_Validate the Fan settings by changing the NA thermostat mode
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate Fan Setting should be disabled
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate Fan Setting should be enabled
    When user select Auto in Fan Setting
    Then Validate Auto should be enabled in Fan Setting
    When user select Circulate in Fan Setting
    Then Validate Circulate should be enabled in Fan Setting
    And  it should display with 15mins, 30mins and 45mins
    When user select Circulate as 15mins in Fan Setting
    Then Verify if the selected circulate is set
    When user select Circulate as 30mins in Fan Setting
    Then Verify if the selected circulate is set
    When user select Circulate as 45mins in Fan Setting
    Then Verify if the selected circulate is set
    When user select Always on in Fan Setting
    Then Validate Always on should be enabled in Fan Setting

   Examples:
     | ThermostatState      |ThermostatName|
     | Dual                 |Dual          |


  @SC-NA-CO-MC07 @NAHumiditySettings @AndroidRegression
  Scenario Outline: SC-NA-DL-MC07_Validate the Humidity settings by changing the NA thermostat mode
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to OFF when stat is <ThermostatState>
    Then Validate Humidity Setting should be disabled
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    Then Validate Humidity Setting should be enabled
    When user sets Humidity value to <HumidityValue>
    Then Validate humidity value sets to <HumidityValue>


   Examples:
     | ThermostatState      |ThermostatName|HumidityValue|
     | Dual                 |Dual          |50           |


  @SC-NA-CO-MC08 @NA_HeatBoost
  Scenario Outline: SC-NA-DL-MC08_Validate the Boost temperature and duration in NA Heat thermostat
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    And Mode is changed to BOOST with target temperature as <Boost Temperature> for a duration of 1 hour on the Heat thermostate
    Then validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    And Mode is changed to BOOST with target temperature as <Boost Temperature> for a duration of <Duration> on the Heat thermostate
    Then validate current mode as BOOST with Target Temperature as <Boost Temperature>

   Examples:
     | ThermostatState      |ThermostatName|Boost Temperature|  |Duration|
     | Heat                 |Heat          |80               |  |2 hours  |



  @SC-NA-CO-MC09 @NA_CoolBoost
  Scenario Outline: SC-NA-DL-MC09_Validate the Boost temperature and duration in  NA Cool Thermostat
    Given <ThermostatName> is paired with NA Hive
    When Operating mode is changed to HOLD when stat is <ThermostatState>
    And Mode is changed to BOOST with target temperature as <Boost Temperature> for a duration of 1 hour on the Cool thermostate
    Then validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Operating mode is changed to SCHEDULE when stat is <ThermostatState>
    And Mode is changed to BOOST with target temperature as <Boost Temperature> for a duration of <Duration> on the Cool thermostate
    Then validate current mode as BOOST with Target Temperature as <Boost Temperature>

   Examples:
     | ThermostatState      |ThermostatName|Boost Temperature| |Duration|
     | Cool                 |Cool          |65               | |1 hour|