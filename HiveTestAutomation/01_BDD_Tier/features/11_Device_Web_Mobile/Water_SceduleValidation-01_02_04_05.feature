Feature: Validate the schedules for the central heating end point in the boiler module

  @SC-HW-SH01-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App 
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

  @BasicSmokeTest  @SC-HW-SH02-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App @AndroidRegression
  Scenario Outline: SC-HW-SH02-01_Set the given customized 'six' event schedule for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | ON              | 08:30      |
      | OFF             | 11:00      |
      | ON              | 13:45      |
      | OFF             | 15:30      |
      | OFF             | 23:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @BasicSmokeTest @SC-HW-SH02-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH02-02_Set the given customized 'four' event schedule for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 08:30      |
      | OFF             | 12:00      |
      | ON              | 14:00      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH02-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @V6_App 
  Scenario Outline: SC-HW-SH02-03_Set the given customized 'two' event schedule for the given day and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 14:00      |
      | OFF             | 16:30      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH04-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH04-01_Set the given 'six' event schedule with earliest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 00:00      |
      | ON              | 06:00      |
      | OFF             | 10:00      |
      | ON              | 14:00      |
      | OFF             | 16:00      |
      | OFF             | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH04-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH04-02_Set the given 'four' event schedule with earliest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 00:00      |
      | OFF             | 06:00      |
      | ON              | 10:00      |
      | OFF             | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH04-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @All_App 
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

  @SC-HW-SH05-01 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH05-01_Set the given 'six' event schedule with latest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | ON              | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:30      |
      | ON              | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH05-02 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH05-02_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | OFF             | 12:00      |
      | ON              | 14:00      |
      | ON              | 16:30      |
      | OFF             | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-HW-SH05-03 @HotWater @ScheduleTest @2_Event @Verify @All_Client @All_App 
  Scenario Outline: SC-HW-SH05-03_Set the given 'two' event schedule with latest possible event time for the given day of the week and verify the same for Hot Water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 16:30      |
      | OFF             | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |


@SC-HW-SH01-04 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App @ResetSchedule @AndroidRegression
  Scenario Outline: SC-HW-SH01-04_Reset Schedule for the given day of the week and verify the same for Hot water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The schedule is reset for <Day> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | ON              | 16:00      |
      | OFF             | 21:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day     |
      | Today   |

  @SC-HW-SH01-05 @HotWater @ScheduleTest @6_Event @Verify @All_Client @All_App @CopySchedule
  Scenario Outline: SC-HW-SH01-05_Copy the schedule of given day to another day in the app and verify the same for Hot water
    Given The Hive product is paired and setup for Hot Water with API Validation
    When The below schedule is set for <Day 2> on the Client
      | Hot Water State | Start Time |
      | OFF             | 06:30      |
      | OFF             | 08:30      |
      | OFF             | 12:00      |
      | OFF             | 14:00      |
      | OFF             | 16:30      |
      | OFF             | 23:45      |
    Then Verify if the Schedule is set
    When The below schedule is set for <Day 1> on the Client
      | Hot Water State | Start Time |
      | ON              | 06:30      |
      | ON              | 08:30      |
      | ON              | 12:00      |
      | ON              | 14:00      |
      | ON              | 16:30      |
      | OFF             | 23:45      |
    Then Verify if the Schedule is set
    When The schedule is copied to <Day 2> from <Day 1> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day 1  | Day 2   |
      | Friday | Monday  |


  @SC-HW-SH01-06 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-HW-SH01-06_Create a new time slot with state as OFF and verify if other slots are affected
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
      | Day     |Start Time|state |
      | Friday  |09:30     |OFF   |

  @SC-HW-SH01-07 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App
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

  @SC-HW-SH01-08 @HotWater @ScheduleTest @4_Event @Verify @All_Client @All_App @AndroidRegression
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
