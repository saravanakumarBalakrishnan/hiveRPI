# Created by kingston.samselwyn on 21/03/2017
Feature: Consists of scenario that validates the thermostat operations using button press, hold and spinning dial

  @SC-TH-UI01 @UITest
  Scenario Outline: SC-TH-UI01_Validate the setting mode on thermostat
    Given The telegesis is paired with given heating devices
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
     #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
     #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
     #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
     #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    #SCHEDULE OVERRIDE MODE
    When the heat OVERRIDE is activated using button on the <Language> <DeviceType> as <AutoOverRideTemperature>
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    And validate current Heat mode as OVERRIDE on the <DeviceType> screen in <Language>
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #SCHEDULE OVERRIDE MODE
    When the heat OVERRIDE is activated using button on the <Language> <DeviceType> as <AutoOverRideTemperature>
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    And validate current Heat mode as OVERRIDE on the <DeviceType> screen in <Language>
    #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #SCHEDULE OVERRIDE MODE
    When the heat OVERRIDE is activated using button on the <Language> <DeviceType> as <AutoOverRideTemperature>
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    And validate current Heat mode as OVERRIDE on the <DeviceType> screen in <Language>
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    #SCHEDULE OVERRIDE MODE
    When the heat OVERRIDE is activated using button on the <Language> <DeviceType> as <AutoOverRideTemperature>
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    And validate current Heat mode as OVERRIDE on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    #SCHEDULE OVERRIDE MODE
    When the heat OVERRIDE is activated using button on the <Language> <DeviceType> as <AutoOverRideTemperature>
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    And validate current Heat mode as OVERRIDE on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature

    Examples:
      | DeviceType | Language | AutoOverRideTemperature |
      | SLT3b      | English  | 15                      |

  @SC-TH-UI02 @UITest
  Scenario Outline: SC-TH-UI02_Validate the setting boost on thermostat in Italian
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | Italian  |

  @SC-TH-UI03 @UITestWater
  Scenario Outline: SC-TH-UI03_Validate the setting water boost on thermostat
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UI04Debug @UITestChildLock
  Scenario Outline: SC-TH-UI04Debug_Put stat in Child Lock
    Given The telegesis is paired with given heating devices
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>


    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UI04 @UITestChildLock
  Scenario Outline: SC-TH-UI04_Put stat in Child Lock
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the Child Lock is activated and deactivated using button flow on the <Language> <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>


    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UI05  @UITestHeatScheduleStartOver
  Scenario Outline: SC-TH-UI05_Validate the setting Heat Schedule with StartOver on thermostat
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the Heat Schedule is set with <EnergyType> with StartOver on the <DeviceType> screen in <Language>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature

    Examples:
      | DeviceType | Language | EnergyType       |
      | SLT3b      | English  | Energy Efficient |

  @SC-TH-UI05-01  @UITestHeatScheduleStartOver
  Scenario Outline: SC-TH-UI05-01_Validate the setting Heat Schedule with StartOver on thermostat
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the Heat Schedule is set with <EnergyType> with StartOver on the <DeviceType> screen in <Language>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature

    Examples:
      | DeviceType | Language | EnergyType |
      | SLT3b      | English  | Comfort    |

  @SC-TH-UI06  @UITestWaterScheduleStartOver
  Scenario Outline: SC-TH-UI06_Validate the setting Water Schedule with StartOver on thermostat
    Given The Hive product is paired and setup for Dual Channel with Zigbee Validation
    When the water OFF is activated using button on the <Language> <DeviceType>
    When the Water Schedule is set with default-schedule with StartOver on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UI13 @UITestFrostTemperature
  Scenario Outline: SC-TH-UI13_Validate the setting of Frost Temperature
    Given The telegesis is paired with given heating devices
    When the Frost temperature is set to 8 on the <DeviceType> screen in <Language>


    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UI14 @UITestFrostTemperature
  Scenario Outline: SC-TH-UI14_Validate the setting of Frost Temperature on Platform with Stat setting it
    Given The telegesis is paired with given heating devices
    When The Frost temperature is set to 8 min on the <DeviceType>
    Then Validate on Platform

    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI15 @UITestholiday
  Scenario Outline: SC-TH-UI15_Set and validate Vacation zone
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel FALSE on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel FALSE on the <DeviceType>

    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI16 @UITestholiday
  Scenario Outline: SC-TH-UI16_Set and validate Vacation zone with Boost Cancelled
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel FALSE on the <DeviceType>

    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI17  @UITestHeatManualOFF
  Scenario Outline: SC-TH-UI17_Validate the setting Heat OFF to manual to Off on thermostat
    Given The telegesis is paired with given heating device
    When the water OFF is activated using button on the <DeviceType>
    When the water is set to Manual on the <DeviceType>
    When the water OFF is activated using button on the <DeviceType>



    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI18  @UITestWaterManualOFF
  Scenario Outline: SC-TH-UI18_Validate the setting Water OFF to manual to Off  on thermostat
    Given The telegesis is paired with given heating device
    When the heat OFF is activated using button on the <DeviceType>
    When the heat is set to Manual on the <DeviceType>
    When the heat OFF is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI19  @UITestHeatManualBoost
  Scenario Outline: SC-TH-UI19_Validate the setting Heat OFF then manual and then boost on thermostat
    Given The telegesis is paired with given heating device
    When the water OFF is activated using button on the <DeviceType>
    When the water is set to Manual on the <DeviceType>
    When the water boost is activated using button on the <DeviceType>



    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI20  @UITestWaterManualBoost
  Scenario Outline: SC-TH-UI20_Validate the setting Water OFF  on thermostat
    Given The telegesis is paired with given heating device
    When the heat OFF is activated using button on the <DeviceType>
    When the heat is set to Manual on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI21  @UITestHeatBoostHoliday
  Scenario Outline: SC-TH-UI21_Validate the setting Heat OFF then boost and Holiday to validate boost should get cancelled on thermostat
    Given The telegesis is paired with given heating device
    When the water OFF is activated using button on the <DeviceType>
    When the water is set to Manual on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel TRUE on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI22  @UITestWaterBoostWithHoliday
  Scenario Outline: SC-TH-UI22_Validate the setting Water OFF then boost and Holiday to validate boost should get cancelled on thermostat
    Given The telegesis is paired with given heating device
    When the heat OFF is activated using button on the <DeviceType>
    When the heat is set to Manual on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel TRUE on the <DeviceType>

    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI23  @UITestHeatScheduleThenOff
  Scenario Outline: SC-TH-UI23_Validate the setting Heat Schedule then Off on thermostat
    Given The telegesis is paired with given heating device
    When the heat schedule is activated using button on the <DeviceType>
    When the heat OFF is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI24  @UITestwatertScheduleThenOff
  Scenario Outline: SC-TH-UI24_Validate the setting Water Schedule then Off on thermostat
    Given The telegesis is paired with given heating device
    When the water schedule is activated using button on the <DeviceType>
    When the water OFF is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI25  @UITestHeatScheduleThenboost
  Scenario Outline: SC-TH-UI25_Validate the setting Heat Schedule then boost on thermostat
    Given The telegesis is paired with given heating device
    When the heat schedule is activated using button on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI26  @UITestWaterScheduleThenBoost
  Scenario Outline: SC-TH-UI26_Validate the setting Water Schedule then Boost on thermostat
    Given The telegesis is paired with given heating device
    When the water schedule is activated using button on the <DeviceType>
    When the heat boost is activated using button on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI27  @UITestHeatScheduleThenboost
  Scenario Outline: SC-TH-UI27_Validate the setting Heat Schedule then Holiday on thermostat
    Given The telegesis is paired with given heating device
    When the heat schedule is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel TRUE on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI28  @UITestWaterScheduleThenBoost
  Scenario Outline: SC-TH-UI28_Validate the setting Water Schedule then Holiday on thermostat
    Given The telegesis is paired with given heating device
    When the water schedule is activated using button on the <DeviceType>
    When The holiday set for Current day for 2 min for temperature 12 degrees and cancel TRUE on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI29  @UITestHeatScheduleThenManual
  Scenario Outline: SC-TH-UI27_Validate the setting Heat Schedule then Manual on thermostat
    Given The telegesis is paired with given heating device
    When the heat schedule is activated using button on the <DeviceType>
    When the heat is set to Manual on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI30  @UITestWaterScheduleThenManual
  Scenario Outline: SC-TH-UI28_Validate the setting Water Schedule then Manual on thermostat
    Given The telegesis is paired with given heating device
    When the water schedule is activated using button on the <DeviceType>
    When the water is set to Manual on the <DeviceType>


    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI31  @UITestHeatBoostThenSchedule
  Scenario Outline: SC-TH-UI27_Validate the setting Heat Boost then Schedule on thermostat
    Given The telegesis is paired with given heating device
    When the heat boost is activated using button on the <DeviceType>
    When the heat schedule is activated using button on the <DeviceType>




    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI32  @UITestWaterScheduleThenSchedule
  Scenario Outline: SC-TH-UI28_Validate the setting Water SBoost then Schedule on thermostat
    Given The telegesis is paired with given heating device
    When the heat boost is activated using button on the <DeviceType>
    When the water schedule is activated using button on the <DeviceType>
    Examples:
      | DeviceType |
      | SLT3b      |

  @SC-TH-UI33
  Scenario Outline: SC-TH-UI33_Boost cancellation by rebooting BM
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    When the <BM> is reboot via telegesis to change Heat mode to OFF with Target Temperature as 1.0 in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI34
  Scenario Outline: SC-TH-UI34_Boost cancellation by back button
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the heat boost is deactivated using button on the <Language> in <DeviceType> to Heat OFF mode when both boost is active
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER boost is deactivated using button on the <Language> in <DeviceType> to HOTWATER OFF mode when both boost is active
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI35
  Scenario Outline: SC-TH-UI35_Boost cancellation by back button
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    When the heat boost is deactivated using button on the <Language> in <DeviceType> to Heat OFF mode
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>


    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI36
  Scenario Outline: SC-TH-UI36_Boost cancellation by back button
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    When the HOTWATER boost is deactivated using button on the <Language> in <DeviceType> to HOTWATER OFF mode
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI37
  Scenario Outline: SC-TH-UI37_Boost cancellation by back button
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    When the heat boost is activated using button on the <Language> <DeviceType> for 6 hours
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    When the heat boost is deactivated using button on the <Language> in <DeviceType> to Heat OFF

    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI38
  Scenario Outline: SC-TH-UI38_Setting up a customized schedule for heat
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When the below heat schedule is set on the <DeviceType> screen in <Language> using startover
      | Day | Event1     | Event2    | Event3     | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Tue | 06:30,16.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,32.0 | 22:30,1.0 |
      | Wed | 00:30,17.0 | 04:30,1.0 | 10:45,17.0 | 13:00,1.0 |            |           |
      | Thu | 15:30,18.0 | 18:30,1.0 | 20:30,17.0 | 23:00,1.0 | 23:30,31.5 | 23:45,1.0 |
      | Fri | 06:30,19.0 | 08:30,1.0 |            |           |            |           |
      | Sat | 06:30,20.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,30.5 | 22:30,1.0 |
      | Sun | 12:30,14.0 | 15:30,1.0 | 19:15,17.0 | 20:00,1.0 | 22:30,31.0 | 23:30,1.0 |
    Then Verify if the Schedule is set for the whole week
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI39
  Scenario Outline: SC-TH-UI39_Setting up a customized schedule for hot water
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    When the below Hotwater schedule is set on the <DeviceType> screen in <Language> using startover
      | Day | Event1   | Event2    | Event3   | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Wed | 00:30,ON | 04:30,OFF | 10:45,ON | 13:00,OFF |          |           |
      | Thu | 15:30,ON | 18:30,OFF | 20:30,ON | 23:00,OFF | 23:30,ON | 23:45,OFF |
      | Fri | 06:30,ON | 08:30,OFF |          |           |          |           |
      | Sat | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Sun | 12:30,ON | 15:30,OFF | 19:15,ON | 20:00,OFF | 22:30,ON | 23:30,OFF |
    Then Verify if the Schedule is set for the whole week
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI40
  Scenario Outline: SC-TH-UI40_Setting up a customized schedule for heat
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And Verify if the below Schedule is set for the whole week
      | Day | Event1   | Event2    | Event3   | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Wed | 00:30,ON | 04:30,OFF | 10:45,ON | 13:00,OFF |          |           |
      | Thu | 15:30,ON | 18:30,OFF | 20:30,ON | 23:00,OFF | 23:30,ON | 23:45,OFF |
      | Fri | 06:30,ON | 08:30,OFF |          |           |          |           |
      | Sat | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Sun | 12:30,ON | 15:30,OFF | 19:15,ON | 20:00,OFF | 22:30,ON | 23:30,OFF |
    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI41
  Scenario Outline: SC-TH-UI41_Setting up a customized schedule for heat Energy Efficient Mode
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When the Heat Schedule is set with <EnergyType> with StartOver on the <DeviceType> screen in <Language>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And Verify if the below Schedule is set for the whole week
      | Day | Event1     | Event2    | Event3    | Event4    | Event5     | Event6    |
      | Mon | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Tue | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Wed | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Thu | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Fri | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Sat | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Sun | 06:30,18.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |

    Examples:
      | DeviceType | Language | EnergyType       |
      | SLT3b      | English  | Energy Efficient |

  @SC-TH-UI42
  Scenario Outline: SC-TH-UI42_Setting up a customized schedule for heat Energy Efficient Mode
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When the Heat Schedule is set with <EnergyType> with StartOver on the <DeviceType> screen in <Language>
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And Verify if the below Schedule is set for the whole week
      | Day | Event1     | Event2    | Event3    | Event4    | Event5     | Event6    |
      | Mon | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Tue | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Wed | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Thu | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Fri | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Sat | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |
      | Sun | 06:30,20.0 | 08:30,1.0 | 12:00,1.0 | 14:00,1.0 | 16:30,20.0 | 22:00,1.0 |

    Examples:
      | DeviceType | Language | EnergyType |
      | SLT3b      | English  | Comfort    |

  @SC-TH-UI43
  Scenario Outline: SC-TH-UI43_Setting up a customized schedule for Hot Water
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    When the Water Schedule is set with default-schedule with StartOver on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    And Verify if the below Schedule is set for the whole week
      | Day | Event1   | Event2    | Event3    | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Wed | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Thu | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Fri | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Sat | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |
      | Sun | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:30,ON | 21:30,OFF |

    Examples:
      | DeviceType | Language | BM   |
      | SLT3b      | English  | SLR2 |

  @SC-TH-UI44
  Scenario Outline: SC-TH-UI44_Setting up a customized schedule for heat
    Given The telegesis is paired with given heating devices
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When the below heat schedule is set on the <DeviceType> screen in <Language> using edit
      | Day | Event1     | Event2    | Event3     | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Tue | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Wed | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Thu | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Fri | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Sat | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
      | Sun | 06:30,15.0 | 08:30,1.0 | 10:30,17.0 | 13:00,1.0 | 15:30,31.0 | 22:30,1.0 |
    Then Verify if the Schedule is set for the whole week
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |

  @SC-TH-UI45
  Scenario Outline: SC-TH-UI44_Setting up a customized schedule for hot water
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    When the below Hotwater schedule is set on the <DeviceType> screen in <Language> using edit
      | Day | Event1   | Event2    | Event3   | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Wed | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Thu | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Fri | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Sat | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
      | Sun | 06:30,ON | 08:30,OFF | 10:30,ON | 13:00,OFF | 15:30,ON | 22:30,OFF |
    Then Verify if the Schedule is set for the whole week
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |


  @SC-TH-UI46
  Scenario Outline: SC-TH-UI46_Setting up a customized schedule for heat
    Given The telegesis is paired with given heating devices
    When the below heat schedule is set on the <DeviceType> screen in <Language> using edit and copy to <COPYTO> days
      | Day | Event1     | Event2    | Event3     | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,1.0 | 12:00,17.0 | 14:00,1.0 | 16:30,31.0 | 22:00,1.0 |
    And Verify if the below Schedule is set for the whole week
      | Day | Event1     | Event2    | Event3     | Event4    | Event5     | Event6    |
      | Mon | 06:30,15.0 | 08:30,1.0 | 12:00,17.0 | 14:00,1.0 | 16:30,31.0 | 22:00,1.0 |
      | Tue | 06:30,15.0 | 08:30,1.0 | 12:00,17.0 | 14:00,1.0 | 16:30,31.0 | 22:00,1.0 |
      | Wed | 06:30,18.0 | 08:30,1.0 | 12:00,1.0  | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Thu | 06:30,18.0 | 08:30,1.0 | 12:00,1.0  | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Fri | 06:30,18.0 | 08:30,1.0 | 12:00,1.0  | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Sat | 06:30,18.0 | 08:30,1.0 | 12:00,1.0  | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |
      | Sun | 06:30,18.0 | 08:30,1.0 | 12:00,1.0  | 14:00,1.0 | 16:30,18.0 | 22:00,1.0 |

    Examples:
      | DeviceType | Language | BM    | COPYTO |
      | SLT3b      | English  | SLR2b | Tue    |

  @SC-TH-UI47
  Scenario Outline: SC-TH-UI47_Setting up a customized schedule for hot water
    Given The telegesis is paired with given heating devices
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    When the HOTWATER Schedule is set with default-schedule with StartOver on the <DeviceType> screen in <Language>
    And Verify if the below Schedule is set for the whole week
      | Day | Event1   | Event2    | Event3    | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Wed | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Thu | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Fri | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Sat | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Sun | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
    When the below HOTWATER schedule is set on the <DeviceType> screen in <Language> using edit and copy to <COPYTO> days
      | Day | Event1     | Event2    | Event3     | Event4    | Event5     | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,ON | 16:00,ON | 21:30,OFF |
    And Verify if the below Schedule is set for the whole week
      | Day | Event1   | Event2    | Event3   | Event4    | Event5   | Event6    |
      | Mon | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,ON | 16:00,ON | 21:30,OFF |
      | Tue | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,ON | 16:00,ON | 21:30,OFF |
      | Wed | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Thu | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Fri | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Sat | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |
      | Sun | 06:30,ON | 08:30,OFF | 12:00,OFF | 14:00,OFF | 16:00,ON | 21:30,OFF |

    Examples:
      | DeviceType | Language | BM    | COPYTO |
      | SLT3b      | English  | SLR2b | Tue    |

  @SC-TH-UI48
  Scenario Outline: SC-TH-UI48_Setting up a customized schedule for heat
    Given The telegesis is paired with given heating devices
    When the HEAT Schedule maximum and minimum start time of an event is validated on the <DeviceType> screen in <Language>

  Examples:
      | DeviceType | Language | BM    |
      | SLT3b      | English  | SLR2b |
  # Created by Fazila.Nizar on 15/11/2017
  @SC-TH-UIMC-01 @UITest

  Scenario Outline: SC-TH-UIMC-01_Set and validate mode change of Heat from OFF to Auto Mode on the Thermostat
    Given The telegesis is paired with given heating devices
      #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
      #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-02 @UITest
  Scenario Outline: SC-TH-UIMC-02_Set and validate mode change of Heat from OFF to Schedule Mode on the Thermostat
    Given The telegesis is paired with given heating devices
      #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
      #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-03 @UITest

  Scenario Outline: SC-TH-UIMC-03_Set and validate modecChange of Heat from OFF to BOOST Mode on the Thermostat
    Given The telegesis is paired with given heating devices
      #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
      #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-04 @UITest

  Scenario Outline: SC-TH-UIMC-04_Set and validate mode change of Heat from OFF to Holiday Mode on the Thermostat

    Given The telegesis is paired with given heating devices
     #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-05 @UITest

  Scenario Outline: SC-TH-UIMC-05_Set and validate mode change of Heat from Manual to OFF Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
   #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-06 @UITest
  Scenario Outline: SC-TH-UIMC-06_Set and validate mode change of Heat from Manual to Schedule Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-07 @UITest

  Scenario Outline: SC-TH-UIMC-07_Set and validate mode change of Heat from Manual to BOOST Mode on the Thermostat
    Given The telegesis is paired with given heating devices
      #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
      #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-08 @UITest

  Scenario Outline: SC-TH-UIMC-08_Set and validate mode change of Heat from Manual to Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
     #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-09 @UITest

  Scenario Outline: SC-TH-UIMC-09_Set and validate mode change of Heat from Schedule to OFF Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-10 @UITest
  Scenario Outline: SC-TH-UIMC-10_Set and validate mode change of Heat from Schedule to Manual Mode on the Thermostat
    Given The telegesis is paired with given heating devices
   #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
   #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-11 @UITest

  Scenario Outline: SC-TH-UIMC-11_Set and validate mode change of Heat from Schedule to BOOST Mode on the Thermostat
    Given The telegesis is paired with given heating devices
   #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-12 @UITest
  Scenario Outline: SC-TH-UIMC-12_Set and validate mode change of Heat from Schedule to Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-13 @UITest
  Scenario Outline: SC-TH-UIMC-13_Set and validate mode change of Hotwater from Always OFF to Always ON Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
  #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-14 @UITest
  Scenario Outline: SC-TH-UIMC-14_Set and validate mode change of Hotwater from Always OFF to Boost Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
  #HOTWATER BOOST MODE
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-15 @UITest
  Scenario Outline: SC-TH-UIMC-15_Set and validate mode change of Hotwater from Always OFF to AUTO Mode on the Thermostat
    Given The telegesis is paired with given heating devices
   #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
   #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-16 @UITest
  Scenario Outline: SC-TH-UIMC-16_Set and validate mode change of Hotwater from Always OFF to Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-17 @UITest
  Scenario Outline: SC-TH-UIMC-17_Set and validate mode change of Hotwater from Always ON to Always OFF Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
  #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-18 @UITest
  Scenario Outline: SC-TH-UIMC-18_Set and validate mode change of Hotwater from Always ON to Boost Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
  #HOTWATER BOOST MODE
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-19 @UITest
  Scenario Outline: SC-TH-UIMC-19_Set and validate mode change of Hotwater from Always ON to AUTO Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-20 @UITest
  Scenario Outline: SC-TH-UIMC-20_Set and validate mode change of Hotwater from Always ON to Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-21 @UITest
  Scenario Outline: SC-TH-UIMC-21_Set and validate mode change of Hotwater from Auto to Always OFF Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    #ALWAYS OFF MODE
    When the HOTWATER OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always OFF
    And validate current HOTWATER mode as OFF on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-22 @UITest
  Scenario Outline: SC-TH-UIMC-22_Set and validate mode change of Hotwater from Auto to Boost Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    #HOTWATER BOOST MODE
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-23 @UITest
  Scenario Outline: SC-TH-UIMC-23_Set and validate mode change of Hotwater from AUTO to Always ON on the Thermostat
    Given The telegesis is paired with given heating devices
    #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    #ALWAYS ON MODE
    When the HOTWATER ON is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as Always ON
    And validate current HOTWATER mode as ON on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-24 @UITest
  Scenario Outline: SC-TH-UIMC-24_Set and validate mode change of Hotwater from Auto to Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
    #AUTO MODE
    When the HOTWATER SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO
    And validate current HOTWATER mode as SCHEDULE on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-25 @UITest
  Scenario Outline: SC-TH-UIMC-25_Set and validate the Holiday Mode on the Thermostat for particular days
    Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-26 @UITest
  Scenario Outline: SC-TH-UIMC-26_Set,edit and validate the Holiday Mode on the Thermostat for particular days
    Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to Edit and validated
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |


  @SC-TH-UIMC-27 @UITest
  Scenario Outline: SC-TH-UIMC-27_Cancel the Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to cancel and validated

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |


  @SC-TH-UIMC-28 @UITest
  Scenario Outline: SC-TH-UIMC-28_Change the temperature of the Holiday Mode on the Thermostat
    Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to Edit and validated
    When the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 11.0 on the stat

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-29 @UITest

  Scenario Outline: SC-TH-UIMC-29_Set and validate mode change of Heat from Schedule Mode to Auto Mode on the Thermostat
    Given The telegesis is paired with given heating devices
   #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
   #MANUAL MODE
    When the heat MANUAL is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    And validate current Heat mode as MANUAL on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-30 @UITest
  Scenario Outline: SC-TH-UIMC-30_Set and validate mode change of Heat from Schedule Mode to OFF on the Thermostat
    Given The telegesis is paired with given heating devices

    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>

    #OFF MODE
    When the heat OFF is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-31 @UITest

  Scenario Outline: SC-TH-UIMC-31_Set and validate modecChange of Heat from Schedule Mode to BOOST Mode on the Thermostat
    Given The telegesis is paired with given heating devices

   #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>

    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-32 @UITest

  Scenario Outline: SC-TH-UIMC-32_Set and validate mode change of Heat from Schedule Mode to Holiday Mode on the Thermostat

    Given The telegesis is paired with given heating devices

    #SCHEDULE MODE
    When the heat SCHEDULE is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as AUTO with Current Target Temperature
    And validate current Heat mode as SCHEDULE on the <DeviceType> screen in <Language>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    #HOLIDAY MODE
    When the HOLIDAY Mode is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as HOLIDAY with Target Temperature as 7.0
    And validate current Holiday mode as Enabled on the <DeviceType> screen in <Language>
    And the Holiday Mode is deactivated using button on the <Language> in <DeviceType>
    And validate current Heat mode as OFF on the <DeviceType> screen in <Language>
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |


  @SC-TH-UIMC-33 @UITest

  Scenario Outline: SC-TH-UIMC-33_Making a change in Holiday Mode and then leaving the screen on the Thermostat
    Given The telegesis is paired with given heating devices
    #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And validate if the screen remains in Holiday Mode on the <DeviceType> in <Language> after 60 seconds

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-34 @UITest

  Scenario Outline: SC-TH-UIMC-34_set and change the temperature of the Holiday Mode and cancel it on the Thermostat
    Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to Edit and validated
    When the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to cancel and validated

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-35 @UITest

  Scenario Outline: SC-TH-UIMC-35_set and change the temperature of the Holiday Mode and cancel it on the Thermostat
    Given The telegesis is paired with given heating devices
    #HOLIDAY MODE
    When the <DeviceType> <Language> is in the MainMenu Screen
    Then the MainMenu options are validated in <Language>
    Then validate if the Back Button is enabled on <DeviceType>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

  @SC-TH-UIMC-36 @UITest

  Scenario Outline: SC-TH-UIMC-36_Set Heat boost on the Thermostat and validate if the Back Button is lit
    Given The telegesis is paired with given heating devices

    #BOOST MODE
    When the heat boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current Heat mode as Boost on the <DeviceType> screen in <Language>
    Then validate if the Back Button is enabled on <DeviceType>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

 @SC-TH-UIMC-37 @UITest
  Scenario Outline: SC-TH-UIMC-37_Set Hot Water boost on the Thermostat and validate if the Back Button is lit

    #HOTWATER BOOST MODE
    When the HOTWATER boost is activated using button on the <Language> <DeviceType>
    Then Automatically validate current mode as BOOST
    And validate current HOTWATER mode as Boost on the <DeviceType> screen in <Language>
    Then validate if the Back Button is enabled on <DeviceType>

    Examples:
      | DeviceType | Language |
      | SLT3b      | English  |

 @SC-TH-UIMC-38 @UITest
  Scenario Outline: SC-TH-UIMC-38_Set Holiday Mode on the Thermostat and validate if the Back Button is lit

   Given The telegesis is paired with given heating devices
  #HOLIDAY MODE
    When the HOLIDAY Mode is set with 2 hours ahead after 2 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 4 hours ahead after 6 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 8.0 on the stat
    Then the HOLIDAY Mode set on the <DeviceType> <Language> is set to Edit and validated
    When the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the start date
    And the HOLIDAY Mode is set with 0 hours ahead after 0 days using button on the <DeviceType> in  <Language> for the End date
    And Set current mode as HOLIDAY with Target Temperature as 11.0 on the stat
    Then validate if the Back Button is enabled on <DeviceType>

     Examples:
    | DeviceType | Language |
    | SLT3b      | English  |