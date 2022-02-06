# Created by fazila.nizar at 11/05/2017

Feature: Performs regression on Active Light for the Device type FWBR30Bulb01US

#Zigbee Dump Test 
#Pairing Test in all Channels
#Pairing & Unpairing in same Channel
#OTA firmware upgrade\downgrade Test
#OTA firmware with reboot during upgrade\downgrade Test
#Device ON\OFF test
#brightness Test
#Zigbee Binding Test

  @FWBR30Bulb01US_RegressionTest @SC-RG-ZT-31 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-31_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType     |
      | FWBR30Bulb01US |

    Examples:
      | DeviceType     |
      | FWBR30Bulb01US |

  @FWBR30Bulb01US_RegressionTest @SC-RG-NT-JN01-16 @PairingTest
  Scenario: SC-RG-NT-JN01-16_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType     | MacID            |
      | AL         | FWBR30Bulb01US | 00158D0001659C25 |

  @FWBR30Bulb01US_RegressionTest @SC-NT-JN05-12 @Generic
  Scenario: SC-NT-JN05-12_The given devices are paired and unpaired sequentially and validated in the same channel twice
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType     | MacID            |
      | AL         | FWBR30Bulb01US | 00158D0001659C25 |

  @FWBR30Bulb01US_RegressionTest @SC-FT-40 @FirmwareTest
  Scenario: SC-FT-40_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType     | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBR30Bulb01US | NA             | 11300002       |
      | AL         | FWBR30Bulb01US | 11340002       | NA             |

  @FWBR30Bulb01US_RegressionTest @SC-SP-DP01-16 @DevicePairingTest
  Scenario Outline: SC-SP-DP01-16_The Device state is changed and validated the using zigbee attribute twice
    Given The telegesis is paired with given <DeviceType>
    When the <DeviceType> state is changed to below states and validated using the zigbee attribute and repeated 2 times
      | State |
      | OFF   |
      | ON    |

    Examples:
      | DeviceType     |
      | FWBR30Bulb01US |

  @FWBR30Bulb01US_RegressionTest @SC-FW-04 @ActiveLight
  Scenario: SC-FW-04_Switch ActiveLight to change the brightness of the light and validate the same
    Given The telegesis is paired with given devices
    When The brightness value of the FW bulb is changed and validated for the given Brightness value infinitely via telegesis
      | BrightnessValue | TimeLapse |
      | ON              | 1         |
      | 01              | 1         |
      | 20              | 1         |
      | 40              | 1         |
      | 60              | 1         |
      | 99              | 1         |
      | OFF             | 1         |

  @FWBR30Bulb01US_RegressionTest @SC-BT-36 @ZigbeeBindingTest
  Scenario Outline: SC-BT-36_To set bindings and validate the binding table on the device via telegesis stick.
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
      | DeviceName | DeviceType     | MacID            |
      | AL         | FWBR30Bulb01US | 00158D0001659C25 |
    When the binding table on the device is verified via telegesis stick
    Then the binding table on the device should have 0 entries

    Examples:
      | DeviceType     |
      | FWBR30Bulb01US |