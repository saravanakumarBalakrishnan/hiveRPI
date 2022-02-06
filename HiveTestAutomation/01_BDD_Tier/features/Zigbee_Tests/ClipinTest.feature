# Created by kingston.samselwyn at 14/06/2017
Feature: This file contains the test for Clipin Device
  # Enter feature description here

  @SC-CL-01-01 @FirmwareTest @ClipinTest
  Scenario: SC-FT-01-01 firmware of the device and later upgrade the firmware to the previous version for the given list of devices
    Given The Hive product is paired and setup for upgrades with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 02164710       |
      | CB         | CL01       | 02154710       | NA             |
    
    
  @SC-CL-01-02 @FirmwareTest @ClipinTest
  Scenario Outline: SC-FT-01-02 firmware of the device and later upgrade the firmware to the previous version for the given list of devices
    Given The Hive product is paired and setup for upgrades with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 with <HUB_TYPE> reboot using <HUB_PLUG_MAC> and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 02164710       |
      | CB         | CL01       | 02154710       | NA             |
    
    Examples:
    | HUB_PLUG_MAC | HUB_TYPE|
    | 000D6F000BEF18E5| NANO2|
    
    
  @SC-CL-01-03 @FirmwareTest @ClipinTest
  Scenario Outline: SC-FT-01-03 firmware of the device and later upgrade the firmware to the previous version for the given list of devices
    Given The Hive product is paired and setup for upgrades with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 with device reboot using <CLIPIN_PLUG_MAC> and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 02164710       |
      | CB         | CL01       | 02154710       | NA             |
    
    Examples:
    | CLIPIN_PLUG_MAC |
    | 000D6F000BEF1755|
    
    
    @SC-CL-01-04 @FirmwareTest @ClipinTest
  Scenario Outline: SC-FT-01-04 firmware of the device and later upgrade the firmware to the previous version for the given list of devices
    Given The Hive product is paired and setup for upgrades with API Validation
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 with router reboot using <ROUTER_PLUG_MAC> and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 02164710       |
      | CB         | CL01       | 02154710       | NA             |
    
    Examples:
    | ROUTER_PLUG_MAC |
    | 000D6F000BEF18E5|
      
  @SC-TT-SC01-01 @ToplogyTest @SC-CL-01-05 @ClipinTest
  Scenario Outline: SC-TT-SC01-01_The given devices are paired and unpaired sequentially and validated via booster and clipin
	Given The devices are paired with the Hive Hub
	And the given attenuation is set on the network
	  | Atten | DB |
	  | 1_2   | 0  |
	  | 2_3   | 0  |
	  | 2_4   | 90 |
	  | 1_3   | 90 |
	  | 3_4   | 0  |
	  | 1_4   | 90 |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | TGStick  | SLB1 	|
	  | SLB1 	 | CL01     |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <CLIPIN_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <CLIPIN_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|CL01      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | CB         | CL01       | NA             | 02164710       |
      | CB         | CL01       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CL         | CL01_1   |
	  | SB         | SLB1_1   |
	
	And the given attenuation is set on the network
	  | Atten | DB |
	  | 1_2   | 90  |
	  | 2_3   | 0  |
	  | 2_4   | 90 |
	  | 1_3   | 0 |
	  | 3_4   | 0  |
	  | 1_4   | 90 |
	Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | CL         | CL01_1   |
	  | SB         | SLB1_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | CL01 	|
	  | CL01 	 | SLB1     |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|CL01      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|CL01      |
	
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | NA             | 01155120       |
      | SB         | SLB1       | 01125120       | NA             |
  	
	Then change the state of the plug with mac address <CLIPIN_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|CL01      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	Then change the state of the plug with mac address <CLIPIN_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|CL01      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	
  Examples:
	| BOOSTER_PLUG_MAC |CLIPIN_PLUG_MAC|HUB_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|
	