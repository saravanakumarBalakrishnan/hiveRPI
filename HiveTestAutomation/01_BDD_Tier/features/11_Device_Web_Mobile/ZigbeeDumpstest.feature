Feature: This feature file contains scenarios to validate the Zigbee cluster and attributes with the baseline dump.

  @SC-ZT-01 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-01_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLT2       |

    Examples:
      | DeviceType |
      | SLT2       |

  @SC-ZT-02 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-02_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLR1B      |

    Examples:
      | DeviceType |
      | SLR1B      |

  @SC-ZT-05 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-05_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType  |
      | RGBBulb01UK |

    Examples:
      | DeviceType  |
      | RGBBulb01UK |

  @SC-ZT-06 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-06_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
      | DeviceType | MACID            |
      | SLT3       | 001E5E09020C2A29 |
    Then the dump is validated against the corresponding baseline dump file.

    Examples:
      | DeviceType |
      | SLT3       |

  @SC-ZT-07 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-07_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLT3b      |

    Examples:
      | DeviceType |
      | SLP2       |

  @SC-ZT-08 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-08_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | TWBulb01US |

    Examples:
      | DeviceType |
      | TWBulb01US |

  @SC-ZT-09 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-09_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType |
      | SLT4       |

    Examples:
      | DeviceType |
      | SLT4       |


  @SC-ZT-10 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-10_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType     |
      | FWGU10Bulb01UK |

    Examples:
      | DeviceType     |
      | FWGU10Bulb01UK |
    
    
    @SC-ZT-101 @ZigbeeDumpTest
  Scenario Outline: SC-ZT-101_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
    Given The telegesis is paired with given devices
    When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
    Then the dump is validated against the corresponding baseline dump file.
      | DeviceType     |
      | FWPAR38Bulb01US |

    Examples:
      | DeviceType     |
      | FWPAR38Bulb01US |




