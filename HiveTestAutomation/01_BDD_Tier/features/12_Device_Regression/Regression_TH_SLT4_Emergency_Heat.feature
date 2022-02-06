Feature: Validate the emergency heat scenarios

"""
Emergency heat feature test
Please do not the following , This test depends on the device ability to switch to emergemcy mode (The current room
temperature should be less than 25 degrees or 78 Degree F) ,

If the precondition is not met then the test case will fail

The device wiring configuration should have emergency heat on
W1, W3, Y1, Rh, C, O/B

"""


  @SLT4_RegressionTest_Emergency_heat @SC-MT-EM-01
    Scenario Outline: SC-MT-EM-01_verify if the emergency heat is turned on when the precondition is met (ambient temp < 25C / 77F)
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The emergency heat precondition has been met
      When The emergency heat is turned on
      Then The emergency heat should be enabled

      Examples: Temperature scale
        |temp_scale|
        |FAHRENHEIT|
        |CELCIUS   |


  @SLT4_RegressionTest_Emergency_heat @SC-MT-EM-02
    Scenario Outline: SC-MT-EM-02_verify if the user is able to cancel the emergency heat
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The emergency heat precondition has been met
      When The emergency heat is turned on
      Then The emergency heat should be enabled
      When The emergency heat is turned off
      Then The emergency heat should be disabled

     Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |

  @SLT4_RegressionTest_Emergency_heat @SC-MT-EM-03
    Scenario Outline: SC-MT-EM-03_verify if the changes the system mode , The emergency heat is cancelled
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The emergency heat precondition has been met
      When The emergency heat is turned on
      Then The emergency heat should be enabled
      When the device is in <device_mode> mode and the required temperature is set to <number> points <value> the ambient temperature
      Then The emergency heat should be disabled


      Examples: Device Valid mode transtions
      |temp_scale|value     |device_mode|number|
      |FAHRENHEIT|above     |HEAT HOLD  |5     |
      |FAHRENHEIT|above     |COOL HOLD  |5     |
      |CELCIUS   |above     |HEAT HOLD  |3     |
      |CELCIUS   |above     |COOL HOLD  |3     |

  @SLT4_RegressionTest_Emergency_heat @SC-MT-EM-04
    Scenario Outline: SC-MT-EM-04_verify if the device is rebooted , The emergency mode is still retained
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When The emergency heat precondition has been met
      When The emergency heat is turned on
      Then The emergency heat should be enabled
      When The device is rebooted
      Then The emergency heat should be enabled

      Examples: Temperature scale
      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |

  @SLT4_RegressionTest_Emergency_heat @SC-MT-EM-05
    Scenario Outline: SC-MT-EM-05_verify if the emergency mode is cancelled , It should restore the previous stat state (which was previously in Heat hold mode)
      Given the TGstick is paired with the SLT4 thermostat and the device is switched to  <temp_scale> scale
      When the device is in HEAT HOLD mode and the required temperature is set to 5 points above the ambient temperature
      When The emergency heat precondition has been met
      When The emergency heat is turned on
      Then The emergency heat should be enabled
      When The emergency heat is turned off
      Then The emergency heat should be disabled
      Then it should be switched to mode HEAT HOLD
      Then The heat temperature should be changed by 5 points

      Examples: Different heat modes
      |temp_scale|
      |CELCIUS   |
      |FAHRENHEIT|



