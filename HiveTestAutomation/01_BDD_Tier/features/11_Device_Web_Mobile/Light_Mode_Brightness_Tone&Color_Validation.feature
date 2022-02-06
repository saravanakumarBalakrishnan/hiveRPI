#@authors:
#iOS        - Meenakshi
#Android    - Vinod Pasalkar
#Web        - Krishna

Feature: Validate the various Brightness levels, Tone and Mode of Active Lights

 @SC-AL-MBC-01 @WarmWhiteLight @ManualModeAllBrightnessTest @ActiveLightTest @C130414
 Scenario Outline: SC-AL-MBC-01_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5% 
	Then automatically validate the mode and brightness as MANUAL and 5% 
    When The mode and brightness is automatically changed to MANUAL and 30% 
	Then automatically validate the mode and brightness as MANUAL and 30% 
    When The mode and brightness is automatically changed to MANUAL and 50% 
	Then automatically validate the mode and brightness as MANUAL and 50% 
    When The mode and brightness is automatically changed to MANUAL and 70% 
	Then automatically validate the mode and brightness as MANUAL and 70% 
    When The mode and brightness is automatically changed to MANUAL and 100% 
	Then automatically validate the mode and brightness as MANUAL and 100% 

    Examples:
    |Active Light       |
    |Warm White Light   |

 @SC-AL-MBC-02 @WarmWhiteLight @ScheduleModeAllBrightnessTest @ActiveLightTest
 Scenario Outline: SC-AL-MBC-02_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to SCHEDULE and 10%
	Then automatically validate the mode and brightness as SCHEDULE and 10%
    When The mode and brightness is automatically changed to SCHEDULE and 20% 
	Then automatically validate the mode and brightness as SCHEDULE and 20% 
    When The mode and brightness is automatically changed to SCHEDULE and 40% 
	Then automatically validate the mode and brightness as SCHEDULE and 40% 
    When The mode and brightness is automatically changed to SCHEDULE and 60%
	Then automatically validate the mode and brightness as SCHEDULE and 60%
    When The mode and brightness is automatically changed to SCHEDULE and 80% 
	Then automatically validate the mode and brightness as SCHEDULE and 80% 
    When The mode and brightness is automatically changed to SCHEDULE and 90% 
	Then automatically validate the mode and brightness as SCHEDULE and 90% 

    Examples:
    |Active Light       |
	|Warm White Light	|

  @SC-AL-MBC-03 @TuneableLight @ManualModeAllBrightnessTest @ActiveLightTest @C142410 @C142431
  Scenario Outline: SC-AL-MBC-03_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5% 
	Then automatically validate the mode and brightness as MANUAL and 5% 
    When The mode and brightness is automatically changed to MANUAL and 30% 
	Then automatically validate the mode and brightness as MANUAL and 30% 
    When The mode and brightness is automatically changed to MANUAL and 50% 
	Then automatically validate the mode and brightness as MANUAL and 50% 
    When The mode and brightness is automatically changed to MANUAL and 70% 
	Then automatically validate the mode and brightness as MANUAL and 70% 
    When The mode and brightness is automatically changed to MANUAL and 100% 
	Then automatically validate the mode and brightness as MANUAL and 100% 

    Examples:
    |Active Light       |
    |Tuneable Light     |

  @SC-AL-MBC-04 @TuneableLight @ScheduleModeAllBrightnessTest @ActiveLightTest @C142415
  Scenario Outline: SC-AL-MBC-04_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to SCHEDULE and 10% 
	Then automatically validate the mode and brightness as SCHEDULE and 10% 
    When The mode and brightness is automatically changed to SCHEDULE and 20% 
	Then automatically validate the mode and brightness as SCHEDULE and 20% 
    When The mode and brightness is automatically changed to SCHEDULE and 40% 
	Then automatically validate the mode and brightness as SCHEDULE and 40% 
    When The mode and brightness is automatically changed to SCHEDULE and 60% 
	Then automatically validate the mode and brightness as SCHEDULE and 60% 
    When The mode and brightness is automatically changed to SCHEDULE and 80% 
	Then automatically validate the mode and brightness as SCHEDULE and 80% 
    When The mode and brightness is automatically changed to SCHEDULE and 90% 
	Then automatically validate the mode and brightness as SCHEDULE and 90% 

    Examples:
    |Active Light       |
	|Tuneable Light     |

 @SC-AL-MBC-05 @ColourLight @ManualModeAllBrightnessTest @ActiveLightTest @C159722
 Scenario Outline: SC-AL-MBC-05_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to MANUAL and 5% 
	Then automatically validate the mode and brightness as MANUAL and 5% 
    When The mode and brightness is automatically changed to MANUAL and 30% 
	Then automatically validate the mode and brightness as MANUAL and 30% 
    When The mode and brightness is automatically changed to MANUAL and 50% 
	Then automatically validate the mode and brightness as MANUAL and 50% 
    When The mode and brightness is automatically changed to MANUAL and 70% 
	Then automatically validate the mode and brightness as MANUAL and 70% 
    When The mode and brightness is automatically changed to MANUAL and 100% 
	Then automatically validate the mode and brightness as MANUAL and 100% 

    Examples:
    |Active Light       |
    |Colour Light       |

 @SC-AL-MBC-06 @ColourLight @ScheduleModeAllBrightnessTest @ActiveLightTest @C159722
 Scenario Outline: SC-AL-MBC-06_Validate the brightness of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and brightness is automatically changed to SCHEDULE and 10% 
	Then automatically validate the mode and brightness as SCHEDULE and 10% 
    When The mode and brightness is automatically changed to SCHEDULE and 20% 
	Then automatically validate the mode and brightness as SCHEDULE and 20% 
    When The mode and brightness is automatically changed to SCHEDULE and 40% 
	Then automatically validate the mode and brightness as SCHEDULE and 40% 
    When The mode and brightness is automatically changed to SCHEDULE and 60% 
	Then automatically validate the mode and brightness as SCHEDULE and 60% 
    When The mode and brightness is automatically changed to SCHEDULE and 80% 
	Then automatically validate the mode and brightness as SCHEDULE and 80% 
    When The mode and brightness is automatically changed to SCHEDULE and 90% 
	Then automatically validate the mode and brightness as SCHEDULE and 90% 

    Examples:
    |Active Light       |
	|Colour Light       |

 @SC-AL-MSC-01 @WarmWhiteLight @ModeOnOffChangeTest @ActiveLightTest @C130416
 Scenario Outline: SC-AL-MSC-01_Validate the mode change of Active light
 	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and status is automatically changed to MANUAL and ON 
    Then automatically validate the mode and status as MANUAL and ON 
    When The mode and status is automatically changed to MANUAL and OFF 
    Then automatically validate the mode and status as MANUAL and OFF 
    When The mode and status is automatically changed to SCHEDULE and ON 
    Then automatically validate the mode and status as SCHEDULE and ON 
    When The mode and status is automatically changed to SCHEDULE and OFF 
    Then automatically validate the mode and status as SCHEDULE and OFF 

   Examples:
	 |Active Light     |
	 |Warm White Light |

 @SC-AL-MSC-02 @TuneableLight @ModeOnOffChangeTest @ActiveLightTest @C142412
 Scenario Outline: SC-AL-MSC-02_Validate the mode change of Active light
 	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and status is automatically changed to MANUAL and ON 
    Then automatically validate the mode and status as MANUAL and ON 
    When The mode and status is automatically changed to MANUAL and OFF 
    Then automatically validate the mode and status as MANUAL and OFF 
    When The mode and status is automatically changed to SCHEDULE and ON 
    Then automatically validate the mode and status as SCHEDULE and ON 
    When The mode and status is automatically changed to SCHEDULE and OFF 
    Then automatically validate the mode and status as SCHEDULE and OFF 

   Examples:
	 |Active Light     |
	 |Tuneable Light   |

 @SC-AL-MSC-03 @ColourLight @ModeOnOffChangeTest @ActiveLightTest @C159724
 Scenario Outline: SC-AL-MSC-03_Validate the mode change of Active light
 	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and status is automatically changed to MANUAL and ON 
    Then automatically validate the mode and status as MANUAL and ON 
    When The mode and status is automatically changed to MANUAL and OFF 
    Then automatically validate the mode and status as MANUAL and OFF 
    When The mode and status is automatically changed to SCHEDULE and ON 
    Then automatically validate the mode and status as SCHEDULE and ON 
    When The mode and status is automatically changed to SCHEDULE and OFF 
    Then automatically validate the mode and status as SCHEDULE and OFF 

   Examples:
	 |Active Light     |
	 |Colour Light     |

 @SC-AL-MTC-01 @TuneableLight @ActiveLightTest @C142459
 Scenario Outline: SC-AL-MTC-01_Validate the tone of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and tone is automatically changed to MANUAL and WARMEST WHITE 
	Then automatically validate the mode and tone as MANUAL and WARMEST WHITE 
    When The mode and tone is automatically changed to MANUAL and WARM WHITE 
	Then automatically validate the mode and tone as MANUAL and WARM WHITE 
    When The mode and tone is automatically changed to MANUAL and MID WHITE 
	Then automatically validate the mode and tone as MANUAL and MID WHITE 
    When The mode and tone is automatically changed to MANUAL and COOL WHITE 
	Then automatically validate the mode and tone as MANUAL and COOL WHITE 
    When The mode and tone is automatically changed to MANUAL and COOLEST WHITE 
	Then automatically validate the mode and tone as MANUAL and COOLEST WHITE 

   Examples:
	 |Active Light     |
	 |Tuneable Light   |


 @SC-AL-MTC-02 @TuneableLight @ActiveLightTest @C142459
 Scenario Outline: SC-AL-MTC-02_Validate the tone of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and tone is automatically changed to SCHEDULE and WARMEST WHITE 
	Then automatically validate the mode and tone as SCHEDULE and WARMEST WHITE 
    When The mode and tone is automatically changed to SCHEDULE and WARM WHITE 
	Then automatically validate the mode and tone as SCHEDULE and WARM WHITE 
    When The mode and tone is automatically changed to SCHEDULE and MID WHITE 
	Then automatically validate the mode and tone as SCHEDULE and MID WHITE 
    When The mode and tone is automatically changed to SCHEDULE and COOL WHITE 
	Then automatically validate the mode and tone as SCHEDULE and COOL WHITE 
    When The mode and tone is automatically changed to SCHEDULE and COOLEST WHITE 
	Then automatically validate the mode and tone as SCHEDULE and COOLEST WHITE 

   Examples:
	 |Active Light     |
	 |Tuneable Light   |

 @SC-AL-MTC-03 @ColourLight @ActiveLightTest @C159724 @C159727
 Scenario Outline: SC-AL-MTC-03_Validate the tone of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and tone is automatically changed to MANUAL and WARMEST WHITE 
	Then automatically validate the mode and tone as MANUAL and WARMEST WHITE 
    When The mode and tone is automatically changed to MANUAL and WARM WHITE 
	Then automatically validate the mode and tone as MANUAL and WARM WHITE 
    When The mode and tone is automatically changed to MANUAL and MID WHITE 
	Then automatically validate the mode and tone as MANUAL and MID WHITE 
    When The mode and tone is automatically changed to MANUAL and COOL WHITE 
	Then automatically validate the mode and tone as MANUAL and COOL WHITE 
    When The mode and tone is automatically changed to MANUAL and COOLEST WHITE 
	Then automatically validate the mode and tone as MANUAL and COOLEST WHITE

   Examples:
	 |Active Light     |
	 |Colour Light     |


 @SC-AL-MTC-04 @ColourLight @ActiveLightTest @C159727
 Scenario Outline: SC-AL-MTC-04_Validate the tone of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
    When The mode and tone is automatically changed to SCHEDULE and WARMEST WHITE 
	Then automatically validate the mode and tone as SCHEDULE and WARMEST WHITE 
    When The mode and tone is automatically changed to SCHEDULE and WARM WHITE 
	Then automatically validate the mode and tone as SCHEDULE and WARM WHITE 
    When The mode and tone is automatically changed to SCHEDULE and MID WHITE 
	Then automatically validate the mode and tone as SCHEDULE and MID WHITE 
    When The mode and tone is automatically changed to SCHEDULE and COOL WHITE 
	Then automatically validate the mode and tone as SCHEDULE and COOL WHITE 
    When The mode and tone is automatically changed to SCHEDULE and COOLEST WHITE 
	Then automatically validate the mode and tone as SCHEDULE and COOLEST WHITE 

   Examples:
	 |Active Light     |
	 |Colour Light     |

 @SC-AL-MCC-01 @ColourLight @ActiveLightTest
 Scenario Outline: SC-AL-MCC-01_Validate the colour of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and colour is automatically changed to MANUAL and RED 
	Then automatically validate the mode and colour as MANUAL and RED 
    When The mode and colour is automatically changed to MANUAL and ORANGE 
	Then automatically validate the mode and colour as MANUAL and ORANGE 
    When The mode and colour is automatically changed to MANUAL and YELLOW 
	Then automatically validate the mode and colour as MANUAL and YELLOW 
    When The mode and colour is automatically changed to MANUAL and MAGENTA 
	Then automatically validate the mode and colour as MANUAL and MAGENTA 
    When The mode and colour is automatically changed to MANUAL and GREEN 
	Then automatically validate the mode and colour as MANUAL and GREEN 

   Examples:
	 |Active Light     |
	 |Colour Light     |

 @SC-AL-MCC-02 @ColourLight @ActiveLightTest
 Scenario Outline: SC-AL-MCC-02_Validate the colour of Active light
	Given The Hive <Active Light> is paired with Hive Hub and setup for API Validation
	When The mode and colour is automatically changed to SCHEDULE and PINK 
	Then automatically validate the mode and colour as SCHEDULE and PINK 
    When The mode and colour is automatically changed to SCHEDULE and GREEN CYAN 
	Then automatically validate the mode and colour as SCHEDULE and GREEN CYAN 
    When The mode and colour is automatically changed to SCHEDULE and YELLOW GREEN 
	Then automatically validate the mode and colour as SCHEDULE and YELLOW GREEN 
    When The mode and colour is automatically changed to SCHEDULE and BLUE MAGENTA 
	Then automatically validate the mode and colour as SCHEDULE and BLUE MAGENTA 
    When The mode and colour is automatically changed to SCHEDULE and PINK RED 
	Then automatically validate the mode and colour as SCHEDULE and PINK RED 

   Examples:
	 |Active Light     |
	 |Colour Light     |