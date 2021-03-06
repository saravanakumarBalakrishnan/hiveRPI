Feature: This feature comprises of scenarios that test the firmware upgrade and downgrade

  @SC-FT-01 @FirmwareTest
  Scenario: SC-FT-01_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | 2.10           | 2.13           |

  @SC-FT-02 @FirmwareTest
  Scenario: SC-FT-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR1       | 7.13           | NA             |
      | BM         | SLR2       | 7.13           | NA             |
      | SB         | SLB1       | 1.08           | NA             |
      | SP         | SLP2       | 2.08           | NA             |
      | TH         | SLT3       | 2.10           | NA             |
      | TH         | SLT2       | 5.10           | NA             |
      | BM         | SLR1       | NA             | 7.15           |
      | BM         | SLR2       | NA             | 7.15           |
      | SB         | SLB1       | NA             | 1.09           |
      | SP         | SLP2       | NA             | 2.09           |
      | TH         | SLT3       | NA             | 2.13           |
      | TH         | SLT2       | NA             | 5.13           |

  @SC-FT-03 @FirmwareTest
  Scenario: SC-FT-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR1       | 7.06           | 7.15           |
      | BM         | SLR2       | 7.06           | 7.15           |
      | BM         | SLR1       | 7.13           | 7.15           |
      | BM         | SLR2       | 7.13           | 7.15           |
      | BM         | SLR1       | 7.11           | 7.15           |
      | BM         | SLR2       | 7.11           | 7.15           |
      | BM         | SLR1       | 7.15           | 7.06           |
      | BM         | SLR2       | 7.15           | 7.06           |
      | BM         | SLR1       | 7.15           | 7.13           |
      | BM         | SLR2       | 7.15           | 7.13           |
      | BM         | SLR1       | 7.15           | 7.11           |
      | BM         | SLR2       | 7.15           | 7.11           |

  @SC-FT-04-01 @FirmwareTest
  Scenario: SC-FT-04-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | 02100203       | NA             |
      | TH         | SLT3       | NA             | 02140205       |
      | BM         | SLR1       | 07114640       | NA             |
      | TH         | SLT3       | 02130204       | NA             |
      | BM         | SLR2       | 07114640       | NA             |
      | TH         | SLT3       | NA             | 02140205       |
      | SB         | SLB1       | 01065120       | NA             |
      | TH         | SLT3       | 02030202       | NA             |
      | SP         | SLP2       | 02055120       | NA             |
      | TH         | SLT3       | NA             | 02140205       |
      | TH         | SLT2       | 05115300       | NA             |
      | HB         | NANO2      | 1.0.0-4380-0.0 | NA             |
      | BM         | SLR1       | NA             | 07154640       |
      | BM         | SLR2       | NA             | 07154640       |
      | SB         | SLB1       | NA             | 01085120       |
      | SP         | SLP2       | NA             | 02085120       |
      | TH         | SLT2       | NA             | 05135300       |
      | HB         | NANO2      | NA             | 1.0.0-4563-0.0 |

  @SC-FT-04-03 @FirmwareTest
  Scenario: SC-FT-04-03_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO1      | 1.0.0-4708-0.0 | NA             |
      | HB         | NANO1      | NA             | 1.0.0-4769-0.0 |

  @SC-FT-04-03-Hubregrade @FirmwareTest
  Scenario: SC-FT-04-03_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO2      | 1.0.0-4563-0.0 | NA             |
      | HB         | NANO2      | NA             | 1.0.0-4822-0.0 |

  @SC-FT-04-02 @FirmwareTest
  Scenario: SC-FT-04-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR1       | 07114640       | NA             |
      | TH         | SLT2       | 05105300       | NA             |
      | HB         | NANO1      | 05105300       | NA             |
      | BM         | SLR1       | NA             | 07154640       |
      | TH         | SLT2       | NA             | 05135300       |
      | HB         | NANO2      | NA             | 05135300       |

  @SC-FT-04-05 @FirmwareTest
  Scenario: SC-FT-04-01_05_Downgrade firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | 02150303       | NA             |
      | TH         | SLT3       | NA             | 03110402      |

  @SC-FT-05 @FirmwareTest @RPI2 @RPI4
  Scenario: SC-FT-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR2       | NA             | 8.00           |
      | TH         | SLT3       | NA             | 2.15           |
      | SB         | SLB1       | NA             | 1.09           |
      | SP         | SLP2       | NA             | 2.09           |
      | BM         | SLR2       | 7.15           | NA             |
      | TH         | SLT3       | 2.13           | NA             |
      | SB         | SLB1       | 1.08           | NA             |
      | SP         | SLP2       | 2.08           | NA             |

  @SC-FT-05-01 @FirmwareTest @RPI2_SB_SP
  Scenario: SC-FT-05-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | 1.08           | NA             |
      | SP         | SLP2       | 2.08           | NA             |
      | SB         | SLB1       | NA             | 1.09           |
      | SP         | SLP2       | NA             | 2.09           |

  @SC-FT-05-02 @FirmwareTest @RPI2_SB_SP
  Scenario: SC-FT-05-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | 2.09           | NA             |
      | SP         | SLP2       | NA             | 2.11           |

  @SC-FT-06 @FirmwareTest @RPI3
  Scenario: SC-FT-06_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR2       | NA             | 8.00           |
      | TH         | SLT3       | NA             | 2.15           |
      | BM         | SLR2       | 7.15           | NA             |
      | TH         | SLT3       | 2.13           | NA             |
      | BM         | SLR2       | NA             | 8.00           |
      | TH         | SLT3       | NA             | 2.15           |
      | BM         | SLR2       | NA             | 7.14           |
      | TH         | SLT3       | NA             | 2.14           |

  @SAN-FT-01 @FirmwareTest
  Scenario: SAN-FT-01_Upgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO1      | NA             | 1.0.0-4615-0.0 |
      | HB         | NANO1      | 1.0.0-4332-0.0 | NA             |

  @SC-FT-04-06 @FirmwareTest
  Scenario: SC-FT-04-06_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR2       | 07114640       | NA             |
      | BM         | SLR2       | 07114640       | NA             |
      | BM         | SLR2       | 07114640       | NA             |
      | BM         | SLR2       | 07114640       | NA             |
      | BM         | SLR2       | 07114640       | NA             |

  @SC-FT-04-07 @FirmwareTest
  Scenario: SC-FT-04-07_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT2       | NA             | 05155300       |
      | TH         | SLT2       | 05135300       | NA             |

  @SC-FT-04-08 @FirmwareTest @Hub @RPI8
  Scenario: SC-FT-04-08_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | 01085120       | NA             |
      | SP         | SLP2       | 02095120       | NA             |
      | SB         | SLB1       | NA             | 01095120       |
      | SP         | SLP2       | NA             | 02115120       |

  @SC-FT-04-09 @FirmwareTest
  Scenario: SC-FT-04-09_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 02150206       |
      | BM         | SLR2       | NA             | 08154640       |
      | HB         | SLT3       | 02140206       | NA             |
      | BM         | SLR2       | 07154640       | NA             |
      | HB         | SLT3       | 02130206       | NA             |
      | BM         | SLR2       | 07134640       | NA             |

  @SC-FT-04-10 @FirmwareTest
  Scenario: SC-FT-04-10_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 02150206       |
      | BM         | SLR1       | NA             | 08004640       |
      | HB         | SLT3       | 02140205       | NA             |
      | BM         | SLR1       | 07154640       | NA             |
      | HB         | SLT3       | 02130204       | NA             |
      | BM         | SLR1       | 07134640       | NA             |

  @SC-FT-04-11 @FirmwareTest
  Scenario: SC-FT-04-11_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 02150206       |
      | HB         | SLT3       | 02140205       | NA             |
      | HB         | SLT3       | 02130204       | NA             |
      | TH         | SLT3       | NA             | 02150206       |
      | HB         | SLT3       | 02130204       | NA             |
      | HB         | SLT3       | 02140205       | NA             |

  @SC-FT-04-12 @FirmwareTest
  Scenario: SC-FT-04-12_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 02150206       |
      | BM         | SLR2       | NA             | 08004640       |
      | SB         | SLB1       | NA             | 01095120       |
      | SP         | SLP2       | NA             | 02095120       |
      | TH         | SLT3       | 02130204       | NA             |
      | BM         | SLR2       | 07154640       | NA             |
      | SB         | SLB1       | 01085120       | NA             |
      | SP         | SLP2       | 02085120       | NA             |

  @SC-FT-02-02 @FirmwareTest
  Scenario: SC-FT-02-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT2       | NA             | 5.15           |
      | TH         | SLT2       | 5.13           | NA             |

  @SC-FT-02-03 @FirmwareTest
  Scenario: SC-FT-02-03_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 2.15           |
      | TH         | SLT3       | 3.11           | NA             |

  @SC-FT-02-03-01 @FirmwareTest
  Scenario: SC-FT-02-03-01_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 2.13           |
      | TH         | SLT3       | 2.10           | NA             |

  @SC-FT-02-03-908 @FirmwareTest
  Scenario: SC-FT-02-03-908_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 9.08           |
      | TH         | SLT3       | 2.13           | NA             |

  @SC-FT-02-03-909 @FirmwareTest
  Scenario: SC-FT-02-03-909_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | NA             | 9.09           |
      | TH         | SLT3       | 2.15           | NA             |

  @SC-FT-04-13 @FirmwareTest
  Scenario: SC-FT-04-13_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | CS         | WDS00140002 | NA             | 30585010       |
      | CS         | WDS00140002 | 30425010       | NA             |
      | MS         | PIR00140005 | NA             | 30585010       |
      | MS         | PIR00140005 | 30425010       | NA             |

  @SC-FT-04-14 @FirmwareTest
  Scenario: SC-FT-04-14 firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 00074710       |
      | CB         | CL01       | 00054710       | NA             |

  @SC-FT-04-15 @FirmwareTest
  Scenario: SC-FT-04-15_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR2        | 07154640       | NA             |
      | SB         | SLB1        | 01085120       | NA             |
      | SP         | SLP2        | 02095120       | NA             |
      | TH         | SLT3        | 02130204       | NA             |
      | CS         | WDS00140002 | 30425010       | NA             |
      | MS         | PIR00140005 | 30425010       | NA             |
      | BM         | SLR2        | NA             | 08004640       |
      | SB         | SLB1        | NA             | 01095120       |
      | SP         | SLP2        | NA             | 02115120       |
      | TH         | SLT3        | NA             | 02150206       |
      | CS         | WDS00140002 | NA             | 30585010       |
      | MS         | PIR00140005 | NA             | 30585010       |

  @SC-FT-04-16 @FirmwareTest
  Scenario: SC-FT-04-16_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO2      | 1.0.0-4563-0.0 | NA             |
      | BM         | SLR2       | 7.13           | NA             |
      | SB         | SLB1       | 1.08           | NA             |
      | SP         | SLP2       | 2.08           | NA             |
      | TH         | SLT3       | 2.10           | NA             |
      | HB         | NANO2      | NA             | 1.0.0-4782-0.0 |
      | BM         | SLR2       | NA             | 7.15           |
      | SB         | SLB1       | NA             | 1.09           |
      | SP         | SLP2       | NA             | 2.09           |
      | TH         | SLT3       | NA             | 2.13           |

  @SC-FT-04-17 @FirmwareTest
  Scenario: SC-FT-04-17_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO2      | 1.0.0-4563-0.0 | NA             |
      | CB         | CL01       | NA             | 00074710       |
      | CB         | CL01       | 00054710       | NA             |
      | HB         | NANO2      | NA             | 1.0.0-4822-0.0 |
      | CB         | CL01       | NA             | 00074710       |
      | CB         | CL01       | 00054710       | NA             |

  @SC-FT-04-18 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-18_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | 02095120       | NA             |
      | SP         | SLP2       | NA             | 02145120       |

  @SC-FT-02-08 @FirmwareTest
  Scenario: SC-FT-02-08_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBulb01   | NA             | 11.10          |
      | AL         | FWBulb01   | 11.0f          | NA             |

  @SC-FT-04-19 @FirmwareTest
  Scenario: SC-FT-04-19_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | 01095120       | NA             |
      | SB         | SLB1       | NA             | 01125120       |

  @SC-FT-04-20 @FirmwareTest
  Scenario: SC-FT-04-20_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | NA             | 01115120       |
      | SB         | SLB1       | 01105120       | NA             |

  @SC-FT-04-20b @FirmwareTest
  Scenario: SC-FT-04-20b_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1b      | NA             | 0003700        |
      | SB         | SLB1b      | 0909700        | NA             |

  @SC-FT-04-21 @FirmwareTest
  Scenario: SC-FT-04-21_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HB         | NANO2      | NA             | 1.0.0-4822-0.0 |
      | SB         | SLB1       | NA             | 01105120       |
      | SB         | SLB1       | 01095120       | NA             |
      | HB         | NANO2      | 1.0.0-4563-0.0 | NA             |
      | SB         | SLB1       | NA             | 01105120       |
      | SB         | SLB1       | 01095120       | NA             |

  @SC-FT-05-02 @FirmwareTest @RPI2_SB_SP
  Scenario: SC-FT-05-02_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | NA             | 1.10           |
      | SB         | SLB1       | 1.09           | NA             |

  @SC-FT-04-22 @FirmwareTest
  Scenario: SC-FT-04-22_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | CS         | WDS00140002 | 30585010       | NA             |
      | MS         | PIR00140005 | 30585010       | NA             |
      | CS         | WDS00140002 | NA             | 31005010       |
      | MS         | PIR00140005 | NA             | 31005010       |

  @SC-FT-04-23 @FirmwareTest
  Scenario: SC-FT-04-23_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | CS         | WDS00140002 | NA             | 31005010       |
      | CS         | WDS00140002 | 30585010       | NA             |

  @SC-FT-04-24 @FirmwareTest
  Scenario: SC-FT-04-24_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBulb01   | NA             | 11250002       |
      | AL         | FWBulb01   | 11190002       | NA             |

  @SC-FT-02-09 @FirmwareTest
  Scenario: SC-FT-02-09_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBulb01   | NA             | 11.14          |
      | AL         | FWBulb01   | 11.13          | NA             |

  @SC-FT-02-10 @FirmwareTest
  Scenario: SC-FT-02-10_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | HA         | SLB3       | NA             | 2.09           |
      | HA         | SLB3       | 2.07           | NA             |

  @SC-FT-04-25 @FirmwareTest
  Scenario: SC-FT-04-24_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01US | NA             | 11150002       |
      | AL         | TWBulb01US | 11110002       | NA             |

  @SC-FT-02-26 @FirmwareTest
  Scenario: SC-FT-02-26_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01US | NA             | 11.11          |
      | AL         | TWBulb01US | 11.15          | NA             |

  @SC-FT-04-27 @FirmwareTest
  Scenario: SC-FT-04-27_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01US | NA             | 11160002       |
      | AL         | RGBBulb01US | 11090002       | NA             |

  @SC-FT-04-28 @FirmwareTest
  Scenario: SC-FT-04-28_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB3       | NA             | 2.08           |
      | SB         | SLB3       | 2.09           | NA             |

  @SC-FT-04-29 @FirmwareTest
  Scenario: SC-FT-04-29_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT4       | NA             | 1.07           |
      | TH         | SLT4       | 1.06           | NA             |

  @SC-FT-04-30 @FirmwareTest
  Scenario: SC-FT-04-30_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01UK | NA             | 11200002       |
      | AL         | RGBBulb01UK | 11140002       | NA             |

  @SC-FT-31 @FirmwareTest
  Scenario: SC-FT-31_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT4       | 1.14           | 1.15           |


  @SC-FT-04-32 @FirmwareTest
  Scenario: SC-FT-04-32_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR2B      | NA             | 00095700       |
      | BM         | SLR2B      | 00065700       | NA             |


  @SC-FT-33 @FirmwareTest
  Scenario: SC-FT-33_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3b      | 9.09           | NA             |
      | TH         | SLT3b      | NA             | 1.010          |

  @SC-FT-34 @FirmwareTest
  Scenario: SC-FT-34_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3       | 2.13           | NA             |
      | TH         | SLT3       | NA             | 2.15           |


  @SC-FT-04-35 @FirmwareTest
  Scenario: SC-FT-04-35_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3b      | NA             | 04090208       |
      | TH         | SLT3b      | 04080206       | NA             |

  @SC-FT-04-36 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-36_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | 02155120       | NA             |
      | SP         | SLP2       | NA             | 03005120       |

  @SC-FT-37 @FirmwareTest
  Scenario: SC-FT-37_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3b      | 0113           | NA             |
      | TH         | SLT3b      | NA             | 0406           |

  @SC-FT-38 @FirmwareTest
  Scenario: SC-FT-38_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The Hive product is paired and setup for Central Heating with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT3b      | 01130110       | NA             |
      | TH         | SLT3b      | NA             | 04060204       |

  @SC-FT-39 @FirmwareTest
  Scenario: SC-FT-39_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | BM         | SLR1b      | 1.05           | NA             |
      | BM         | SLR1b      | NA             | 0.95           |


  @SC-FT-40 @FirmwareTest
  Scenario: SC-FT-40_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2c      | 3.00           | NA             |
      | SP         | SLP2c      | NA             | 3.01           |

  @SC-FT-41 @FirmwareTest
  Scenario: SC-FT-41_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01UK | 11200002       | NA             |
      | AL         | RGBBulb01UK | NA             | 11140002       |

  @SC-FT-67 @FirmwareTest
  Scenario: SC-FT-67_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2      | 3.00           | NA             |
      | SP         | SLP2      | NA             | 3.01           |

     @SC-FT-68 @FirmwareTest
  Scenario: SC-FT-68_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2b      | 3.00           | NA             |
      | SP         | SLP2b      | NA             | 3.01           |

   @SC-FT-04-37 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-37_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2b       | 02155120       | NA             |
      | SP         | SLP2b       | NA             | 03005120       |

     @SC-FT-69 @FirmwareTest
  Scenario: SC-FT-69_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2c      | 3.00           | NA             |
      | SP         | SLP2c      | NA             | 3.01           |

   @SC-FT-04-38 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-38_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2c       | 02155120       | NA             |
      | SP         | SLP2c       | NA             | 03005120       |

      @SC-FT-70 @FirmwareTest
  Scenario: SC-FT-70_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2d      | 3.00           | NA             |
      | SP         | SLP2d      | NA             | 3.01           |

   @SC-FT-04-39 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-39_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2d       | 02155120       | NA             |
      | SP         | SLP2d       | NA             | 03005120       |

  @SC-FT-04-40 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-40_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWGU10Bulb01UK       | 02155120       | NA             |
      | AL         | FWGU10Bulb01UK       | NA             | 03005120       |

     @SC-FT-04-41 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-41_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBulb01US       | 02155120       | NA             |
      | AL         | FWBulb01US       | NA             | 03005120       |

    @SC-FT-04-42 @FirmwareTest @RPI7_SP
  Scenario: SC-FT-04-42_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWPAR38Bulb01US       | 02155120       | NA             |
      | AL         | FWPAR38Bulb01US       | NA             | 03005120       |

   @SC-FT-04-43 @FirmwareTest
  Scenario: SC-FT-04-43_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01UK | NA             | 11150002       |
      | AL         | TWBulb01UK | 11110002       | NA             |

  @SC-FT-04-44 @FirmwareTest
  Scenario: SC-FT-04-44_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB2 | NA             | 11150002       |
      | SB         | SLB2 | 11110002       | NA             |

  @SC-FT-04-45 @FirmwareTest
  Scenario: SC-FT-04-45_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB2c | NA             | 11150002       |
      | SB         | SLB2c | 11110002       | NA             |

   @SC-FT-04-46 @FirmwareTest
  Scenario: SC-FT-04-46_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB3 | NA             | 11150002       |
      | SB         | SLB3 | 11110002       | NA             |

  @SC-FT-04-47 @FirmwareTest
  Scenario: SC-FT-04-47_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB4 | NA             | 11150002       |
      | SB         | SLB4 | 11110002       | NA             |

  @SC-FT-04-48 @FirmwareTest
  Scenario: SC-FT-04-48_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | MS         | PIR00140005 | NA             | 11150002       |
      | MS         | PIR00140005 | 11110002       | NA             |

    @SC-FT-04-49 @FirmwareTest
  Scenario: SC-FT-04-49_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | MS         | MOT003 | NA             | 11150002       |
      | MS         | MOT003 | 11110002       | NA             |

  @SC-FT-04-50 @FirmwareTest
  Scenario: SC-FT-04-50_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | MS         | DWS003 | NA             | 03992603       |
      | MS         | DWS003 | 04002603       | NA             |

    @SC-FT-04-51 @FirmwareTest
  Scenario: SC-FT-04-51_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | MS         | MOT003 | NA             | 03992603       |
      | MS         | MOT003 | 04002603       | NA             |


  @SC-FT-04-52 @FirmwareTest
  Scenario: SC-FT-04-52_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB3 | NA             | 11150002       |
      | SB         | SLB3 | 11110002       | NA             |


      @SC-FT-04-53 @FirmwareTest
  Scenario: SC-FT-04-53_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWCLBulb01UK | NA             | 11040002       |
      | AL         | TWCLBulb01UK | 11050002       | NA             |


     @SC-FT-04-54 @FirmwareTest
  Scenario: SC-FT-04-54_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices infinitely
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWCLBulb01UK | NA             | 11060002       |
      | AL         | FWCLBulb01UK | 11070002       | NA             |

