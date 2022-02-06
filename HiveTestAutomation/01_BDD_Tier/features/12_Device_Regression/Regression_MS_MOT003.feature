# Created by kingston.samselwyn at 04/07/2017
Feature: Performs regression on the Motion Sensor for the Device type MOT003

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Zigbee Binding Test

  @MOT003_RegressionTest @SC-ZT-26
  Scenario Outline: SC-ZT-26_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | MOT003     |

    Examples:
      | DeviceType |
      | MOT003     |

  @MOT003_RegressionTest @SC-NT-JN05-17
  Scenario: SC-NT-JN05-17_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | MS         | MOT003     | 00124B000D7C0318 |

  @MOT003_RegressionTest @SC-GT-SC06-08
  Scenario: SC-GT-SC06-08_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | MS         | MOT003     | 00124B000D7C0318 |


  @MOT003_RegressionTest @SC-FT-41
  Scenario: SC-FT-41_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | MS         | MOT003     | NA             | 3.0.6          |
      | MS         | MOT003     | 3.0.4          | NA             |
      | MS         | MOT003     | NA             | 3.0.6          |

  @MOT003_RegressionTest @SC-BT-32
  Scenario Outline: SC-BT-14_To set bindings and validate the binding table on the device via telegesis stick.
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
      | MS         | MOT003     | 00124B000D7C0318 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries
    When the bindings are cleared on the device
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType |
      | MOT003     |