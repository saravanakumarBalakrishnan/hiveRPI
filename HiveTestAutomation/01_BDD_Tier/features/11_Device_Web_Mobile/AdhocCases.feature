Feature: This feature comprises of scenarios that do the adhoc test not included in regression.

  @SC-AD-01 @FirmwareTest
  Scenario Outline: SC-AD-01_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | RGBBulb01UK | NA             | 11200002       | False  |
      | AL         | RGBBulb01UK | 11140002       | NA             | False  |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |


  @SC-AD-02 @FirmwareTest
  Scenario: SC-AD-02_Downgrade firmware of the device and later upgrade the firmware to the previous version
    Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | BM         | SLR2       | NA             | 08054640       | True   |
      | BM         | SLR2       | 08074640       | NA             | True   |


  @SC-AD-03 @FirmwareTest @ZigbeeDumpTest
  Scenario Outline: SC-AD-03_Downgrade firmware of the device and later upgrade the firmware to the previous version and take Zigbee dump subsequently
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType  |
      | RGBBulb01UK |
    Examples:
      | DeviceType  |
      | RGBBulb01UK |
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01UK | NA             | 11200002       |
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType  |
      | RGBBulb01UK |
    Examples:
      | DeviceType  |
      | RGBBulb01UK |

  @SC-AD-04 @FirmwareTest
  Scenario Outline: SC-AD-04_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2  with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType  | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | RGBBulb01UK | NA             | 11200002       | False  |
      | AL         | RGBBulb01UK | 11140002       | NA             | False  |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |


  @SC-AD-05 @FirmwareTest
  Scenario Outline: SC-AD-05_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SP         | SLP2       | NA             | 11200002       | True   |
      | SP         | SLP2       | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-06 @FirmwareTest
  Scenario Outline: SC-AD-06_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SP         | SLP2b      | NA             | 11200002       | True   |
      | SP         | SLP2b      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

    @SC-AD-07 @FirmwareTest
  Scenario Outline: SC-AD-07_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SP         | SLP2c      | NA             | 11200002       | True   |
      | SP         | SLP2c      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

    @SC-AD-08 @FirmwareTest
  Scenario Outline: SC-AD-08_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SP         | SLP2d      | NA             | 11200002       | True   |
      | SP         | SLP2d      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

    @SC-AD-09 @FirmwareTest
  Scenario Outline: SC-AD-09_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | FWBulb01      | NA             | 11200002       | True   |
      | AL         | FWBulb01      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-10 @FirmwareTest
  Scenario Outline: SC-AD-10_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | FWGU10Bulb01UK      | NA             | 11200002       | True   |
      | AL         | FWGU10Bulb01UK      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-11 @FirmwareTest
  Scenario Outline: SC-AD-11_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | FWBulb01US      | NA             | 11200002       | True   |
      | AL         | FWBulb01US      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

   @SC-AD-12 @FirmwareTest
  Scenario Outline: SC-AD-12_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | FWPAR38Bulb01US      | NA             | 11200002       | True   |
      | AL         | FWPAR38Bulb01US      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-13 @FirmwareTest
  Scenario Outline: SC-AD-13_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | TWBulb01UK      | NA             | 11200002       | True   |
      | AL         | TWBulb01UK      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-14 @FirmwareTest
  Scenario Outline: SC-AD-14_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | TWBulb01US      | NA             | 11200002       | True   |
      | AL         | TWBulb01US      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-15 @FirmwareTest
  Scenario Outline: SC-AD-15_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | RGBBulb01UK      | NA             | 11200002       | True   |
      | AL         | RGBBulb01UK      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

   @SC-AD-16 @FirmwareTest
  Scenario Outline: SC-AD-16_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | RGBBulb01US      | NA             | 11200002       | True   |
      | AL         | RGBBulb01US      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

 @SC-AD-17 @FirmwareTest
  Scenario Outline: SC-AD-17_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB1      | NA             | 11200002       | True   |
      | SB         | SLB1      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-18 @FirmwareTest
  Scenario Outline: SC-AD-18_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB2      | NA             | 11200002       | True   |
      | SB         | SLB2      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-19 @FirmwareTest
  Scenario Outline: SC-AD-19_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB2c      | NA             | 11200002       | True   |
      | SB         | SLB2c      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-20 @FirmwareTest
  Scenario Outline: SC-AD-20_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB3      | NA             | 11200002       | True   |
      | SB         | SLB3      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-21 @FirmwareTest
  Scenario Outline: SC-AD-21_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB4      | NA             | 11200002       | True   |
      | SB         | SLB4      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

    @SC-AD-21 @FirmwareTest
  Scenario Outline: SC-AD-21_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | SB         | SLB4      | NA             | 11200002       | True   |
      | SB         | SLB4      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-22 @FirmwareTest
  Scenario Outline: SC-AD-22_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | MS         | PIR00140005      | NA             | 11200002       | True   |
      | MS         | PIR00140005      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-23 @FirmwareTest
  Scenario Outline: SC-AD-23_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | MS         | MOT003      | NA             | 11200002       | True   |
      | MS         | MOT003      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |


  @SC-AD-24 @FirmwareTest
  Scenario Outline: SC-AD-24_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | CS         | WDS00140002      | NA             | 11200002       | True   |
      | CS         | WDS00140002      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

  @SC-AD-25 @FirmwareTest
  Scenario Outline: SC-AD-25_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | CS         | DWS003      | NA             | 11200002       | True   |
      | CS         | DWS003      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |


  @SC-AD-26 @FirmwareTest
  Scenario Outline: SC-AD-26_Downgrade firmware of the device and later upgrade the firmware to the previous version with reboot in each 10min,other than(BM and TH) plug it on smartPlug (PLUG or NOPLUG)Given The telegesis is paired with given devices
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely with reboot and validated via Telegisis <PlugMacID>
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 | Reboot |
      | AL         | TWGU10Bulb01UK      | NA             | 11200002       | True   |
      | AL         | TWGU10Bulb01UK      | 11140002       | NA             | True   |


    Examples:
      | PlugMacID        |
      | 001E5E0902120F1B |

   @SC-AD-27 @VoltageTst
    Scenario Outline: SC-TH-UIMC-135_Check Voltage after stat reboot
    Given The telegesis is paired with given heating devices
    #HOLIDAY MODE
    When the <DeviceType> is rebooted after <min> min
    Then validate by reading attribute
    Examples:
      | DeviceType | min |
      | SLT3b      | 4   |
