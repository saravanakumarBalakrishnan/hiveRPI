# Created by anuj.kumar at 10/07/2017

  #Validation for Luminousity
Feature: Mimic
  # Vaidate the device behavior on applying mimic

  #Lets suppose FuzzyStartTime is FST and end time is FET
  ############################################
  #Main Validation Points

  #Lights turned OFF as Mimic activated (scenarios - prev status ON and OFF and modes)

  #Single Light
  #Light Turning on at X ( FST+0,FST+30)
  #Turning off at Y ( FET-30, FET)

  #Mulitple Lights
  #First light (lets say A) truning on at X where X is FST+0,FST+30
  #All the other lights turn on in X, X+15
  #First light turn off at Y where Y is FET-30,FET , A or any ?
  #All the other lights will be turn off in Y,Y+15

  #Lights will be off until next day FST
  #There is only a single occurance of ON->OFF for a light between for Single FST and FET, for multiple FST and FET+15
  ############################################
  #other validations

  #Fallback behavior after mimic is stopped
  #Offline behavior
  #Actions working as expected
  #Mimic On-boarding
  #Entitlements
  #Various Time periods
  #Light Combinations and selections
  #Light Features Brightness, tune and Color

  @Mimic @SC-MI-AL-SC01 @C295587 @295570
  Scenario Outline: SC-MI-AL-SC01_Verify Mimic behavior is set for all the Active lights
    Given Active lights are paired with Hive
    When The mimic is set between <startTime> and <endTime> for Random lights
    Then The mimic behavior is seen for the enabled lights

    Examples:
    |startTime    |endTime    |
    |16:00        |19:00      |


 @Mimic @SC-MI-AL-SC02 @C295588
  Scenario Outline: SC-MI-AL-SC02_Validate Mimic behavior for all the Active lights
    Given Active lights are paired with Hive
    When The mimic is set between <startTime> and <endTime> for Random lights
    Then The mimic behavior is seen for the enabled lights over <validationMinutes> minutes

    Examples:
    |startTime    |endTime      |validationMinutes  |
    |13:30        |15:00        |1200               |


  @Mimic @SC-MI-AL-SC03 @295589 @295571
  Scenario Outline: SC-MI-AL-SC03_Validate Mimic behavior for all the Active lights when set points are set with minimum duration for Random lights
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And The mimic is set for Random lights
    Then The mimic behavior is seen for the enabled lights over <validationMinutes> minutes

    Examples:

      |validationMinutes  |
      |300                |

  @Mimic @SC-MI-AL-SC04 @295590
  Scenario Outline: SC-MI-AL-SC04_Validate Mimic behavior for all the Active lights when set points are set with minimum duration for all the lights
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And The mimic is set for All lights
    Then The mimic behavior is seen for the enabled lights over <validationMinutes> minutes

    Examples:

      |validationMinutes  |
      |300                |

  @Mimic @SC-MI-AL-SC05 @295591 @C295578 @C295583 @C295584 @C295585
  Scenario: SC-MI-AL-SC05_Validate Mimic override behavior when mimic is started before the set points
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And  Mimic starts before the set points for Random lights
    Then The mimic behavior is seen for the enabled lights


  @Mimic @SC-MI-AL-SC06 @295592 @C295582
  Scenario: SC-MI-AL-SC06_Validate Mimic override behavior when mimic is started before at the mid of 1st set point
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And  Mimic starts Mid of 1st of the set points for Random lights
    Then The mimic behavior is seen for the enabled lights

  @Mimic @SC-MI-AL-SC07 @295593
  Scenario: SC-MI-AL-SC07_Validate Mimic override behavior when mimic is started between set points
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And  Mimic starts Between set points for Random lights
    Then The mimic behavior is seen for the enabled lights

  @Mimic @SC-MI-AL-SC08 @295594
  Scenario: SC-MI-AL-SC08_Validate Mimic override behavior when mimic is started after the 2nd set point
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And  Mimic starts just after 2nd of the set points for Random lights
    Then The mimic behavior is seen for the enabled lights


  @Mimic @SC-MI-AL-SC09 @295595
  Scenario: SC-MI-AL-SC09_Validate Mimic override behavior when mimic is started before the set points for all the lights
    Given Active lights are paired with Hive
    When Delete Fake Occupancy node
    And  A random behavior is set for lights
    And  Mimic starts Before the set points for All lights
    Then The mimic behavior is seen for the enabled lights

 @Mimic @SC-MI-AL-SC10
  Scenario Outline: SC-MM-UP Screen_Validate copy text on different screens with different languages for subscriber user
  # Pre-requisites : Step 1 : Change device Language to respective language before execution
  # Screens are Upsell splash screen,Light control screen,Onboarding splash screen,Onboarding select lights screen,Onboarding select times screen,Onboarding All done screen,Active Mimic mode popup,Mimic active screen,Stop Mimic mode popup,Add to mimic popups,
  # "Set times" inputs popup
  # Languages can be UK_English, US_English, Canadian_English, US_Spanish, Canadian_French, Italian, Irish
  # Provide "subscribed" if need to add hive live subscription and provide "not subscribed" if hive live needs to be removed ( Same applies for LEAK ALERT PLAN )
  Given The device and user language is set to UK_English
  And The <ActiveLightName> is paired with the hub
  And The user is not subscribed to HIVE LIVE
  When I am on the screen <Screen Name>
  Then The text is correct in English

  Examples:
  |ActiveLightName  |Screen Name                    |
  |Warm white light |Upsell splash screen           |
  #|Warm white light |Light control screen           |
  #|Warm white light |Onboarding splash screen       |
  #|Warm white light |Onboarding select lights screen|
  #|Warm white light |Onboarding select times screen |
  #|Warm white light |Onboarding All done screen     |
  #|Warm white light |Active Mimic mode popup        |
  #|Warm white light |Mimic active screen            |
  #|Warm white light |Stop Mimic mode popup          |
  #|Warm white light |Add to mimic popups            |
  #|Warm white light |"Set times" inputs popup       |

@Mimic @SC-MI-AL-SC11
  Scenario Outline: SC-MM-UP Screen_Validate copy text on different screens with different languages for non subscriber user
  # Languages can be UK_English, US_English, Canadian_English, US_Spanish, Canadian_French, Italian, Irish
  # Provide "subscribed" if need to add hive live subscription and provide "not subscribed" if hive live needs to be removed ( Same applies for LEAK ALERT PLAN )
  Given The device and user language is set to UK_English
  And The <ActiveLightName> is paired with the hub
  And The user is subscribed to HIVE LIVE
  When I am on the screen <Screen Name>
  Then The text is correct in US Spanish

  Examples:
  |ActiveLightName  |Screen Name                    |
  |Warm white light |Light control screen           |
  #|Warm white light |Onboarding splash screen       |
  #|Warm white light |Onboarding select lights screen|
  #|Warm white light |Onboarding select times screen |
  #|Warm white light |Onboarding All done screen     |
  #|Warm white light |Active Mimic mode popup        |
  #|Warm white light |Mimic active screen            |
  #|Warm white light |Stop Mimic mode popup          |
  #|Warm white light |Add to mimic popups            |
  #|Warm white light |"Set times" inputs popup       |
