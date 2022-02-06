Feature: Consists of scenario that validates the network between devices

  @SC-NT-JN01-01 @PairingTest @testing
  Scenario: SC-NT-JN01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2b      | 001E5E09022C1A25 |
   
@SC-NT-JN01-03 @PairingTest
  Scenario: SC-NT-JN01-03_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated infinitely via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2       | 00158D00012E4C02 |
      
    @SC-GT-SC01-01 @Generic
  Scenario: SC-GT-SC01-01_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2    | 000D6F000AE154DF |

  @SC-GT-SC01-02 @Generic
  Scenario: SC-GT-SC01-02_The given devices are paired and unpaired sequentially and validated
    Given The telegesis is paired with given devices
    When the below devices are paired and unpaired sequentially and validated 2 times via Telegesis
      | DeviceName | DeviceType | MacID            |
      | SP         | SLP2    | 000D6F000B99FC75 |

  @SC-GT-SC03-01 @Generic @SPONFF
  Scenario: SC-GT-SC03-01_The smart plug state is changed and validated the using zigbee attribute and repeated infinitely.
    Given The telegesis is paired with given devices
    When the smartplug state is changed to below states and validated using the zigbee attribute and repeated infinitely
      | DeviceName | DeviceType | State | MacID            |
      | SP         | SLP2    | ON    | 001E5E090217155F |
      | SP         | SLP2    | OFF   | 001E5E090217155F |
