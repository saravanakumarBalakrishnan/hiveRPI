# Created by kingston.samselwyn at 09/12/2016
Feature: Consists of scenario that validates the network topology between devices
	
  @SC-TT-SC01-15 @PairingTest
  Scenario Outline: SC-TT-SC01-15_The given devices are paired and unpaired sequentially and validated via plug
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
	  | TWBulb01UK 	 | SLB1     |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	Then change the state of the plug with mac address <BULB_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
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
	|SLB1      |
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
	|SLB1      |
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
      | AL         | TWBulb01UK       | NA             | 02164710       |
      | AL         | TWBulb01UK       | 02154710       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLP2_1   |
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
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLP2_1   |
	  | SB         | SLB1_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | TWBulb01UK 	|
	  | TWBulb01UK 	 | SLP2     |
	  | SLP2 	 | SLB1     |
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
	|SLB1      |
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
	|SLB1      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	Then change the state of the plug with mac address <PLUG_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
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
	|SLB1      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SB         | SLB1       | NA             | 01155120       |
      | SB         | SLB1       | 01125120       | NA             |
	Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | AL         | TWBulb01UK_1   |
	  | SP         | SLB1_1   |
	  | BM         | SLP2_1   |
	
	And the given attenuation is set on the network
	  | Atten | DB |
	  | 1_2   | 90  |
	  | 2_3   | 90  |
	  | 2_4   | 0 |
	  | 1_3   | 90 |
	  | 3_4   | 0  |
	  | 1_4   | 0 |
	Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SB         | SLB1   |
	  | SP         | SLP2_1   |
	  | AL         | TWBulb01UK_1   |
	When the given topology is formed and verified
	  | Parent   | Child    |
	  | COO      | SLB1 	|
	  | SLB1 	 | TWBulb01UK     |
	  | SLB1 	 | SLP2     |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to OFF via telegesis
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Absent
	|DeviceType|
	|SLP2      |
	Then change the state of the plug with mac address <BOOSTER_PLUG_MAC> to ON via telegesis
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLB1      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|TWBulb01UK      |
	And validate the time taken for the devices presence to go Present
	|DeviceType|
	|SLP2      |
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2       | NA             | 01155120       |
      | SP         | SLP2       | 01125120       | NA             |
  Examples:
	| BULB_PLUG_MAC |PLUG_PLUG_MAC|HUB_PLUG_MAC|BOOSTER_PLUG_MAC|
    | 001E5E09021D4734|001E5E09021223FA|000D6F000E2CB423|000D6F000E2CB423|
