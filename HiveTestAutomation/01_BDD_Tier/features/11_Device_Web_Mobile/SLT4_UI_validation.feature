


      Feature: UI / Screen based validation test cases for Regression cases for SLT4 for electric air handler


   @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_001
    Scenario Outline: STH-UI-REG-001_verify if the user is able to switch to different modes using the stat UI and also verify if the stat is toggled correctly
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
      When the device is set to mode <device_mode> with <change> points <change_mode> ambient temperature via UI
      Then The device should be successfully switched to <device_mode> in UI
      Then it should be switched to mode <device_mode>


      Examples: Device temperature change scenarios
      |temp_scale|device_mode    |change|change_mode|
      |FAHRENHEIT| COOL HOLD     | 4    |below      |
      |FAHRENHEIT| HEAT_BOOST    | 4    |above      |
      |FAHRENHEIT| COOL_BOOST    | 4    |below      |
      |FAHRENHEIT| HEAT HOLD     | 4    |above      |
      |FAHRENHEIT| HEAT SCHEDULE | 4    |above      |
      |FAHRENHEIT| COOL SCHEDULE | 4    |above      |
      |CELCIUS   | COOL HOLD     | 4    |below      |
      |CELCIUS   | HEAT_BOOST    | 4    |above      |
      |CELCIUS   | COOL_BOOST    | 4    |below      |
      |CELCIUS   | HEAT HOLD     | 4    |above      |
      |CELCIUS   | HEAT SCHEDULE | 4    |above      |
      |CELCIUS   | COOL SCHEDULE | 4    |above      |

    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_002
    Scenario Outline: STH-UI-REG-002_verify if the user is able to switch to dual hold mode using the stat UI and also verify if the stat is toggled correctly
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
      When the stat UI is set to dual hold mode with heat target set to <heat_target> and cool target set to <cool_target>
      Then The device should be successfully switched to DUAL HOLD in UI
      Then it should be switched to mode DUAL HOLD

      Examples: Device Modes
      |temp_scale|heat_target|cool_target|
      |FAHRENHEIT| 70        |     80    |
      |CELCIUS   | 22        |     30    |


    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_003
    Scenario Outline: STH-UI-REG-003_verify if the stat is able to be set to quick cool and heat mode via UI
      Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
      When the device is set to mode <device_mode> with <change> points <change_mode> ambient temperature via UI
      Then the stat UI should be in <device_mode> with the target temperature changed <change> points <change_mode> the ambient temperature
      Then the stat should display the expected target temperature value


      Examples: Device Modes
      |temp_scale|device_mode|change|change_mode|
      |FAHRENHEIT| HEAT_BOOST|3     |above      |
      |FAHRENHEIT| COOL_BOOST|3     |below      |
      |CELCIUS   | HEAT_BOOST|2     |above      |
      |CELCIUS   | COOL_BOOST|2     |below      |

    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_004
      Scenario Outline: STH-UI-REG-004_verify if in the quick mode the stat timer values are displayed correctly in the heat and cool boost modes
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the device is set to  boost mode <boost_mode> with <change> points <change_mode> ambient temperature via UI for <hours> hours
        Then The stat should display the timer value for atleast <expected_min_hours> hours and <expected_min_mins> mins

        Examples: Device boost timer values
        |temp_scale|boost_mode |change|change_mode|hours|expected_min_hours|expected_min_mins|
        |CELCIUS   |HEAT_BOOST |5     |above      |0    | 0                |29               |
        |CELCIUS   |HEAT_BOOST |5     |above      |2    | 1                |58               |
        |CELCIUS   |COOL_BOOST |5     |below      |2    | 1                |58               |
        |CELCIUS   |COOL_BOOST |5     |below      |2    | 1                |58               |
        |FAHRENHEIT|HEAT_BOOST |5     |above      |0    | 0                |29               |
        |FAHRENHEIT|HEAT_BOOST |5     |above      |2    | 1                |58               |
        |FAHRENHEIT|COOL_BOOST |5     |below      |2    | 1                |58               |
        |FAHRENHEIT|COOL_BOOST |5     |below      |2    | 1                |58               |

    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_005
      Scenario Outline: STH-UI-REG-005_verify the override values in heat boost and heat hold mode
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the device is set to mode <device_mode> with <change> points <change_mode> ambient temperature via UI
        When The stat heat temperature is overridden by <change> degrees via UI
        Then the device should be in <device_mode> mode
        Then The heat temperature should be overridden in UI by <change> points

        Examples: Heat temperature override values
        |temp_scale|device_mode|change|change_mode|
        |CELCIUS   |HEAT HOLD  | 3    |above      |
        |CELCIUS   |HEAT_BOOST | 3    |above      |
        |FAHRENHEIT|HEAT HOLD  | 3    |above      |
        |FAHRENHEIT|HEAT_BOOST | 3    |above      |




    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_006
      Scenario Outline: STH-UI-REG-006_verify the override values in cool boost and cool hold mode
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the device is set to mode <device_mode> with <change> points <change_mode> ambient temperature via UI
        When The stat cool temperature is overridden by <change> degrees via UI
        Then the device should be in <device_mode> mode
        Then The cool temperature should be overridden in UI by <change> points

        Examples: Heat temperature override values
        |temp_scale|device_mode|change|change_mode|
        |CELCIUS   |COOL HOLD  | 3    |below      |
        |CELCIUS   |COOL_BOOST | 3    |below      |
        |FAHRENHEIT|COOL HOLD  | 3    |below      |
        |FAHRENHEIT|COOL_BOOST | 3    |below      |


    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_007
        Scenario Outline: STH-UI-REG-007_verify if the protection timer functionality
         Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
         When The device is switched to mode <device_mode>  with  <change> points <change_mode> ambient temperature and OFF 1 times via UI
         When the device is set to mode <device_mode> with <change> points <change_mode> ambient temperature via UI
         Then The protection timer should be ON in UI
         Then The protection timer should be on for atleast 2 minutes in the UI

      Examples: Heat temperature override values

      |temp_scale|device_mode|change|change_mode|
      |FAHRENHEIT|COOL HOLD  |3     |below      |
      |CELCIUS   |COOL HOLD  |3     |below      |
      |FAHRENHEIT|HEAT HOLD  |3     |above      |
      |CELCIUS   |HEAT HOLD  |3     |above      |


      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_008
        Scenario Outline: STH-UI-REG-008_verify if the device is able to toggle from quick heat to quick cool mode in UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the device is set to  boost mode HEAT_BOOST with 3 points above ambient temperature via UI for 0 hours
        Then the stat UI should be in HEAT_BOOST with the target temperature changed 3 points above the ambient temperature
        Then The stat should display the timer value for atleast 0 hours and 29 mins
        When the device is set to  boost mode COOL_BOOST with 3 points below ambient temperature via UI for 2 hours
        Then the stat UI should be in COOL_BOOST with the target temperature changed 3 points below the ambient temperature
        Then The stat should display the timer value for atleast 1 hours and 58 mins


        Examples: Device temperature scale

      |temp_scale|
      |FAHRENHEIT|
      |CELCIUS   |


        @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_009
          Scenario Outline: STH-UI-REG-009_verify if the user is able to switch boost time duration and temperature in UI
          Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
          When the device is set to  boost mode <boost_mode> with 2 points <change_mode> ambient temperature via UI for 0 hours
          Then the stat UI should be in <boost_mode> with the target temperature changed 2 points <change_mode> the ambient temperature
          Then The stat should display the timer value for atleast 0 hours and 28 mins
          When the device is set to  boost mode <boost_mode> with 3 points <change_mode> ambient temperature via UI for 2 hours
          Then The stat should display the timer value for atleast 1 hours and 58 mins

           Examples: Device boost mode changes

             |temp_scale|boost_mode|change_mode|
             |FAHRENHEIT|COOL_BOOST|below      |
             |FAHRENHEIT|HEAT_BOOST|above      |
             |CELCIUS   |HEAT_BOOST|above      |
             |CELCIUS   |COOL_BOOST|below      |



          @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_010
            Scenario Outline: STH-UI-REG-010_verify verify if the device is able to toggle to different modes and back to the original mode without a set point
            Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
            When the stat is switched to the mode <from_mode> in UI
            Then The device should be successfully switched to <from_mode> in UI
            Then it should be switched to mode <from_mode>
            When the stat is switched to the mode <to_mode> in UI
            Then The device should be successfully switched to <to_mode> in UI
            Then it should be switched to mode <to_mode>
            When the stat is switched to the mode <from_mode> in UI
            Then The device should be successfully switched to <from_mode> in UI
            Then it should be switched to mode <from_mode>


            Examples: Device boost mode changes
              |temp_scale|from_mode       |to_mode       |
              |FAHRENHEIT| HEAT SCHEDULE  |HEAT HOLD     |
              |FAHRENHEIT| COOL SCHEDULE  |COOL HOLD     |
              |FAHRENHEIT| DUAL SCHEDULE  |DUAL HOLD     |
              |CELCIUS   | HEAT SCHEDULE  |HEAT HOLD     |
              |CELCIUS   | COOL SCHEDULE  |COOL HOLD     |
              |CELCIUS   | DUAL SCHEDULE  |DUAL HOLD     |

      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_011
        Scenario Outline:  STH-UI-REG-011_verify if the device name is properly set in the device UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the device name is set to <name>
        Then the device name <name> should be set on the stat UI

        Examples: Device name scenario
          |temp_scale|name |
          |FAHRENHEIT|f123|
          |CELCIUS   |c123|

      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_012
        Scenario Outline:STH-REG-012_verify if the device returns to the previous state when the Quick heat / Cool is cancelled
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the stat is switched to the mode <initial_mode> in UI
        When the device is in <device_mode> mode and the required temperature is set to <temp_points> points <temp_change_mode> the ambient temperature for <duration> minutes
        When After the duration of <duration> minutes
        Then The device should be successfully switched to <initial_mode> in UI

        Examples: Device previous mode scenario
        |temp_scale|initial_mode|device_mode |temp_points|temp_change_mode|duration|
        |CELCIUS   |HEAT SCHEDULE|COOL_BOOST |2          |below           |1       |
        |CELCIUS   |HEAT SCHEDULE|HEAT_BOOST |2          |above           |1       |
        |CELCIUS   |COOL SCHEDULE|COOL_BOOST |2          |below           |1       |
        |CELCIUS   |COOL SCHEDULE|HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|HEAT HOLD    |HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|HEAT HOLD    |COOL_BOOST |2          |below           |1       |
        |FAHRENHEIT|COOL HOLD    |COOL_BOOST |2          |below           |1       |
        |FAHRENHEIT|COOL HOLD    |HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|HEAT SCHEDULE|COOL_BOOST |2          |below           |1       |
        |FAHRENHEIT|HEAT SCHEDULE|HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|COOL SCHEDULE|COOL_BOOST |2          |below           |1       |
        |FAHRENHEIT|COOL SCHEDULE|HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|DUAL SCHEDULE|HEAT_BOOST |2          |above           |1       |
        |FAHRENHEIT|DUAL SCHEDULE|COOL_BOOST |2          |below           |1       |

      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_013
        Scenario Outline:STH-REG-013_verify if the user is able to set the vacation mode for the stat and the mode is reflected successfully in UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When The vacation mode is set for 2 minutes from the current stat time
        Then The device should be successfully switched to VACATION MODE in UI

        Examples: Device Temperature scale
          |temp_scale|
          |FAHRENHEIT|
          |CELCIUS   |


      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_014
        Scenario Outline:STH-REG-014_verify if the user is able to cancel the vacation mode for the stat and the mode is reflected successfully in UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When The vacation mode is set for 2 minutes from the current stat time
        When The vacation mode is cancelled
        Then The vacation mode should be disabled in UI

         Examples: Device Temperature scale
          |temp_scale|
          |FAHRENHEIT|
          |CELCIUS   |


      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_015
        Scenario Outline:STH-REG-015_verify if the vacation mode has ended the stat is restored to the previous HEAT states in UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the stat is switched to the mode <initial_mode> in UI
        When The stat heat temperature is overridden by <change> degrees via UI
        When The vacation mode is set for 2 minutes from the current stat time
        When The vacation mode ends after 2 minutes in the UI
        Then The device should be successfully switched to <initial_mode> in UI
        Then The heat temperature should be overridden in UI by <change> points


         Examples: Device Temperature scale
          |temp_scale|initial_mode|change|
          |FAHRENHEIT|HEAT HOLD   |2     |
          |CELCIUS   |HEAT HOLD   |2     |


       @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_016
        Scenario Outline:STH-REG-016_verify if the vacation mode has ended the stat is restored to the previous COOLING states in UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the stat is switched to the mode <initial_mode> in UI
        When The stat cool temperature is overridden by <change> degrees via UI
        When The vacation mode is set for 2 minutes from the current stat time
        When The vacation mode ends after 2 minutes in the UI
        Then The device should be successfully switched to <initial_mode> in UI
        Then The cool temperature should be overridden in UI by <change> points


         Examples: Device Temperature scale
          |temp_scale|initial_mode|change|
          |FAHRENHEIT|COOL HOLD   |2     |
          |CELCIUS   |COOL HOLD   |2     |



      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_017
      Scenario Outline:STH-REG-017_verify if the humidifier can be set in any of the device modes (Except when the device is off) and can set by the user
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When the stat is switched to the mode <device_mode> in UI
        When the ACC wiring configuration is connected
        When The stat <humidity_control_type> is set to <percentage> percent via UI
        Then The stat humidity control type should be <humidity_control_type>
        Then The stat humidity percent should be <percentage> in the UI
        Then the humidity should be set to <percentage> percentage

          Examples: Device Temperature scale
          |temp_scale|humidity_control_type|percentage|device_mode|
          |FAHRENHEIT|HUMIDIFIER           |35        |HEAT HOLD    |
          |FAHRENHEIT|HUMIDIFIER           |45        |COOL HOLD    |
          |FAHRENHEIT|HUMIDIFIER           |40        |HEAT HOLD    |
          |FAHRENHEIT|HUMIDIFIER           |55        |HEAT HOLD    |
          |FAHRENHEIT|HUMIDIFIER           |60        |HEAT_BOOST   |
          |FAHRENHEIT|HUMIDIFIER           |35        |COOL_BOOST   |
          |FAHRENHEIT|HUMIDIFIER           |35        |DUAL HOLD    |
          |FAHRENHEIT|HUMIDIFIER           |35        |DUAL SCHEDULE|
          |CELCIUS   |HUMIDIFIER           |35        |HEAT HOLD    |
          |CELCIUS   |HUMIDIFIER           |45        |COOL HOLD    |
          |CELCIUS   |HUMIDIFIER           |40        |HEAT HOLD    |
          |CELCIUS   |HUMIDIFIER           |55        |HEAT HOLD    |
          |CELCIUS   |HUMIDIFIER           |60        |HEAT_BOOST   |
          |CELCIUS   |HUMIDIFIER           |35        |COOL_BOOST   |
          |CELCIUS   |HUMIDIFIER           |35        |DUAL HOLD    |
          |CELCIUS   |HUMIDIFIER           |35        |DUAL SCHEDULE|

    @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_018
    #Ensure that the fan is connected to the
      Scenario Outline:STH-REG-018_verify if the user is able to set the fan modes AUTO And via UI
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When The device fan is set to <target_fan_mode> MODE in the UI
        Then the device fan should be successfuly set to <target_fan_mode>

       Examples: Device Temperature scale
          |temp_scale|target_fan_mode|
          |FAHRENHEIT|AUTO           |
          |FAHRENHEIT|ALWAYS_ON      |
          |CELCIUS   |AUTO           |
          |CELCIUS   |ALWAYS_ON      |

      @STH_US_RegressionTest_UI_Electric_handler @STH_UI_REG_019
       Scenario Outline:STH-REG-019_verify if the user is able to set the fan mode CIRCULATE with the desired timer value
        Given the TGstick is paried with the SLT4 thermostat and the device is switched to  <temp_scale> scale for UI based validation
        When The device fan is set to CIRCULATE_MODE for <duration> mins in the UI
        Then the device fan should be successfuly set to CIRCULATE
         Then the fan circulate timer should be set to <duration> mins


       Examples: Device Temperature scale
          |temp_scale|duration|
          |FAHRENHEIT|15      |
          |FAHRENHEIT|30      |
          |CELCIUS   |15      |
          |CELCIUS   |30      |