# Created by anuj.kumar at 03/07/2017
Feature: Validate the schedules for the central heating end point in the boiler module

  @C265100 @HotWaterSchedule @Android_Regression  @Android_SmokeTest
  Scenario Outline: SC-HW-SH01-01_Set the given default 'six' event schedule for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:00      |
      | OFF             | 21:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265104 @HotWaterSchedule @Android_Regression
  Scenario Outline: SC-HW-SH04-03_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 00:00      |
      | OFF             | 06:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day   |
      | Today |

  @C265103 @HotWaterSchedule @Android_Regression
  Scenario Outline: SC-HW-SH01-07_Set 4 event schedule and add 3rd event today and 5th event next day and verify the same for Hot water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
    Then Verify if the Schedule is set
    When Add a time slot of <Start Time> with state as <state> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day       |Start Time  |state  |
      | Today     |13:00       |OFF    |
      | Tomorow   |18:00       |OFF    |

  @C265101 @HotWaterSchedule @Android_Regression
  Scenario Outline: SC-HW-SH01-08_Delete a 3rd event from today and 2nd event from next day and verify the same for Hot water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
    And Delete a time slot of <Start Time> for <Day> on the Client
    Then Verify if the Schedule is set
    Examples:
      | Day         |Start Time|
      | Friday      |12:00     |

  @C265102 @HotWaterSchedule @Android_Regression
  Scenario Outline: SC-HW-SH01-04_Reset Schedule for the given day of the week and verify the same for Hot water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The schedule is reset for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:30      |
      | OFF             | 22:00      |
    Then Verify if the Schedule is set

    Examples:
      | Day     |
      | Today   |