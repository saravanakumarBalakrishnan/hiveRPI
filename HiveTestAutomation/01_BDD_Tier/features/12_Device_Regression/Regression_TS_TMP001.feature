# Created by kingston.samselwyn at 04/07/2017
Feature: Performs regression on the Motion Sensor for the Device type TMP001

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Zigbee Binding Test

  @TMP001_RegressionTest @SC-ZT-42
  Scenario Outline: SC-ZT-27_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | TMP001     |

    Examples:
      | DeviceType |
      | TMP001     |

  @TMP001_RegressionTest @SC-NT-JN05-32
  Scenario: SC-NT-JN01-32_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | TS         | TMP001     | 00124B00146D2940 |

  @TMP001_RegressionTest @SC-GT-SC06-20
  Scenario: SC-GT-SC06-20_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | TS         | TMP001     | 00124B00146D2940 |


  @TMP001_RegressionTest @SC-FT-57
  Scenario: SC-FT-47_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TS         | TMP001     | NA             | 3.0.6          |
      | TS         | TMP001     | 3.0.4          | NA             |
      | TS         | TMP001     | NA             | 3.0.6          |

  @TMP001_RegressionTest @SC-BT-49
  Scenario Outline: SC-BT-49_To set bindings and validate the binding table on the device via telegesis stick.
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
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the values of the reportable attributes should be the default value
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries
    When the zigbee clusters on the device are bound to the telegesis stick
    Then validate if the Bindings are set correctly
    When the below devices are paired and unpaired sequentially and validated 1 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | TS         | TMP001     | 00124B00146D2940 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType |
      | TMP001     |