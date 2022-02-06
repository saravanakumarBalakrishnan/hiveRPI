#@authors:
#iOS        - Meenakshi
#Android    - Vinod Pasalkar
#Web        - Krishna

Feature: Validate the various Brightness levels, Tone and Mode alongwith the schedule of Active Lights

 @C265033 @WarmWhiteLight  @Android_Regression @Android_SmokeTest @iOS_Regression
 Scenario Outline: SC-AL-MBC-01_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5% 
	Then automatically validate the mode and brightness as MANUAL and 5% 
    When The mode and brightness is automatically changed to MANUAL and 30% 
	Then automatically validate the mode and brightness as MANUAL and 30%

    Examples:
    |Active Light       |
    |Warm White Light   |

 @C265039 @WarmWhiteLight @Android_Regression @iOS_Regression
 Scenario Outline: SC-AL-MBC-02_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and brightness is automatically changed to SCHEDULE and 80% 
	Then automatically validate the mode and brightness as SCHEDULE and 80% 
    When The mode and brightness is automatically changed to SCHEDULE and 90% 
	Then automatically validate the mode and brightness as SCHEDULE and 90% 

    Examples:
    |Active Light       |
	|Warm White Light	|

  @C142415 @iOS_Regression
 Scenario Outline: SC-AL-MBC-04_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to SCHEDULE and 10%
	Then automatically validate the mode and brightness as SCHEDULE and 10%
    When The mode and brightness is automatically changed to SCHEDULE and 90%
	Then automatically validate the mode and brightness as SCHEDULE and 90%

    Examples:
    |Active Light       |
	|Tuneable Light     |

  @C142410 @C142431 @iOS_Regression
 Scenario Outline: SC-AL-MBC-03_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5%
	Then automatically validate the mode and brightness as MANUAL and 5%
    When The mode and brightness is automatically changed to MANUAL and 70%
	Then automatically validate the mode and brightness as MANUAL and 70%
    When The mode and brightness is automatically changed to MANUAL and 100%
	Then automatically validate the mode and brightness as MANUAL and 100%

    Examples:
    |Active Light       |
    |Tuneable Light     |


  @C159722 @iOS_Regression
 Scenario Outline: SC-AL-MBC-05_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5%
	Then automatically validate the mode and brightness as MANUAL and 5%
    When The mode and brightness is automatically changed to MANUAL and 70%
	Then automatically validate the mode and brightness as MANUAL and 70%
    When The mode and brightness is automatically changed to MANUAL and 100%
	Then automatically validate the mode and brightness as MANUAL and 100%

    Examples:
    |Active Light       |
    |Colour Light       |

  @C159722 @iOS_Regression
 Scenario Outline: SC-AL-MBC-06_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to SCHEDULE and 10%
	Then automatically validate the mode and brightness as SCHEDULE and 10%
    When The mode and brightness is automatically changed to SCHEDULE and 90%
	Then automatically validate the mode and brightness as SCHEDULE and 90%

    Examples:
    |Active Light       |
	|Colour Light       |

    @C130408 @iOS_Regression
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

   @C130415 @iOS_Regression
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

   @C130415 @iOS_Regression
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

     @C130409 @iOS_Regression
  Scenario Outline: SC-WWL-SH-13_Copy the schedule of given day to another day in the app and verify the same for Warm White Light
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
    When The below schedule of Warm White Light is set for <Day 2> on the Client
      | Start Time  | Status     | Brightness Value  |
      | 06:30       | ON         | 100               |
      | 07:30       | OFF        | 0                 |
      | 16:00       | ON         | 100               |
      | 21:30       | OFF        | 0                 |
    Given The Hive Warm White Light is paired with Hive Hub and setup for API Validation
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


  @C142408 @iOS_Regression
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

  @C142409 @iOS_Regression
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


  @C159720 @iOS_Regression
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


  @C265031 @WarmWhiteLight @Android_Regression @Android_SmokeTest
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

  @C265107 @WarmWhiteLight @Android_Regression
  Scenario Outline: SC-WWL-SH-03_Set the given customized 'six' event schedule for the given day and verify the same for Warm White Light
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

  @C265032 @WarmWhiteLight  @Android_Regression
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