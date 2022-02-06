# Created by fazila.nizar at 25/06/2017

Feature: Performs regression on the Boiler Module for the Device type SLR1b.

  #Boiler Module, Plug and the thermostat must be paired before executing the below ones

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Zigbee Binding Test

  @SLR1b_RegressionTest @SC-ZT-37
  Scenario Outline: SC-ZT-37_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLR1b      |

    Examples:
      | DeviceType |
      | SLR1b      |

  @SLR1b_RegressionTest @SC-NT-JN01-27 @PairingTest
  Scenario: SC-NT-JN01-27_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            | BMMacID          | plugMacID        |
      | TH         | SLT3       | 000D6F000BEF0BE6 | 000D6F000E7F9A5F | 001E5E09023421E6 |

  @SLR1b_RegressionTest @SC-GT-SC06-18
  Scenario: SC-GT-SC06-18_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            | BMMacID          | plugMacID        |
      | TH         | SLT3       | 001E5E09020E5638 | 001E5E0902020EF7 | 001E5E09023421E6 |

  @SLR1b_RegressionTest @SC-FT-65
  Scenario: SC-FT-65_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR1b      | 1.05           | NA             |
      | BM         | SLR1b      | NA             | 9.09           |
      | BM         | SLR1b      | 1.05           | NA             |

  @SLR1b_RegressionTest @SC-BT-43
  Scenario Outline: SC-BT-43_To set bindings and validate the binding table on the device via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 6 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the reportable attributes are set to report for the given timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the specified timeperiod
    And the values of the reportable attributes should be the set value
    When the reportable attributes are set to report for the default timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the default timeperiod
    Then the values of the reportable attributes should be the default value
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the bindings are cleared on the device
    Then the binding table on the device should have 6 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the below devices are paired and unpaired sequentially and validated 1 times via Telegesis
      | DeviceName | DeviceType | MacID            | BMMacID          | plugMacID        |
      | BM         | SLR1b      | 000D6F000BEF0BE6 | 000D6F000BEF0BE6 | 000D6F000BEF0BE6 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 6 entries

    Examples:
      | DeviceType |
      | SLR1b      |
    
  @SLR1b_RegressionTest @SC-CH-MC-04
  Scenario Outline: SC-CH-MC-04_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
     When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Target Temperature is automatically set to 20.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to <FirstSetTemperature> on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as <FirstSetTemperature>
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
	 
    Examples:
      | FirstSetTemperature |
      | 27.0                |
    
  @SLR1b_RegressionTest @SC-CH-MC-11
  Scenario Outline: SC-CH-MC11_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to BOOST with Target Temperature as <Boost Temperature> for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Target Temperature is automatically set to 7.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 7.0

    Examples:
      | Boost Temperature |
      | 27.0              |
    
  @SLR1b_RegressionTest @SC-CH-MC17
  Scenario Outline: SC-CH-MC17_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to BOOST with Target Temperature as <Boost Temperature> for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as <Boost Temperature>
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Target Temperature is automatically set to <AutoOverRideTemperature> on the Client
    Then Automatically validate current mode as OVERRIDE with Target Temperature as <AutoOverRideTemperature>
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | AutoOverRideTemperature | Boost Temperature |
      | 12.0                    | 27.0              |
    
  @SLR1b_RegressionTest @SC-CH-MC23
  Scenario Outline: SC-CH-MC23_Validate the Mode change for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Current Target Temperature
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to <FirstSetTemperature> on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as <FirstSetTemperature>
    When Mode is automatically changed to MANUAL on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 20.0
    When Target Temperature is automatically set to 7.0 on the Client
    Then Automatically validate current mode as MANUAL with Target Temperature as 7.0
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0

    Examples:
      | FirstSetTemperature |
      | 27.0                |

  @SLR1b_RegressionTest @SC-CH-SH10
  Scenario Outline: SC-CH-SH10_Set the given customized 'six' event schedule for all day of the week and verify the same for Central Heating
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
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SLR1b_RegressionTest @SC-CH-SH11
  Scenario Outline: SC-CH-SH11_Set the given customized 'four' event schedule for all day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 12:00      |
      | 30.0               | 14:00      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SLR1b_RegressionTest @SC-CH-SH12
  Scenario Outline: SC-CH-SH12_Set the given customized 'two' event schedule for all day of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When The below schedule is set for <Day> on the Client
      | Target Temperature | Start Time |
      | 29.0               | 08:30      |
      | 1.0                | 16:30      |
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |
    
  @SC-CH-SH31 @SLR1b_RegressionTest
  Scenario Outline: SC-CH-SH31_Set the 'six' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When 6 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-CH-SH32 @SLR1b_RegressionTest
  Scenario Outline: SC-CH-SH32_Set the 'four' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When 4 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |

  @SC-CH-SH33 @SLR1b_RegressionTest
  Scenario Outline: SC-CH-SH33_Set the 'two' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When 2 event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |
	
  @SC-CH-SH12-34 @SLR1b_RegressionTest
  Scenario Outline: SC-CH-SH12_34_Set the 'six, four or two' event random schedule for all days of the week and verify the same for Central Heating
    Given The Hive product is paired and setup for Central Heating with API Validation
    When Any event Random schedule is generated and set for <Day> on the Client
    Then Verify if the Schedule is set

    Examples:
      | Day       |
      | Sunday    |
      | Monday    |
      | Tuesday   |
      | Wednesday |
      | Thursday  |
      | Friday    |
      | Saturday  |