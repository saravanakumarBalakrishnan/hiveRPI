# Created by fazila.nizar at 11/05/2017

Feature: Performs regression on Smart Plug for the Device type SLP2c

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Device ON\OFF test
  #Zigbee Binding Test

  @SLP2c_RegressionTest @SC-ZT-14 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-14_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLP2c      |

    Examples:
      | DeviceType |
      | SLP2c      |

  @SLP2c_RegressionTest @SC-NT-JN05-03 @PairingTest
  Scenario: SC-NT-JN05-03_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2c      | 001E5E090217676F |

  @SLP2c_RegressionTest @SC-GT-SC06-03 @Generic
  Scenario: SC-GT-SC06-03_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2c      | 001E5E090217676F |

  @SLP2c_RegressionTest @SC-FT-45 @FirmwareTest
  Scenario: SC-FT-45_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2c      | 3.10           | NA             |
      | SP         | SLP2c      | 3.15           | NA             |

  @SLP2c_RegressionTest @SC-SP-DP01-07 @DevicePairingTest
  Scenario Outline: SC-SP-DP01-07_The smart plug state is changed and validated the using zigbee attribute twice
    Given The telegesis is paired with given <DeviceType>
    When the <DeviceType> state is changed to below states and validated using the zigbee attribute and repeated 2 times
      | State |
      | ON    |
      | OFF   |

    Examples:
      | DeviceType |
      | SLP2c      |

  @SLP2c_RegressionTest @SC-BT-20 @ZigbeeBindingTest # Enter the Mac id of the Device
  Scenario Outline: SC-BT-20_To set bindings and validate the binding table on the device via telegesis stick.
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
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2c      | 001E5E090217676F |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType |
      | SLP2c      |

