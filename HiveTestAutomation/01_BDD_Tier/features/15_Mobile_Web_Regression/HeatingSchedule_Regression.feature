# Created by anuj.kumar at 03/07/2017
Feature: Validate the schedules for the central heating end point in the boiler module
  # Enter feature description here

  @C265074 @HeatSchedule @Android_Regression  @Android_SmokeTest
  Scenario Outline: SC-CH-SH02-01_Set the given customized 'six' event schedule for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
      | 23.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265079 @HeatSchedule @Android_Regression
  Scenario Outline: SC-CH-SH02-02_Set the given customized 'four' event schedule for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265075 @HeatSchedule @Android_Regression
  Scenario Outline: SC-CH-SH02-03_Set the given customized 'two' event schedule for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265028 @HeatSchedule @Android_Regression
  Scenario Outline: SC-CH-SH01-04_Reset Schedule for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The schedule is reset for <Day> on the Client
      | Target Temperature | Start Time |
      | 20.0               | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 20.0               | 16:30      |
      | 1.0                | 22:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day     |
      | Friday  |

  @C265030 @HeatSchedule @Android_Regression
  Scenario Outline: SC-CH-SH01-07_Set 4 event schedule and add 3rd event today and 5th event next day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 20.0               | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
    Then Verify if the Schedule is set
    When Add a time slot of <Start Time> with temp as <temp> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time     |temp  |
      | Today     |09:30          |1.0   |
      | Tommorow  |18:30          |22.0  |

  @C265027 @HeatSchedule @Android_Regression
  Scenario Outline: SC-CH-SH01-08_Delete a 3rd event from today and 2nd event from next day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 20.0               | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
    Then Verify if the Schedule is set
    When Delete a time slot of <Start Time> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time|
      | Today     |12:00     |
      | Tommorow  |08:30     |