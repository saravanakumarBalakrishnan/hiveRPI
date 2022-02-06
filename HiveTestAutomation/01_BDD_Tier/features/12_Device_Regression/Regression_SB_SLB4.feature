# Created by fazila.nizar at 11/05/2017

Feature: Performs regression on the Signal Booster for the Device type SLB4

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Zigbee Binding Test

  @SLB4_RegressionTest @SC-ZT-32 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-32_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLB4       |

    Examples:
      | DeviceType |
      | SLB4       |

  @SLB4_RegressionTest @SC-NT-JN05-23 @PairingTest
  Scenario: SC-NT-JN05-08_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB4       | 000D6F000CA914BD |

  @SLB4_RegressionTest @SC-GT-SC06-23 @Generic
  Scenario: SC-GT-SC06-08_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB4       | 000D6F000CA914BD |

  @SLB4_RegressionTest @SC-FT-60 @FirmwareTest
  Scenario: SC-FT-49_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLB4       | 2.08           | NA             |
      | SP         | SLB4       | NA             | 2.09           |

  @SLB4_RegressionTest @SC-BT-33 @ZigbeeBindingTest
  Scenario Outline: SC-BT-24_To set bindings and validate the binding table on the device via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the below devices are paired and unpaired sequentially and validated 1 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLB4       | 000D6F000CA914BD |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType |
      | SLB4       |
