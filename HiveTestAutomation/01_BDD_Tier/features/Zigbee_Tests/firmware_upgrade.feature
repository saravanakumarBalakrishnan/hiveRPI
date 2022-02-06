Feature: This feature comprises of scenarios that test the firmware upgrade and downgrade
	
	  
	@SC-FT-43 @FirmwareTest
  Scenario: SC-FT-43_Downgrade firmware of the device and later upgrade the firmware to the previous version
	Given The telegesis is paired with given devices
	When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 infinitely and validated via Telegisis
	  | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
	  | SP         | SLP2b      | 0.04           | NA             |
	  | SP         | SLP2b      | NA             | 9.09           |
