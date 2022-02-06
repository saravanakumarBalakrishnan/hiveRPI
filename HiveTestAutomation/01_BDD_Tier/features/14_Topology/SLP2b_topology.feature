# Created by kingston.samselwyn at 09/12/2016
Feature: Consists of scenario that validates the network topology between devices

  @SC-TT-SC01-03 @PairingTest @SC_TT_SC01_03
  Scenario: SC-TT-SC01-03_The given devices are paired and unpaired sequentially and validated via plug
    Given The Hive product is paired and setup for Routing Topology
    And the given attenuation is set on the network
      | Atten | DB |
      | 1_2   | 0  |
      | 2_3   | 0  |
      | 2_4   | 90 |
      | 1_3   | 90 |
      | 3_4   | 0  |
      | 1_4   | 90 |
    When the given topology is formed and verified
      | Parent     | Child      |
      | TGStick    | SLP2b      |
      | SLP2b      | TWBulb01UK |
      | TWBulb01UK | SLB1       |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01UK | NA             | 11180002       |
      | AL         | TWBulb01UK | 11140002       | NA             |
    Then change the state of the plug with mac address BOX2 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX2 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX3 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX3 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX1 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | NANO2      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX1 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | NANO2      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX4 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX4 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01UK | NA             | 11180002       |
      | AL         | TWBulb01UK | 11140002       | NA             |
    Then the below devices are unpaired via NANO2 Hub
      | DeviceName | DeviceType   |
      | AL         | TWBulb01UK_1 |
      | SP         | SLP2b_1      |
      | SB         | SLB1_1       |

    And the given attenuation is set on the network
      | Atten | DB |
      | 1_2   | 90 |
      | 2_3   | 0  |
      | 2_4   | 90 |
      | 1_3   | 0  |
      | 3_4   | 0  |
      | 1_4   | 90 |
    Then the below devices are paired via NANO2 Hub
      | DeviceName | DeviceType   |
      | AL         | TWBulb01UK_1 |
      | SP         | SLP2b_1      |
      | SB         | SLB1_1       |
    When the given topology is formed and verified
      | Parent     | Child      |
      | COO        | TWBulb01UK |
      | TWBulb01UK | SLP2b      |
      | SLP2b      | SLB1       |
    Then change the state of the plug with mac address BOX1 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | NANO2      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX1 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | NANO2      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX3 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    Then change the state of the plug with mac address BOX3 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLP2b      |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2b      | NA             | 01035700       |
      | SP         | SLP2b      | 01045700       | NA             |
    Then change the state of the plug with mac address BOX3 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    Then change the state of the plug with mac address BOX3 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    Then change the state of the plug with mac address BOX4 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    Then change the state of the plug with mac address BOX4 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | NA             | 01155120       |
      | SB         | SLB1       | 01125120       | NA             |
    Then the below devices are unpaired via NANO2 Hub
      | DeviceName | DeviceType   |
      | AL         | TWBulb01UK_1 |
      | SP         | SLB1_1       |
      | BM         | SLP2b_1      |

    And the given attenuation is set on the network
      | Atten | DB |
      | 1_2   | 90 |
      | 2_3   | 90 |
      | 2_4   | 0  |
      | 1_3   | 90 |
      | 3_4   | 0  |
      | 1_4   | 0  |
    Then the below devices are paired via NANO2 Hub
      | DeviceName | DeviceType   |
      | SB         | SLB1         |
      | SP         | SLP2b_1      |
      | AL         | TWBulb01UK_1 |
    When the given topology is formed and verified
      | Parent | Child      |
      | COO    | SLB1       |
      | SLB1   | TWBulb01UK |
      | SLB1   | SLP2b      |
    Then change the state of the plug with mac address BOX4 to OFF via telegesis through API
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLB1       |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Absent
      | DeviceType |
      | SLP2b      |
    Then change the state of the plug with mac address BOX4 to ON via telegesis through API
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLB1       |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | TWBulb01UK |
    And validate the time taken for the devices presence to go Present
      | DeviceType |
      | SLP2b      |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2b      | NA             | 01035700       |
      | SP         | SLP2b      | 01045700       | NA             |

