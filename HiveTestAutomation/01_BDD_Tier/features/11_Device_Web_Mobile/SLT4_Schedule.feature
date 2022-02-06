# Created by anand.ramakrishnan at 28/12/2017
Feature: Regression cases for SLT4 stat to validate schedule


  @STH_US_RegressionTest @STH_SCH_REG_001
  Scenario Outline: STH_SCH_REG_001_Set the given custom 'six' event schedule for the whole week and reset the value for today in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Sun | 09:30,30.0 | 18:30,31.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,17.0 |
      | Mon | 09:30,30.0 | 18:30,31.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,18.0 |
      | Tue | 04:30,18.0 | 18:30,25.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,17.0 |
      | Wed | 04:30,18.0 | 18:30,31.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,17.0 |
      | Thu | 15:30,18.0 | 18:30,31.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,17.0 |
      | Fri | 06:00,32.0 | 08:30,31.0 | 12:30,21.0 | 14:00,18.0 | 18:30,31.5 | 22:45,17.0 |
      | Sat | 15:30,18.0 | 18:30,31.0 | 20:30,21.0 | 23:00,18.0 | 23:30,31.5 | 23:45,17.0 |
    Then Verify if the Schedule is set in SLT4
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 08:30,25.0 | 12:30,21.0 | 14:00,18.0 | 18:30,27.5 | 22:45,17.0 |
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |


  @STH_US_RegressionTest @STH_SCH_REG_002
  Scenario Outline: STH_SCH_REG_002_Set the given custom 'six' event schedule for the whole week and reset the value for today in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Sun | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
      | Mon | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
      | Tue | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
      | Wed | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
      | Thu | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
      | Fri | 06:00,64.0 | 08:30,87.0 | 12:30,69.0 | 14:00,82.0 | 18:30,88.5 | 22:45,62.0 |
      | Sat | 15:30,64.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
    Then Verify if the Schedule is set in SLT4
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,80.0 | 18:30,80.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
    Then Verify if the Schedule is set in SLT4
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

@STH_US_RegressionTest @STH_SCH_REG_003
  Scenario Outline: STH_SCH_REG_003 verify the given schedule is override by a values in fahrenheit scale
  Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
  When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,70.0 | 10:30,80.0 | 12:30,69.0 | 15:00,82.0 | 18:30,70.5 | 23:45,79.0 |
  When The temperature is overridden by <change> points
  Then The temperature should be changed by <change> points
  Examples: Different schedule modes
  |device_mode    |change|
  |HEAT SCHEDULE  |2     |
  |COOL SCHEDULE  |2     |
  |DUAL SCHEDULE  |3     |

@STH_US_RegressionTest @STH_SCH_REG_004
  Scenario Outline: STH_SCH_REG_004 verify the given schedule is override by a values in celcius scale
  Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
  When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 08:30,25.0 | 12:30,21.0 | 14:00,18.0 | 18:30,27.5 | 22:45,17.0 |
  When The temperature is overridden by <change> points
  Then The temperature should be changed by <change> points
  Examples: Different schedule modes
  |device_mode    |change|
  |HEAT SCHEDULE  |2     |
  |COOL SCHEDULE  |2     |
  |DUAL SCHEDULE  |3     |


  @STH_US_RegressionTest @STH_SCH_REG_005
    Scenario Outline: STH_SCH_REG_005_Verify if the set schedule is copied to remaining days in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 08:30,25.0 | 12:30,21.0 | 14:00,18.0 | 18:30,27.5 | 22:45,17.0 |
    Then Verify if the Schedule is set in SLT4
    When Above events are to be copied for <days>
    Then Verify the schedule is copied to the mentioned days
    Examples: Different schedule modesx
    |device_mode    |days             |
    |HEAT SCHEDULE  |SATURDAY,SUNDAY  |
    |COOL SCHEDULE  |SATURDAY,SUNDAY  |
    |DUAL SCHEDULE  |SATURDAY,SUNDAY  |

  @STH_US_RegressionTest @STH_SCH_REG_006
    Scenario Outline: STH_SCH_REG_006_Verify if the set schedule is copied to remaining days in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,70.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
    Then Verify if the Schedule is set in SLT4
    When Above events are to be copied for <days>
    Then Verify the schedule is copied to the mentioned days
    Examples: Different schedule modesx
    |device_mode    |days             |
    |HEAT SCHEDULE  |SATURDAY,SUNDAY  |
    |COOL SCHEDULE  |SATURDAY,SUNDAY  |
    |DUAL SCHEDULE  |SATURDAY,SUNDAY  |

  @STH_US_RegressionTest @STH_SCH_REG_007
    Scenario Outline: STH_SCH_REG_007_Verify if the said timeslot to the schedule is added in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,80.0 | 18:30,65.0 | 20:30,69.0 |            |            |            |
    Then Verify if the Schedule is set in SLT4
    When Below events are added from the schedule
      | To be Added   |
      | 12:30,70.0    |
      | 23:45,62.0    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

  @STH_US_RegressionTest @STH_SCH_REG_008
    Scenario Outline: STH_SCH_REG_008_Verify if the said timeslot to the schedule is added in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 13:30,25.0 | 16:00,18.0 |            |            |            |
    Then Verify if the Schedule is set in SLT4
    When Below events are added from the schedule
      | To be Added   |
      | 12:30,21.0    |
      | 23:45,15.0    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

  @STH_US_RegressionTest @STH_SCH_REG_009
    Scenario Outline: STH_SCH_REG_009_Verify if the said timeslot from the schedule is deleted in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 08:30,25.0 | 12:30,21.0 | 14:00,18.0 | 18:30,27.5 | 22:45,17.0 |
    Then Verify if the Schedule is set in SLT4
    When Below events are deleted from the schedule
      | To be Deleted |
      | 06:00,28.0    |
      | 12:30,21.0    |
      | 18:30,27.5    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |


  @STH_US_RegressionTest @STH_SCH_REG_0010
    Scenario Outline: STH_SCH_REG_0010_Verify if the said timeslot from the schedule is deleted in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,80.0 | 18:30,80.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
    Then Verify if the Schedule is set in SLT4
    When Below events are deleted from the schedule
      | To be Deleted |
      | 18:30,80.0    |
      | 23:00,82.0    |
      | 23:45,62.0    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |


  @STH_US_RegressionTest @STH_SCH_REG_011
    Scenario Outline: STH_SCH_REG_011_Verify if the 2-3-4-5-6 timeslot is added in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:30,80.0 |            |            |            |            |            |
    Then Verify if the Schedule is set in SLT4
    When Below events are added from the schedule
      | To be Added   |
      | 12:30,70.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 15:30,65.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 18:30,80.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 20:30,69.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 23:45,75.0    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

  @STH_US_RegressionTest @STH_SCH_REG_012
    Scenario Outline: STH_SCH_REG_012_Verify if the 2-3-4-5-6 timeslot is added in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,20.0 |            |            |            |            |            |
    Then Verify if the Schedule is set in SLT4
    When Below events are added from the schedule
      | To be Added   |
      | 10:30,32.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 12:30,21.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 16:00,29.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 20:00,15.0    |
    Then Verify the events before and after change
    When Below events are added from the schedule
      | To be Added   |
      | 23:45,25.0    |
    Then Verify the events before and after change
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |



@STH_US_RegressionTest @STH_SCH_REG_013
    Scenario Outline: STH_SCH_REG_013_Set the given custom 'six' event schedule for today & powercycled in fahrenheit scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,70.0 | 18:30,87.0 | 20:30,69.0 | 23:00,82.0 | 23:30,88.5 | 23:45,62.0 |
    Then Verify if the Schedule is set in SLT4
    When The device is rebooted
    Then Verify if the Schedule is set in SLT4
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

@STH_US_RegressionTest @STH_SCH_REG_014
    Scenario Outline: STH_SCH_REG_014_Set the given custom 'six' event schedule for today & powercycled in celcius scale
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  CELCIUS scale
    When The Below <device_mode> is set in Hub mode
      | Day   | Event1     | Event2     | Event3     | Event4     | Event5     | Event6     |
      | Today | 06:00,28.0 | 08:30,25.0 | 12:30,21.0 | 14:00,18.0 | 18:30,27.5 | 22:45,17.0 |
    Then Verify if the Schedule is set in SLT4
    When The device is rebooted
    Then Verify if the Schedule is set in SLT4
    Examples: Different schedule modes
    |device_mode    |
    |HEAT SCHEDULE  |
    |COOL SCHEDULE  |
    |DUAL SCHEDULE  |

