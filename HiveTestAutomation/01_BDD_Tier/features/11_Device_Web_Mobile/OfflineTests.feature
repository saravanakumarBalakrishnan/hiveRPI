Feature: Consists of scenario that validates the Offline tests

  @SC-OFF-RS01 @OfflineTest
  Scenario: SC-OFF-RS01_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online and repeated infinitely
      | DeviceName | DeviceType |
      | BM         | SLR2       |



  @SC-OFF-RS03 @OfflineTest
  Scenario: SC-OFF-RS03_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLR2       |

  @SC-OFF-RS04 @OfflineTest
  Scenario: SC-OFF-RS04_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | SP         | SLP2       |

  @SC-OFF-RS05 @OfflineTest
  Scenario: SC-OFF-RS05_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLB1       |

  @SC-OFF-RS06 @OfflineTest
  Scenario: SC-OFF-RS06_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLB3       |

  @SC-OFF-RS07 @OfflineTest
  Scenario: SC-OFF-RS07_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLP2C      |

  @SC-OFF-RS08 @OfflineTest
  Scenario: SC-OFF-RS08_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLT3       |

  @SC-OFF-RS09 @OfflineTest
  Scenario: SC-OFF-RS09_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | BM         | SLT4       |

  @SC-OFF-CS10 @OfflineTest
  Scenario: SC-OFF-CS10_Validate the device presence via Hub
    Given The Devices are paired with the Hive Hub
    When The device is untouched and validate the presence status of the devices infinitely
      | DeviceName | DeviceType |
      | SB         | SLB3       |
    
  @SC-OFF-CS11 @OfflineTest
   Scenario: SC-OFF-CS11_Validate the boost is cancelled when the BM is powercycled
    Given The telegesis is paired with given devices
    When Mode is automatically changed to OFF on the Client
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When the plug is powercycled and the latest BM setting is fetched
    Then Automatically validate current mode as OFF with Target Temperature as 1.0
     
  @SC-OFF-CS12 @OfflineTest
   Scenario: SC-OFF-CS12_Validate the boost is cancelled when the BM is powercycled
    Given The telegesis is paired with given devices
    When Mode is automatically changed to AUTO on the Client
    Then Automatically validate current mode as AUTO with Target Temperature as 1.0
    When Mode is automatically changed to BOOST with Target Temperature as 22.0 for a duration of 1 hour on the Client
    Then Automatically validate current mode as BOOST with Target Temperature as 22.0
    When the plug is powercycled and the latest BM setting is fetched
    Then Automatically validate current mode as AUTO

  @SC-OFF-RS11 @OfflineTest
  Scenario: SC-OFF-RS11_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | SP         | SLP2c       |


  @SC-OFF-RS12 @OfflineTest
  Scenario: SC-OFF-RS12_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Devices are paired with the Hive Hub
    When The Hub is rebooted via telegesis and validate the alarm state of device for 30 minutes
      | DeviceName | DeviceType |
      | BM         | SLR1b_1       |

   @SC-OFF-CS10 @OfflineTest
  Scenario: SC-OFF-CS10_Validate the device presence via Hub
    Given The Devices are paired with the Hive Hub
     And the given attenuation is set on the network
	  | Atten | DB |
	  | 1_2   | 0  |
	  | 2_3   | 90 |
	  | 2_4   | 90 |
	  | 1_3   | 90 |
	  | 3_4   | 90 |
	  | 1_4   | 90 |
     Then validate the time taken for the devices to show offline for 60 minutes
     | DeviceName | DeviceType |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     And the given attenuation is set on the network
	  | Atten | DB |
	  | 1_2   | 0  |
	  | 2_3   | 90 |
	  | 2_4   | 90 |
	  | 1_3   | 90 |
	  | 3_4   | 0 |
	  | 1_4   | 90 |
     Then validate the time taken for the devices to show online for 60 minutes
     | DeviceName | DeviceType |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | MOT         | MOT003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |
     | DWS         | DWS003      |