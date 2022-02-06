Feature: Consists of scenario that validates the network between devices

  @SC-NT-JN01-01 @PairingTest
  Scenario: SC-NT-JN01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SB         | SLB1       | 001E5E09020F6AE0 |
      | SP         | SLP2       | 001E5E09020F2F4C |

  @SC-NT-JN01-02 @PairingTest
  Scenario: SC-NT-JN01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | SLL1       | 000D6F000B99FC75 |


  @SC-NT-JN01-03 @PairingTest
  Scenario: SC-NT-JN01-03_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | FWBulb01US | 00158D00012E4C02 |

  @SC-NT-JN01-04 @PairingTest
  Scenario: SC-NT-JN01-04_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2       | 000D6F000BC650BD |

  @SC-NT-JN01-05 @PairingTest
  Scenario: SC-NT-JN01-05_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | TWBulb01UK | 00158D00012E4419 |

  @SC-NT-JN01-06 @PairingTest
  Scenario: SC-NT-JN01-06_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | TWBulb01US | 00158D0001361200 |

    @SC-NT-JN01-07 @PairingTest
  Scenario: SC-NT-JN01-06_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | RGBBulb01UK| 00158D00014F34AD |


  @SC-NT-JN02-01 @PairingTest
  Scenario: SC-NT-JN02-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Hub
      | DeviceName | DeviceType      |
      | AL         | LDS_DimmerLight |

  @SC-NT-JN02-02 @PairingTest
  Scenario: SC-NT-JN02-02_The given devices are paired and unpaired sequentially and validated
    Given The Clipin are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | CB         | CL01_1     |

  @SC-NT-JN03-01 @PairingTest
  Scenario: SC-NT-JN03-01_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | AL         | FWBulb01_1 |

  @SC-NT-JN03-02 @PairingTest
  Scenario: SC-NT-JN03-02_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO1 Hub
      | DeviceName | DeviceType |
      | AL         | FWBulb01_1 |

  @SC-NT-JN03-03 @PairingTest
  Scenario: SC-NT-JN03-01_The given devices are paired and unpaired sequentially and validated
    Given The Active Lights are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO1 Hub
      | DeviceName | DeviceType   |
      | AL         | TWBulb01UK_1 |

  @SC-NT-JN04-01 @PairingTest
  Scenario: SC-NT-JN04-01_The given devices are paired and unpaired sequentially and validated
    Given The Smart Plugs are paired with the Hive Hub
    When the below devices are paired and unpaired sequentially and validated infinitely via NANO2 Hub
      | DeviceName | DeviceType |
      | SB         | SLB1_1     |

  @SC-NT-JN01-09 @PairingTest
  Scenario: SC-NT-JN01-09_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType     | MacID            |
      | AL         | FWGU10Bulb01UK | 00158D0001743547 |
    
    
  @SC-NT-BT01-01 @Generic
  Scenario: SC-NT-BT01-01_The given devices are paired and unpaired sequentially and validated in the same channel
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired after 4 minutes and send identify command sequentially validated 10 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | BT         | Button01   | 00158D0001CB8BEA |
    
  @SC-NT-BT01-02 @Generic
  Scenario: SC-NT-BT01-01_The given devices are paired and unpaired sequentially and validated in the same channel
    Given The telegesis is paired with given devices
    When the below devices are re-paired and send identify command for 5 seconds and wait 2 seconds sequentially validated 10 times for 10 iterations via Telegesis
      | DeviceName | DeviceType | MacID            |
      | BT         | Button01   | 00158D0001CB8BEA |

   @SC-NT-JN04-04 @PairingTest
  Scenario: SC-NT-JN04-04_The given devices are paired and unpaired sequentially and validated
    Given The Smart Plugs are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2c_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2c_1   |

    @SC-NT-JN04-05 @PairingTest
  Scenario: SC-NT-JN04-05_The given devices are paired and unpaired sequentially and validated
    Given The Smart Plugs are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2d_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2d_1   |

  @SC-NT-JN04-06 @PairingTest
  Scenario: SC-NT-JN04-06_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWBulb01_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWBulb01_1   |

    @SC-NT-JN04-07 @PairingTest
  Scenario: SC-NT-JN04-07_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWGU10Bulb01UK_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWGU10Bulb01UK_1   |


  @SC-NT-JN04-08 @PairingTest
  Scenario: SC-NT-JN04-08_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWBulb01US_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWBulb01US_1   |

  @SC-NT-JN04-09 @PairingTest
  Scenario: SC-NT-JN04-09_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWPAR38Bulb01US_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWPAR38Bulb01US_1   |

  @SC-NT-JN04-10 @PairingTest
  Scenario: SC-NT-JN04-10_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |

  @SC-NT-JN04-11 @PairingTest
  Scenario: SC-NT-JN04-11_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01US_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01US_1   |

   @SC-NT-JN04-12 @PairingTest
  Scenario: SC-NT-JN04-12_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | RGBBulb01UK_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | RGBBulb01UK_1   |

 @SC-NT-JN04-13 @PairingTest
  Scenario: SC-NT-JN04-13_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | RGBBulb01US_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | RGBBulb01US_1   |

 @SC-NT-JN04-14 @PairingTest
  Scenario: SC-NT-JN04-14_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB1_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB1_1   |

 @SC-NT-JN04-15 @PairingTest
  Scenario: SC-NT-JN04-15_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB2_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB2_1   |

 @SC-NT-JN04-16 @PairingTest
  Scenario: SC-NT-JN04-16_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB2c_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB2c_1   |

 @SC-NT-JN04-17 @PairingTest
  Scenario: SC-NT-JN04-17_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB3_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB3_1   |

 @SC-NT-JN04-18 @PairingTest
  Scenario: SC-NT-JN04-18_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | MS         | PIR00140005_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | MS         | PIR00140005_1   |

 @SC-NT-JN04-19 @PairingTest
  Scenario: SC-NT-JN04-19_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | MS         | MOT003_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | MS         | MOT003_1   |

 @SC-NT-JN04-20 @PairingTest
  Scenario: SC-NT-JN04-20_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CS         | DWS003_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CS         | DWS003_1   |

 @SC-NT-JN04-21 @PairingTest
  Scenario: SC-NT-JN04-21_The given devices are paired and unpaired sequentially and validated
    Given The Active Light are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CS         | WDS00140002_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CS         | WDS00140002_1   |

 @SC-NT-JN01-10 @PairingTest
  Scenario: SC-NT-JN01-10_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    Then the below devices are unpaired via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
    Then the below devices are paired via Telegesis
      | DeviceName | DeviceType | MacID            |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |
      | AL         | FWBulb01US | 00158D00012E4C02 |