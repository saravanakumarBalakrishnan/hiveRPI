# Created by Shiva Kadu at 23/05/2017
# Modified by Fazila Nizar at 31/05/2017

Feature: Performs regression on Active Light for the Device type RGBBulb01UK

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #OTA firmware with reboot during upgrade\downgrade Test
  #Device ON\OFF test
  #Hue, saturation and brightness Test
  #Zigbee Binding Test

  @RGBBulb01Uk_RegressionTest @SC-RG-ZT-20 @ZigbeeDumpTest
  Scenario Outline: SC-RG-ZT-20_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType  |
      | RGBBulb01UK |

    Examples:
      | DeviceType  |
      | RGBBulb01UK |

  @RGBBulb01Uk_RegressionTest @SC-RG-NT-JN01-10 @PairingTest
  Scenario: SC-RG-NT-JN01-10_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType  | MacID            |
      | AL         | RGBBulb01UK | 00158D00014F34AD |

  @RGBBulb01Uk_RegressionTest @SC-RG-GT-SC06-10 @Generic
  Scenario: SC-RG-GT-SC06-10_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType  | MacID            |
      | AL         | RGBBulb01UK | 00158D00014F34AD |

  @RGBBulb01Uk_RegressionTest @SC-FT-51 @FirmwareTest
  Scenario: SC-FT-51_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01UK | NA             | 11140002       |
      | AL         | RGBBulb01UK | 11200002       | NA             |

  @RGBBulb01Uk_RegressionTest @SC-SP-DP01-10 @DevicePairingTest
  Scenario Outline: SC-SP-DP01-10_The Device state is changed and validated the using zigbee attribute twice
    Given The telegesis is paired with given <DeviceType>
    When the <DeviceType> state is changed to below states and validated using the zigbee attribute and repeated 2 times
      | State |
      | OFF   |
      | ON    |

    Examples:
      | DeviceType  |
      | RGBBulb01UK |

  @RGBBulb01Uk_RegressionTest @SC-RGB-01 @ActiveLight
  Scenario Outline: SC-RGB-01_Change Hue with Saturation and brightness in a RGB Bulb by changing the Hue with saturation and brightness respectively
    Given The telegesis is paired with given devices
    When The hue value of the <DeviceType> is changed and validated for the given saturation and brightness value infinitely via telegesis
      | HueValue | SatValue | Brightness | TimeLapse |
      | 00       | 00       | 01          | 1         |
      | 01       | 2F       | 10         | 1         |
      | 21       | 3F       | 20         | 1         |
      | 31       | 4F       | 30         | 1         |
      | 41       | 5F       | 40         | 1         |
      | 51       | 6F       | 50         | 1         |
      | 61       | 7F       | 60         | 1         |
      | 71       | 8F       | 70         | 1         |
      | 81       | 9F       | 80         | 1         |
      | 91       | BF       | 90         | 1         |
      | A1       | FE       | 100        | 1         |
      | 01       | 2F       | 10         | 1         |

    Examples:
      | DeviceType  |
      | RGBBulb01UK |

  @RGB_RegressionTest @SC-BT-26 @ZigbeeBindingTest
  Scenario Outline: SC-BT-26_To set bindings and validate the binding table on the device via telegesis stick.
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
      | DeviceName | DeviceType  | MacID            |
      | AL         | RGBBulb01UK | 00158D0001743547 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType |
      | RGBBulb01UK|