#This tests validate the device built in humidifier
# It should be noted that the device should have ACC connected

Feature: To validate the humidifier and dehumidifier
  @SLT4_RegressionTest_Humidifier @SC-HT-01
    Scenario Outline: SC-HT-01_verify if the humidifier can be set in any of the device modes (Except when the device is off)
    Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
    When the stat is set to mode <device_mode>
    When the ACC wiring configuration is connected
    When The humidifier is set to <percent> percentage humidity
    Then the humidity should be set to <percent> percentage

     Examples: Device humidity values
    |temp_scale|device_mode|percent|
    |FAHRENHEIT|HEAT_BOOST |40     |
    |CELCIUS   |HEAT_BOOST |35     |
    |FAHRENHEIT|COOL_BOOST |50     |
    |CELCIUS   |COOL_BOOST |45     |

  @SLT4_RegressionTest_Humidifier @SC-HT-02
    Scenario Outline: SC-HT-02_verify if the de-humidifier can be set in any of the device modes (Except when the device is off)
     Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
     When the stat is set to mode <device_mode>
     When the ACC wiring configuration is connected
     When The de-humidifier is set to <percent> percentage humidity
     Then the humidity should be set to <percent> percentage

     Examples: Device humidity values
    |temp_scale|device_mode|percent|
    |FAHRENHEIT|HEAT_BOOST |40     |
    |CELCIUS   |HEAT_BOOST |35     |
    |FAHRENHEIT|COOL_BOOST |50     |
    |CELCIUS   |COOL_BOOST |45     |
