# Created by anuj.kumar at 28/06/2017
Feature: For validating Schedules for NA Thermostat
  # Enter feature description here

  @SC-NA-HO-SH01 @NASchedule @AndroidRegression @AndoridSmokeTest
  Scenario Outline: SC-NA-HO-SH01_Validate the Schedules for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 71                  | 06:30      |
      | 73                  | 08:30      |
      | 88                  | 12:00      |
      | 80                  | 14:00      |
      | 83                  | 16:30      |
      | 67                  | 21:00      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Heating           |Thermostat 1   |Today   |

    @SC-NA-HO-SH02 @NASchedule @AndroidRegression
    Scenario Outline: SC-NA-HO-SH02_Validate the Schedules for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 75                  | 06:30      |
      | 62                  | 08:30      |
      | 62                  | 12:00      |
      | 90                  | 21:00      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Heating           |Thermostat 1   |Today   |

   @SC-NA-HO-SH03 @NASchedule @AndroidRegression
   Scenario Outline: SC-NA-HO-SH03_Validate the Schedules for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 45                  | 23:45      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Heating           |Thermostat 1   |Today   |

  @SC-NA-HO-SH04 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-HO-SH04_Validate the Schedules for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 90                  | 00:00      |
      | 45                  | 23:45      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Heating           |Thermostat 1   |Today   |

  @SC-NA-HO-SH05 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-HO-SH05_Validate the Schedules for NA thermostat operating in Heating Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  |
      | 45                  |
      | 62                  |
      | 76                  |
      | 90                  |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Heating           |Thermostat 1   |Today   |

  @SC-NA-HO-SH06 @NASchedule @AndroidRegression @AndoridSmokeTest
  Scenario Outline: SC-NA-CO-SH06_Validate the Schedules for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 71                  | 06:30      |
      | 73                  | 08:30      |
      | 62                  | 12:00      |
      | 80                  | 14:00      |
      | 63                  | 16:30      |
      | 67                  | 21:00      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Cooling           |Thermostat 1   |Today   |

  @SC-NA-HO-SH07 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-CO-SH07_Validate the Schedules for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 78                  | 09:30      |
      | 73                  | 12:30      |
      | 83                  | 15:45      |
      | 67                  | 23:15      |
    Then Verify if the Schedule is set

    Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Cooling           |Thermostat 1   |Today   |

  @SC-NA-HO-SH08 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-CO-SH08_Validate the Schedules for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 85                  | 00:00      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Cooling           |Thermostat 1   |Today   |

  @SC-NA-HO-SH09 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-CO-SH09_Validate the Schedules for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 62                  | 00:00      |
      | 90                  | 23:45      |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Cooling           |Thermostat 1   |Today   |

  @SC-NA-HO-SH10 @NASchedule @AndroidRegression
  Scenario Outline: SC-NA-CO-SH10_Validate the Schedules for NA thermostat operating in Cooling Only
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  |
      | 62                  |
      | 90                  |
      | 75                  |
      | 85                  |
    Then Verify if the Schedule is set

     Examples:
     | ThermostatState   |ThermostatName |Day     |
     | Cooling           |Thermostat 1   |Today   |

  @SC-NA-DL-SH11 @NASchedule @AndroidRegression
   Scenario Outline: SC-NA-DL-SH07_Validate the Schedules for NA thermostat operating in Dual Mode
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 82--78                  | 09:30      |
      | 82--78                  | 12:30      |
      | 82--78                  | 15:45      |
      | 90--87                  | 17:15      |
      | 75--64                  | 19:15      |
      | 82--78                  | 23:15      |
    Then Verify if the Schedule is set

    Examples:
     | ThermostatState    |ThermostatName   |Day     |
     | Dual               |Thermostat 1     |Today   |


  @SC-NA-DL-SH12 @NASchedule @AndroidRegression
   Scenario Outline: SC-NA-DL-SH07_Validate the Schedules for NA thermostat operating in Dual Mode
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 82--78                  | 09:30      |
      | 82--78                  | 12:30      |
      | 82--78                  | 15:45      |
      | 90--87                  | 17:15      |
    Then Verify if the Schedule is set

    Examples:
     | ThermostatState    |ThermostatName   |Day     |
     | Dual               |Thermostat 1     |Today   |


  @SC-NA-DL-SH13 @NASchedule @AndroidRegression
   Scenario Outline: SC-NA-DL-SH07_Validate the Schedules for NA thermostat operating in Dual Mode
    Given <ThermostatName> is paired with NA Hive
    When The below schedule is set for <Day> when stat is <ThermostatState>
      | Target Temperature  | Start Time |
      | 82--78                  | 00:00      |
      | 82--78                  | 23:45      |

    Then Verify if the Schedule is set

    Examples:
     | ThermostatState    |ThermostatName   |Day     |
     | Dual               |Thermostat 1     |Today   |