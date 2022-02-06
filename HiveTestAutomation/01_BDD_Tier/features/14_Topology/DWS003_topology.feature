# Created by kingston.samselwyn at 09/12/2016
Feature: Consists of scenario that validates the network topology between devices
	
  @SC-TT-SC01-28 @PairingTest
  Scenario Outline: SC-TT-SC01-28_The given devices are paired and unpaired sequentially and validated via plug
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
	  | TGStick  | SLP2 	|
	  | SLP2 	 | TWBulb01UK     |
	  | TWBulb01UK 	 | DWS003     |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01UK       | NA             | 02164710       |
      | AL         | TWBulb01UK       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLP2_1   |
	  | SB         | DWS003_1   |
	
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
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLP2_1   |
	  | SB         | DWS003_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | TWBulb01UK 	|
	  | TWBulb01UK 	 | SLP2     |
	  | SLP2 	 | DWS003     |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | NA             | 01155120       |
      | SP         | SLP2       | 01125120       | NA             |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |


  Examples:
	| BULB_PLUG_MAC |PLUG_PLUG_MAC|HUB_PLUG_MAC|BOOSTER_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|000D6F000E2CB423|

	  
  @SC-TT-SC01-29 @PairingTest
  Scenario Outline: SC-TT-SC01-29_The given devices are paired and unpaired sequentially and validated via plug
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
	  | TGStick  | SLP2c 	|
	  | SLP2c 	 | RGBBulb01UK     |
	  | RGBBulb01UK 	 | DWS003     |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | RGBBulb01UK       | NA             | 02164710       |
      | AL         | RGBBulb01UK       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | RGBBulb01UK_1   |
	  | SP         | SLP2c_1   |
	  | SB         | DWS003_1   |
	
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
	  | AL         | RGBBulb01UK_1   |
	  | SP         | SLP2c_1   |
	  | SB         | DWS003_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | RGBBulb01UK 	|
	  | RGBBulb01UK 	 | SLP2c     |
	  | SLP2c 	 | DWS003     |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2c      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2c       | NA             | 01155120       |
      | SP         | SLP2c       | 01125120       | NA             |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|RGBBulb01UK      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|RGBBulb01UK      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |


  Examples:
	| BULB_PLUG_MAC |PLUG_PLUG_MAC|HUB_PLUG_MAC|BOOSTER_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|000D6F000E2CB423|

	  
  @SC-TT-SC01-30 @PairingTest
  Scenario Outline: SC-TT-SC01-30_The given devices are paired and unpaired sequentially and validated via plug
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
	  | SLB1 	 | TWBulb01UK     |
	  | TWBulb01UK 	 | DWS003     |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | TWBulb01UK       | NA             | 02164710       |
      | AL         | TWBulb01UK       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLB1_1   |
	  | SB         | DWS003_1   |
	
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
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLB1_1   |
	  | SB         | DWS003_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | TWBulb01UK 	|
	  | TWBulb01UK 	 | SLB1     |
	  | SLB1 	 | DWS003     |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLB1       | NA             | 01155120       |
      | SP         | SLB1       | 01125120       | NA             |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |


  Examples:
	| BULB_PLUG_MAC |PLUG_PLUG_MAC|HUB_PLUG_MAC|BOOSTER_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|000D6F000E2CB423|

	    
  @SC-TT-SC01-31 @PairingTest
  Scenario Outline: SC-TT-SC01-31_The given devices are paired and unpaired sequentially and validated via plug
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
	  | TGStick  | SLB3 	|
	  | SLB3 	 | FWBulb01     |
	  | FWBulb01 	 | DWS003     |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | AL         | FWBulb01       | NA             | 02164710       |
      | AL         | FWBulb01       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | FWBulb01_1   |
	  | SP         | SLB3_1   |
	  | SB         | DWS003_1   |
	
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
	  | AL         | FWBulb01_1   |
	  | SP         | SLB3_1   |
	  | SB         | DWS003_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | FWBulb01 	|
	  | FWBulb01 	 | SLB3     |
	  | SLB3 	 | DWS003     |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <HUB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|NANO2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB3      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLB3       | NA             | 01155120       |
      | SP         | SLB3       | 01125120       | NA             |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|FWBulb01      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|FWBulb01      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|DWS003      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|DWS003      |


  Examples:
	| BULB_PLUG_MAC |PLUG_PLUG_MAC|HUB_PLUG_MAC|BOOSTER_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|000D6F000E2CB423|
