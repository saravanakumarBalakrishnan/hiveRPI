# Created by bharath.gopalan at 02/08/2017
Feature: To validate the end functionality of the SLT4 stat at a zigbee level (HEAT HOLD and COOL HOLD)
  # These cases automate the associated SLT4 related zigbee cases
  #It is mandatory to set the SLT4 to the correct configuration before attempting to run the tests


  @SLT4_RegressionTest @SC-NT-JN05-29 @PairingTest
    Scenario: SC-NT-JN05-29_The given devices are paired and unpaired sequentially and validated once in all Zigbee Channels
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
      When the below devices are paired and unpaired sequentially on all Zigbee Channels and validated via Telegesis
      | DeviceName          | DeviceType | MacID            |
      | test device         | SLT4       | 001E5E090223263F |


  @SLT4_RegressionTest @SC-FT-69
    Scenario: SC-FT-69_Downgrade firmware of the device and later upgrade the firmware to the previous version
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  FAHRENHEIT scale
      When the below list of DeviceName of DeviceType is upgraded and downgraded between DeviceVersion1 and DeviceVersion2 via Telegisis
      | DeviceName | DeviceType | DeviceVersion1 | DeviceVersion2 |
      | TH         | SLT4      | 06.13           | NA             |
      | TH         | SLT4      | NA             | 06.14           |


  @SLT4_RegressionTest @SC-BT-47 @ZigbeeBindingTest
    Scenario Outline: SC-BT-47_To set bindings and validate the binding table on the device via telegesis stick.
      Given The telegesis is paired with given devices
      When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
      Then the values of the reportable attributes should be the default value
      When the binding table on the device is verified via telegesis stick
      Then the binding table on the device should have 0 entries
      When the zigbee clusters on the device are bound to the telegesis stick
      Then validate if the Bindings are set correctly
      When the reportable attributes are set to report for the given timeperiod
      Then the telegesis stick is mornitored and verified whether the attributes report for the specified timeperiod
      And the values of the reportable attributes should be the set value
      When the reportable attributes are set to report for the default timeperiod
      Then the telegesis stick is mornitored and verified whether the attributes report for the default timeperiod
      Then the values of the reportable attributes should be the default value
      When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
      Then the values of the reportable attributes should be the default value
      When the bindings are cleared on the device
      Then the binding table on the device should have 0 entries
      When the zigbee clusters on the device are bound to the telegesis stick
      Then validate if the Bindings are set correctly
      When the below devices are paired and unpaired sequentially and validated 1 times via Telegesis
        | DeviceName | DeviceType | MacID            |
        | test device| SLT4      | 001E5E090223263F |
      When the binding table on the device is verified via telegesis stick
      Then the binding table on the device should have 0 entries

      Examples:
        | DeviceType |
        | SLT4      |


  @SLT4_RegressionTest @SC-ZT-41 @ZigbeeDumpTest
    Scenario Outline: SC-ZT-41_Download the zigbee dump from the device and validate with the baseline dump file via telegesis stick.
      Given The telegesis is paired with given devices
      When the zigbee dump for the <DeviceType> is downloaded with the clusters and attributes list via telegesis stick
      Then the dump is validated against the corresponding baseline dump file.
        | DeviceType |
        | SLT4      |

      Examples:
        | DeviceType |
        | SLT4      |

  @SLT4_RegressionTest @SC-MT-01
    Scenario Outline: SC-MT-01_verify if the device turns on the heater when there is a heating demand in heat hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT HOLD mode and the required temperature is set to 5 points above the ambient temperature
      Then the HEAT_STAGE_1 FAN_STAGE_1 should be on

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|


  @SLT4_RegressionTest @SC-MT-02
    Scenario Outline: SC-MT-02_verify if the device turns off the heater when there is no heating demand in heat hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT HOLD mode and the required temperature is set to 5 points below the ambient temperature
      Then the heater should be off

      Examples: Temperature scale
        |temp_scale|
        |FAHRENHEIT|
        |   CELCIUS|


  @SLT4_RegressionTest @SC-PT-01
    Scenario Outline: SC-PT-01_verify if the protection timer starts for 180 seconds when the heater/cooler is turned on and off repeatedly
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is set to <mode> mode and the required temperature is set to 5 points <point_type> the ambient temperature 2 times
      Then the <type> should be off
      #Due to sleeps that were used in the case we need a time off of like 15 seconds
      Then the protection timer should be on for 165 seconds

      Examples: Temperature scale
      |temp_scale|  mode      | type    |point_type |
      |FAHRENHEIT|  HEAT HOLD | heater  | above     |
      |   CELCIUS|  COOL HOLD | cooler  | below     |


  @SLT4_RegressionTest @SC-MT-03
    Scenario Outline:SC-MT-03_verify if the device turns heater on for the specified duration in quick heat mode when there is a heating demand
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT_BOOST mode and the required temperature is set to 5 points above the ambient temperature for 3 minutes
      Then the HEAT_STAGE_1 FAN_STAGE_1 should be on
      Then the device timer should be on for 2 minutes

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|

  @SLT4_RegressionTest @SC-MT-04
    Scenario Outline:SC-MT-04_verify if the heater does not turn on on quick heat mode, however timer runs, when there is no heating demand
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT_BOOST mode and the required temperature is set to 5 points below the ambient temperature for 3 minutes
      Then the heater should be off
         #An approximation done here
      Then the device timer should be on for 2 minutes

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|


  @SLT4_RegressionTest @SC-MT-QH-01
    Scenario Outline: SC-MT-QH-01_verify if the user is able to cancel quick heat mode and the stat returns to the previous state
     Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT_BOOST mode and the required temperature is set to 5 points below the ambient temperature for 30 minutes
      When the user cancels quick mode
      Then the QUICK_HEAT mode should be cancelled
      Then the stat should return to the previous state

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|

  @SLT4_RegressionTest @SC-CH-MC26
    Scenario Outline: SC-CH-MC26_verify if the user is able to switch modes
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device switches from HEAT HOLD to <final_mode>
      Then the change to <final_mode> should be successful

      Examples: Temperature scale
      |temp_scale|final_mode     |
      |FAHRENHEIT| HEAT_BOOST    |
      |FAHRENHEIT| COOL_BOOST    |
      |FAHRENHEIT| HEAT SCHEDULE |
      |FAHRENHEIT| COOL SCHEDULE |
      |FAHRENHEIT| COOL HOLD     |
      |FAHRENHEIT| DUAL HOLD     |
      |FAHRENHEIT| DUAL SCHEDULE |
      |FAHRENHEIT| OFF           |
      |CELCIUS   | HEAT_BOOST    |
      |CELCIUS   | COOL_BOOST    |
      |CELCIUS   | HEAT SCHEDULE |
      |CELCIUS   | COOL SCHEDULE |
      |CELCIUS   | COOL HOLD     |
      |CELCIUS   | DUAL HOLD     |
      |CELCIUS   | DUAL SCHEDULE |
      |CELCIUS   | OFF           |


  @SLT4_RegressionTest @SC-MT-05
    Scenario Outline: SC-MT-05_verify if the device turns on the cooler when there is a cooling demand in cool hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in COOL HOLD mode and the required temperature is set to 5 points below the ambient temperature
      Then the COOL_STAGE_1 FAN_STAGE_1 should be on

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|

  @SLT4_RegressionTest @SC-MT-06
    Scenario Outline: SC-MT-06_verify if the device turns off the cooler when there is no cooling demand in heat hold mode
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in COOL HOLD mode and the required temperature is set to 5 points above the ambient temperature
      Then the cooler should be off

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |   CELCIUS|







