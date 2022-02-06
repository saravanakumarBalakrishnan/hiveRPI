# Created by Kingston

Feature: Performs regression on Smart Plug for the Device type SLP2

  #Pairing & Unpairing in same Channel
  #Device ON\OFF Test
  #Device ON\OFF Schedule test
  #OTA firmware upgrade\downgrade Test
  #Device Offline Test

  @SC-NT-JN04-02 @Regression_API_SLP2_Test
  Scenario: SC-NT-JN04-02_The given devices are paired and unpaired sequentially and validated
    Given The Smart Plugs are paired with the Hive Hub
    Then the below devices are unpaired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2_1   |
    Then the below devices are paired via NANO2 Hub
	  | DeviceName | DeviceType |
	  | SP         | SLP2_1   |

  @SC-SP-OO-02 @Regression_API_SLP2_Test
  Scenario: SC-SP-OO-02_Switch Plug to ON and OFF state and validate the same
	Given The Hive product is paired and setup for PLUG
	When The SLP2_1 is switched ON and validated via Hub
    Then Automatically validate current state as ON while in Manual mode
	When The SLP2_1 is switched OFF and validated via Hub
    Then Automatically validate current state as OFF while in Manual mode

  @SC-SP-SH12-03 @Regression_API_SLP2_Test
  Scenario Outline: SC-SP-SH12-03_Set the given default 'six' event schedule for the given day and verify the same for Smart Plug
    Given The Smart Plugs are paired with the Hive Hub
    When The below <Device> schedule is set for <Day> via Hub
      | Start Time | SmartPlug State |
      | 06:30      | ON              |
      | 08:30      | OFF             |
      | 12:00      | OFF             |
      | 14:00      | OFF             |
      | 16:00      | ON              |
      | 21:30      | OFF             |
    Then Verify if the Schedule is set

    Examples:
      |Device  | Day   |
      |SLP2_1 | Today |


  @SC-FT-14-38 @Regression_API_SLP2_Test
  Scenario: SC-FT-14-38_Downgrade  firmware of the device and later upgrade the firmware to the previous version for the given list of devices once
    Given The Hive product is paired and setup for upgrades
    When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 and validated via HUB
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | SP         | SLP2      | 03055120       | NA             |
      | SP         | SLP2      | NA             | 03065120       |

    @SC-OFF-RS04
  Scenario: SC-OFF-RS04_Validate the the time taken for devices to come Online after Hub Reboot
    Given The Hive product is paired and setup for PLUG
    When The NANO2_1 Hub is rebooted via API and validate the time taken for the devices to come Online
      | DeviceName | DeviceType |
      | SP         | SLP2       |
