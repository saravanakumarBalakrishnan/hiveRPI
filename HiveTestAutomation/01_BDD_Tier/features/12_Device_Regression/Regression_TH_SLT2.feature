# Created by fazila.nizar at 25/06/2017

Feature: Performs regression on the Thermostat for the Device type SLT2.

  #Boiler Module, Plug and the thermostat must be paired before executing the below ones

  #Zigbee Dump Test 
  #Pairing Test in all Channels
  #Pairing & Unpairing in same Channel
  #OTA firmware upgrade\downgrade Test
  #Zigbee Binding Test

  @SLT2_RegressionTest @SC-ZT-34
  Scenario Outline: SC-ZT-34_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLT2       |

    Examples:
      | DeviceType |
      | SLT2       |

  @SLT2_RegressionTest @SC-NT-JN01-24 @PairingTest
  Scenario: SC-NT-JN01-24_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            | BMMacID          | plugMacID        |
      | TH         | SLT2       | 000D6F000BEF0BE6 | 000D6F000E7F9A5F | 001E5E09023421E6 |

  @SLT2_RegressionTest @SC-GT-SC06-15
  Scenario: SC-GT-SC06-15_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            | BMMacID          | plugMacID        |
      | TH         | SLT2       | 001E5E09020E5638 | 001E5E0902020EF7 | 001E5E09023421E6 |

  @SLT2_RegressionTest @SC-FT-62
  Scenario: SC-FT-62_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT2       | 6.00           | NA             |
      | TH         | SLT2       | NA             | 5.15           |
      | TH         | SLT2       | 6.00           | NA             |

  @SLT2_RegressionTest @SC-BT-40
  Scenario Outline: SC-BT-40_To set bindings and validate the binding table on the device via telegesis stick.
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
      | TH         | SLT2       | 000D6F000BEF0BE6 | 000D6F000BEF0BE6 | 000D6F000BEF0BE6 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 6 entries

    Examples:
      | DeviceType |
      | SLT2       |
