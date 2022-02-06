# Created by fazila.nizar at 27/09/2017

Feature: Performs regression on Active Light for the Device type TWCLBulb01UK

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #OTA firmware with reboot during upgrade\downgrade Test
  #Device ON\OFF test
  #Tune, brightness Test
  #Zigbee Binding Test

  @TWCLBulb01UK_RegressionTest @SC-ZT-72 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-39_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType   |
      | TWCLBulb01UK |

    Examples:
      | DeviceType   |
      | TWCLBulb01UK |

  @TWCLBulb01UK_RegressionTest @SC-RG-NT-JN01-20 @PairingTest
  Scenario: SC-RG-NT-JN01-18_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType   | MacID            |
      | AL         | TWCLBulb01UK | 00158D000177FCCE |

  @TWCLBulb01UK_RegressionTest @SC-NT-JN05-24 @Generic
  Scenario: SC-NT-JN05-21_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType   | MacID            |
      | AL         | TWCLBulb01UK | 00158D000177FCCE |

  @TWCLBulb01UK_RegressionTest @SC-FT-68 @FirmwareTest
  Scenario: SC-FT-67_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType   | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWCLBulb01UK | NA             | 11160002       |
      | AL         | TWCLBulb01UK | 11200002       | NA             |

  @TWCLBulb01UK_RegressionTest @SC-SP-DP01-22 @DevicePairingTest
  Scenario Outline: SC-SP-DP01-18_The Device state is changed and validated the using zigbee attribute twice
    Given The telegesis is paired with given <DeviceType>
    When the <DeviceType> state is changed to below states and validated using the zigbee attribute and repeated 2 times
      | State |
      | OFF   |
      | ON    |

    Examples:
      | DeviceType   |
      | TWCLBulb01UK |

  @TWCLBulb01UK_RegressionTest @SC-TW-05 @ActiveLight
  Scenario: SC-TW-03_Change Tune and Brightness in a TW Bulb by changing the Tune and Brightness respectively
    Given The telegesis is paired with given devices
    When The Tune value of the TW bulb is changed and validated for the given Brightness value infinitely via telegesis
      | Tune | BrightnessValue | TimeLapse |
      | 00A5 | ON              | 1         |
      | 00B8 | 01              | 1         |
      | 00C8 | 20              | 1         |
      | 00F0 | 40              | 1         |
      | 0162 | 60              | 1         |
      | 0171 | 99              | 1         |
      | 0172 | OFF             | 1         |

  @TWCLBulb01UK_RegressionTest @SC-BT-48 @ZigbeeBindingTest
  Scenario Outline: SC-BT-45_To set bindings and validate the binding table on the device via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the reportable attributes are set to report for the given timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the specified timeperiod
    And the values of the reportable attributes should be the set value
    When the reportable attributes are set to report for the default timeperiod
    Then the telegesis stick is mornitored and verified whether the attributes report for the default timeperiod
    Then the values of the reportable attributes should be the default value
    When the given attributes are set to report for the given timeperiod
      | DeviceType | ModelId | ClusterId | AttributeId | AttributeType | MinDuration | MaxDuration | EP |ChangeRep|
      | FFD        | TWCLBulb01UK  | 0006      | 0000        | 10            | 0001        | 0078        | 01 |     True     |
    When the device state is changed to OFF
    Then the telegesis stick is mornitored and verified whether the attributes report for the change immediately
    When the device state is changed to ON
    Then the telegesis stick is mornitored and verified whether the attributes report for the change immediately
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the below devices are paired and unpaired sequentially and validated 1 times via Telegesis
      | DeviceName | DeviceType   | MacID            |
      | AL         | TWCLBulb01UK | 00158D000177FCCE |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType   |
      | TWCLBulb01UK |

  @TWCLBulb01UK_RegressionTest @SC-FR-01
  Scenario: SC-FR-01_To Factory Reset the device and Verify the Btable after re-pairing via telegesis stick.
    Given The telegesis is paired with given devices
    When the device is reset and re-paired via plug to check binding table on the device repeatedly for 20 times via telegesis stick
      | DeviceName | DeviceType   | MacID            |
      | SP         | SLP2b | 001E5E090231B2C4 |