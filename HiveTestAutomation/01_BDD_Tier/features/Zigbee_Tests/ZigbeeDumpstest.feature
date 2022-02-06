Feature: This feature file contains scenarios to validate the Zigbee cluster and attributes with the baseline dump.

  @SC-ZT-01 @ZigbeeDumpTet @test
  Scenario Outline: SC-ZT-01_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLP2       |

    Examples:
      | DeviceType |
      | SLP2       |


  @SC-ZT-02 @ZigbeeDumpTet @test
  Scenario Outline: SC-ZT-02_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLP2C      |

    Examples:
      | DeviceType |
      | SLP2C      |
  
