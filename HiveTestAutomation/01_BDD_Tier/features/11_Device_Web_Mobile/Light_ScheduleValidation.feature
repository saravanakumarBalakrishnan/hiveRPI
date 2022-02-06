Feature: Validate the schedules for the Active lights

  @SC-WWL-SH-01 @WarmWhiteLightScheduleTest @LightScheduleTest @C130408
  Scenario Outline: SC-WWL-SH-01_Set the given default 'four' event schedule for the given day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 08:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-02 @WarmWhiteLightScheduleTest @LightScheduleTest
  Scenario Outline: SC-WWL-SH-02_Set the given customized 'four' event schedule for the given day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 09:30       | ON         | 60                |
      | 11:30       | OFF        | 0                 |
      | 19:00       | OFF        | 0                 |
      | 22:30       | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-WWL-SH-03 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-03_Set the given customized 'four' event schedule for the given day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 09:30       | ON         | 60                |
      | 11:30       | ON         | 90                |
      | 14:00       | ON         | 70                |
      | 18:30       | ON         | 5                 |
      | 20:00       | ON         | 70                |
      | 22:30       | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-WWL-SH-04 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-04_Set the given customized 'two' event schedule for the given day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 10:00       | ON         | 60                |
      | 19:30       | OFF        | 0                 |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-05 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-05_Set the given 'four' event schedule with earliest possible event time for the given day of the week and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 00:00       | ON         | 60                |
      | 11:30       | ON         | 5                 |
      | 19:00       | ON         | 70                |
      | 22:30       | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-06 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-06_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 00:00       | ON         | 10                |
      | 20:30       | ON         | 5                 |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-07 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-07_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 12:00       | ON         | 60                |
      | 14:00       | ON         | 5                 |
      | 16:30       | ON         | 70                |
      | 23:45       | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-08 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-08_Set the given 'two' event schedule with latest possible event time for the given day of the week and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 16:30       | ON         | 70                |
      | 23:45       | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-09 @WarmWhiteLightScheduleTest
  Scenario Outline: SC-WWL-SH-09_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day> on the Client
      | Status     | Brightness Value  |
      | ON         | 60                |
      | ON         | 5                 |
      | ON         | 70                |
      | ON         | 40                |
      | OFF        | 0                 |
      | ON         | 40                |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-WWL-SH-10 @WarmWhiteLightScheduleTest @LightScheduleTest @ResetSchedule @C130409
  Scenario Outline: SC-WWL-SH-10_Reset event schedule for the given day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 08:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-WWL-SH-11 @WarmWhite @LightScheduleTest @AddSchedule @C130415
  Scenario Outline: SC-WWL-SH-11_Create a new time slot and verify if other slots are affected for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   |
      | 06:30       | ON         | 100                |
      | 08:30       | OFF        | 0                  |
      | 16:00       | ON         | 100                |
      | 21:30       | OFF        | 0                  |
    Then Verify if the Warm White Light Schedule is set
    When Add the below time slot for active light on <Day> on the Client
      | Start Time  | Status     | Brightness Value   |
      | 09:30       | ON         | 70                |
    Then Verify if the Warm White Light Schedule is set
    Examples:
      | Day     |
      | Friday  |

  @SC-WWL-SH-12 @WarmWhite @LightScheduleTest @LightScheduleTest @DelSchedule @C130415
   Scenario Outline: SC-WWL-SH-12_Delete a 3rd event from today and 2nd event from next day and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   |
      | 06:30       | ON         | 100                |
      | 08:30       | OFF        | 0                  |
      | 16:00       | ON         | 100                |
      | 21:30       | OFF        | 0                  |
    Then Verify if the Warm White Light Schedule is set
    When Delete a time slot for active light of <Start Time> for <Day> on the Client
    Then Verify if the Warm White Light Schedule is set
    Examples:
      | Day           |Start Time|
      | Today         |16:00     |
      | Tommorow      |08:30     |

  @SC-WWL-SH-13 @WarmWhite @LightScheduleTest @LightScheduleTest @CopySchedule @C130409
  Scenario Outline: SC-WWL-SH-13_Copy the schedule of given day to another day in the app and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day 2> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 07:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    When The below schedule of Warm White Light is set for <Day 1> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 08:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    When The schedule is copied to <Day 2> from <Day 1> on the Client for Active light
    Then Verify if the Warm White Light Schedule is set

    Examples:
      | Day 1   | Day 2   |
      | Today   | Tommorow  |

  @SC-TL-SH-14 @TuneableLightScheduleTest @LightScheduleTest @C142408
  Scenario Outline: SC-TL-SH-14_Set the given default 'four' event schedule for the given day and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 06:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | OFF        | 0                 |                  |
      | 16:00       | ON         | 100               | WARMEST WHITE    |
      | 21:30       | OFF        | 0                 |                  |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-15 @TuneableLightScheduleTest @LightScheduleTestt
  Scenario Outline: SC-TL-SH-15_Set the given customized 'four' event schedule for the given day and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 06:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | MID WHITE        |
      | 16:00       | ON         | 100               | COOLEST WHITE    |
      | 21:30       | ON         | 50                | WARM WHITE       |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-TL-SH-16 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-16_Set the given customized 'six' event schedule for the given day and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 06:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | MID WHITE        |
      | 16:00       | ON         | 100               | COOLEST WHITE    |
      | 18:30       | ON         | 50                | WARM WHITE       |
      | 20:00       | ON         | 100               | COOLEST WHITE    |
      | 22:30       | ON         | 50                | WARM WHITE       |

    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-TL-SH-17 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-17_Set the given customized 'two' event schedule for the given day and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 06:30       | ON         | 100               | WARMEST WHITE    |
      | 22:00       | ON         | 60                | MID WHITE        |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-18 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-18_Set the given 'four' event schedule with earliest possible event time for the given day of the week and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 00:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | MID WHITE        |
      | 16:00       | ON         | 100               | COOLEST WHITE    |
      | 21:30       | ON         | 50                | WARM WHITE       |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-19 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-19_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 00:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | MID WHITE        |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-20 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-20_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 12:00       | ON         | 100               | WARMEST WHITE    |
      | 14:00       | ON         | 30                | MID WHITE        |
      | 16:30       | ON         | 100               | COOLEST WHITE    |
      | 23:45       | ON         | 50                | WARM WHITE       |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-21 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-21_Set the given 'two' event schedule with latest possible event time for the given day of the week and verify the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone             |
      | 10:30       | ON         | 100               | WARMEST WHITE    |
      | 23:45       | ON         | 30                | MID WHITE        |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-22 @TuneableLightScheduleTest
  Scenario Outline: SC-TL-SH-22_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day> on the Client
      | Status     | Brightness Value  | Tone             |
      | ON         | 100               | WARMEST WHITE    |
      | ON         | 30                | MID WHITE        |
      | ON         | 100               | COOLEST WHITE    |
      | ON         | 50                | WARM WHITE       |
      | ON         | 30                | COOLEST WHITE    |
      | ON         | 10                | WARM WHITE       |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-23 @TuneableLightScheduleTest @LightScheduleTest @ResetSchedule @C142409
  Scenario Outline: SC-TL-SH-23_Reset event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Tuneable Light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone        |
      | 06:30       | ON         | 100                | MID WHITE   |
      | 08:30       | OFF        | 0                  |             |
      | 16:00       | ON         | 100                | MID WHITE   |
      | 21:30       | OFF        | 0                  |             |
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day     |
      | Monday  |

  @SC-TL-SH-24 @TuneableLightScheduleTest @LightScheduleTest @AddSchedule @C142411
  Scenario Outline: SC-TL-SH-24_Create a new time slot and verify if other slots are affected for Tuneable light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone        |
      | 06:30       | ON         | 100                | MID WHITE   |
      | 08:30       | OFF        | 0                  |             |
      | 16:00       | ON         | 100                | MID WHITE   |
      | 21:30       | OFF        | 0                  |             |
    Then Verify if the Tuneable Light Schedule is set
    When Add the below time slot for active light on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone        |
      | 09:30       | ON         | 100                | MID WHITE   |
    Then Verify if the Tuneable Light Schedule is set
    Examples:
      | Day     |
      | Friday  |

  @SC-TL-SH-25 @TuneableLightScheduleTest @LightScheduleTest @DelSchedule @C142411
   Scenario Outline: SC-TL-SH-25_Delete a 3rd event from today and 2nd event from next day and verify the same for Tuneable light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone        |
      | 06:30       | ON         | 100                | MID WHITE   |
      | 08:30       | OFF        | 0                  |             |
      | 16:00       | ON         | 100                | MID WHITE   |
      | 21:30       | OFF        | 0                  |             |
    Then Verify if the Tuneable Light Schedule is set
    When Delete a time slot for active light of <Start Time> for <Day> on the Client
    Then Verify if the Tuneable Light Schedule is set
    Examples:
      | Day           |Start Time|
      | Today         |16:00     |
      | Tommorow      |08:30     |

  @SC-TL-SH-26 @TuneableLightScheduleTest @LightScheduleTest @CopySchedule @C142409
  Scenario Outline: SC-TL-SH-26_Copy the schedule of given day to another day in the app and verify the same for Tuneable light
    Given The Hive Tuneable Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Tuneable Light is set for <Day 2> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 07:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    Then Verify if the Tuneable Light Schedule is set
    When The below schedule of Tuneable Light is set for <Day 1> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 08:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    Then Verify if the Tuneable Light Schedule is set
    When The schedule is copied to <Day 2> from <Day 1> on the Client for Active light
    Then Verify if the Tuneable Light Schedule is set

    Examples:
      | Day 1   | Day 2     |
      | Today   | Tommorow  |

  @SC-CL-SH-27 @ColourLightScheduleTest @LightScheduleTest @C159720
  Scenario Outline: SC-CL-SH-27_Set the given default 'four' event schedule for the given day and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | RED              |
      | 08:30       | OFF        | 0                 |                  |
      | 16:00       | ON         | 100               | RED              |
      | 21:30       | OFF        | 0                 |                  |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-28 @ColourLightScheduleTest @LightScheduleTestt
  Scenario Outline: SC-CL-SH-28_Set the given customized 'four' event schedule for the given day and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | GREEN            |
      | 16:00       | ON         | 100               | BLUE             |
      | 21:30       | ON         | 50                | RED ORANGE       |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day    |
      | Monday |

  @SC-CL-SH-29 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-29_Set the given customized 'six' event schedule for the given day and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | MID WHITE        |
      | 08:30       | ON         | 30                | COOLEST WHITE    |
      | 16:00       | ON         | 100               | MAGENTA          |
      | 18:30       | ON         | 50                | CYAN BLUE        |
      | 20:00       | ON         | 100               | YELLOW           |
      | 22:30       | ON         | 50                | RED              |

    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day    |
      | Monday |

 @SC-CL-SH-30 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-30_Set the given customized 'two' event schedule for the given day and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | PINK             |
      | 22:00       | ON         | 60                | GREEN CYAN       |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-31 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-31_Set the given 'four' event schedule with earliest possible event time for the given day of the week and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 00:30       | ON         | 100               | WARMEST WHITE    |
      | 08:30       | ON         | 30                | RED              |
      | 16:00       | ON         | 100               | MAGENTA          |
      | 21:30       | ON         | 50                | YELLOW GREEN     |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-32 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-32_Set the given 'two' event schedule with earliest possible event time for the given day of the week and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 00:30       | ON         | 100               | YELLOW GREEN     |
      | 08:30       | ON         | 30                | RED ORANGE       |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-33 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-33_Set the given 'four' event schedule with latest possible event time for the given day of the week and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour |
      | 12:00       | ON         | 60                | MID WHITE     |
      | 14:00       | ON         | 5                 | RED           |
      | 16:30       | ON         | 70                | GREEN         |
      | 23:45       | ON         | 40                | WARM WHITE    |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-34 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-34_Set the given 'two' event schedule with latest possible event time for the given day of the week and verify the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 10:30       | ON         | 100               | MAGENTA PINK     |
      | 23:45       | ON         | 30                | PINK RED         |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-CL-SH-35 @ColourLightScheduleTest
  Scenario Outline: SC-CL-SH-35_Set the given 'six' event schedule with 15 minutes time difference between events for the given day of the week and validate the same for Colour Light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day> on the Client
      | Status     | Brightness Value  | Tone / Colour    |
      | ON         | 100               | WARMEST WHITE    |
      | ON         | 30                | RED              |
      | ON         | 100               | GREEN            |
      | ON         | 50                | WARM WHITE       |
      | ON         | 30                | PINK             |
      | ON         | 10                | CYAN             |
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day   |
      | Today |

  @SC-TL-SH-24 @ColourLightScheduleTest @LightScheduleTest @AddSchedule @C159723 @C159721
  Scenario Outline: SC-TL-SH-24_Create a new time slot and verify if other slots are affected for Colour light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone / Colour   |
      | 06:30       | ON         | 100                | MID WHITE       |
      | 08:30       | OFF        | 0                  |                 |
      | 16:00       | ON         | 100                | GREEN           |
      | 21:30       | OFF        | 0                  |                 |
    Then Verify if the Colour Light Schedule is set
    When Add the below time slot for active light on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone / Colour      |
      | 09:30       | ON         | 100                | MID WHITE          |
    Then Verify if the Colour Light Schedule is set
    Examples:
      | Day     |
      | Friday  |

  @SC-TL-SH-25 @ColourLightScheduleTest @LightScheduleTest @DelSchedule @C159723
   Scenario Outline: SC-TL-SH-25_Delete a 3rd event from today and 2nd event from next day and verify the same for Colour light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule is reset for active lights on <Day> on the Client
      | Start Time  | Status     | Brightness Value   | Tone / Colour        |
      | 06:30       | ON         | 100                | MAGENTA PINK         |
      | 08:30       | OFF        | 0                  |                      |
      | 16:00       | ON         | 100                | RED ORANGE           |
      | 21:30       | OFF        | 0                  |                      |
    Then Verify if the Colour Light Schedule is set
    When Delete a time slot for active light of <Start Time> for <Day> on the Client
    Then Verify if the Colour Light Schedule is set
    Examples:
      | Day           |Start Time|
      | Today         |16:00     |
      | Tommorow      |08:30     |

  @SC-TL-SH-26 @ColourLightScheduleTest @LightScheduleTest @CopySchedule @C159721
  Scenario Outline: SC-TL-SH-26_Copy the schedule of given day to another day in the app and verify the same for Colour light
    Given The Hive Colour Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Colour Light is set for <Day 2> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | YELLOW GREEN     |
      | 07:30       | OFF        | 0                 |                  |
      | 16:00       | ON         | 100               | RED              |
      | 21:30       | OFF        | 0                 |                  |
    Then Verify if the Colour Light Schedule is set
    When The below schedule of Colour Light is set for <Day 1> on the Client
      | Start Time  | Status     | Brightness Value  | Tone / Colour    |
      | 06:30       | ON         | 100               | GREEN            |
      | 08:30       | OFF        | 0                 |                  |
      | 16:00       | ON         | 100               | YELLOW           |
      | 21:30       | OFF        | 0                 |                  |
    Then Verify if the Colour Light Schedule is set
    When The schedule is copied to <Day 2> from <Day 1> on the Client for Active light
    Then Verify if the Colour Light Schedule is set

    Examples:
      | Day 1   | Day 2     |
      | Today   | Tommorow  |