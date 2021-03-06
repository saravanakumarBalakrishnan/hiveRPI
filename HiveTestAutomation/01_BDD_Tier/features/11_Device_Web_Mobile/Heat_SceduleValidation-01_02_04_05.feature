Feature: Validate the schedules for the central heating end point in the boiler module

  @BasicSmokeTest @SC-CH-SH01-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH01-01_Set the given default 'six' event schedule for the given day and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 20.0               | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 20.0               | 16:30      |
      | 1.0                | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH02-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
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

  @BasicSmokeTest @SC-CH-SH02-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
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

  @SC-CH-SH02-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
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

  @SC-CH-SH04-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH04-01_Set the given 'six' event schedule with earliest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 00:00      |
      | 29.0               | 06:00      |
      | 1.0                | 10:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:00      |
      | 23.0               | 22:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH04-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH04-02_Set the given 'four' event schedule with earliest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 00:00      |
      | 29.0               | 06:00      |
      | 1.0                | 10:00      |
      | 30.0               | 14:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH04-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_APP
  Scenario Outline: SC-CH-SH04-03_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 00:00      |
      | 29.0               | 06:00      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH05-01 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH05-01_Set the given 'six' event schedule with latest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 15.0               | 06:30      |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
      | 23.0               | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH05-02 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
  Scenario Outline: SC-CH-SH05-02_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
      | 23.0               | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH05-03 @Heating @ScheduleTest @2_Event @Verify @All_Client @V6_App
  Scenario Outline: SC-CH-SH05-03_Set the given 'two' event schedule with latest possible event time for the given day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 16:30      |
      | 23.0               | 23:45      |
    Then Verify if the Schedule is set

    Examples: 
      | Day   |
      | Today |

  @SC-CH-SH013-W01 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App
  Scenario: SC-CH-SH01-01_Set the given custom 'six' event schedule for the whole week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for the whole week on the Client in stand alone mode
      | Day | Event1     | Event2     | Event3    | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,28.0 | 10:30,1.0 | 13:00,10.0 | 15:30,31.0 | 22:30,1.0 |
      | Tue | 06:30,16.0 | 08:30,29.0 | 10:30,1.0 | 13:00,09.0 | 15:30,32.0 | 22:30,1.0 |
      | Wed | 00:30,17.0 | 04:30,30.0 | 10:45,1.0 | 13:00,30.0 |            |           |
      | Thu | 15:30,18.0 | 18:30,31.0 | 20:30,1.0 | 23:00,08.0 | 23:30,31.5 | 23:45,1.0 |
      | Fri | 06:30,19.0 | 08:30,32.0 |           |           |            |           |
      | Sat | 06:30,20.0 | 08:30,28.0 | 10:30,1.0 | 13:00,07.0 | 15:30,30.5 | 22:30,1.0 |
      | Sun | 12:30,14.0 | 15:30,27.0 | 19:15,1.0 | 20:00,06.0 | 22:30,31.0 | 23:30,1.0 |
    Then Validate if the Schedule is set for the whole week

     @SC-CH-SH013-W02 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App
  Scenario: SC-CH-SH013-W02_Set the given custom 'six' event schedule for the whole week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for the whole week on the Client via Hub
      | Day | Event1     | Event2     | Event3    | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,28.0 | 10:30,1.0 | 13:00,10.0 | 15:30,31.0 | 22:30,1.0 |
      | Tue | 06:30,16.0 | 08:30,29.0 | 10:30,1.0 | 13:00,09.0 | 15:30,32.0 | 22:30,1.0 |
      | Wed | 00:30,17.0 | 04:30,30.0 | 10:45,1.0 | 13:00,30.0 |            |           |
      | Thu | 15:30,18.0 | 18:30,31.0 | 20:30,1.0 | 23:00,08.0 | 23:30,31.5 | 23:45,1.0 |
      | Fri | 06:30,19.0 | 08:30,32.0 |           |           |            |           |
      | Sat | 06:30,20.0 | 08:30,28.0 | 10:30,1.0 | 13:00,07.0 | 15:30,30.5 | 22:30,1.0 |
      | Sun | 12:30,14.0 | 15:30,27.0 | 19:15,1.0 | 20:00,06.0 | 22:30,31.0 | 23:30,1.0 |
    Then Validate if the Schedule is set for the whole week

   @SC-CH-SH013-W03 @Heating @ScheduleTest @6_Event @Validate @All_Client @All_App @AndroidRegression
  Scenario: SC-CH-SH01-03_Set the given custom 'six' event schedule for the whole week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for the whole week on the Client in stand alone mode
      | Day | Event1     | Event2     | Event3    | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,28.0 | 10:30,1.0 | 13:00,10.0 | 15:30,31.0 | 22:30,1.0 |
      | Tue | 06:30,16.0 | 08:30,29.0 | 10:30,1.0 | 13:00,09.0 | 15:30,32.0 | 22:30,1.0 |
      | Wed | 00:30,17.0 | 04:30,30.0 | 10:45,1.0 | 13:00,30.0 |            |           |
      | Thu | 15:30,18.0 | 18:30,31.0 | 20:30,1.0 | 23:00,08.0 | 23:30,31.5 | 23:45,1.0 |
      | Fri | 06:30,19.0 | 08:30,32.0 |           |           |            |           |
      | Sat | 06:30,20.0 | 08:30,28.0 | 10:30,1.0 | 13:00,07.0 | 15:30,30.5 | 22:30,1.0 |
      | Sun | 12:30,14.0 | 15:30,27.0 | 19:15,1.0 | 20:00,06.0 | 22:30,31.0 | 23:30,1.0 |
    Then Verify if the Schedule is set for the whole week

  @SC-CH-SH01-04 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App @ResetSchedule @AndroidRegression
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


  @SC-CH-SH01-05 @Heating @ScheduleTest @6_Event @Verify @All_Client @All_App @CopySchedule
  Scenario Outline: SC-CH-SH01-05_Copy the schedule of given day to another day in the app and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day 2> on the Client
      | Target Temperature | Start Time |
      | 20.0               | 06:30      |
      | 1.0                | 08:30      |
      | 1.0                | 12:00      |
      | 16.0               | 14:00      |
      | 18.0               | 16:30      |
      | 1.0                | 21:00      |
    Then Verify if the Schedule is set
    When The below schedule is set for <Day 1> on the Client
      | Target Temperature | Start Time |
      | 1.0                | 06:30      |
      | 20.0               | 08:30      |
      | 1.0                | 12:00      |
      | 1.0                | 14:00      |
      | 20.0               | 16:30      |
      | 1.0                | 23:00      |
    Then Verify if the Schedule is set
    When The schedule is copied to <Day 2> from <Day 1> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day 1   | Day 2   |
      | Today   | Tommorow  |


  @SC-CH-SH01-06 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App @AndroidRegression
  Scenario Outline: SC-CH-SH01-06_Create a new time slot with temp as frost and verify if other slots are affected
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
      | Day     |Start Time|temp |
      | Friday  |09:30     |1.0   |

  @SC-CH-SH01-07 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App
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

  @SC-CH-SH01-08 @Heating @ScheduleTest @4_Event @Verify @All_Client @All_App @AndroidRegression
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
