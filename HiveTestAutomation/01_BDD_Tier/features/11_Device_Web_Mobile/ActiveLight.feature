Feature: Contains the scenario to test the Active Light
  
  @SC-AL-01 @ActiveLight
  Scenario: SC-AL-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The Active Lights are paired with the Hive Hub
	When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via Hub
	  | BrightnessValue |
	  | 0               |
	  | 100              |
	  | 0               |
	  | 99              |
	  | 0               |
	  | 98              |
	  | 0               |
	  | 97              |
	  | 0               |
	  | 96             |
  
  @SC-AL-01-01 @ActiveLight
  Scenario Outline: SC-AL-01-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The Active Lights are paired with the Hive Hub
	When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied <1>min and validated for the below brightness values Default via Hub
	| BrightnessValue |
	  |0|
	 |2|
	 |4|
	  |6|
	  |8|
	  |10|
	  |12|
	  |14|
	  |16|
	  |18|
	  |20|
	  |22|
	  |24|
	  |26|
	  |28|
	  |30|
 	  |32|
	  |34|
	  |36|
	  |38|
	  |40|
	  |42|
	  |44|
	  |46|
	  |48|
	  |50|
 	  |52|
	  |54|
	  |56|
	  |58|
	  |60|
	  |62|
	  |64|
	  |66|
	  |68|
	  |70|
 	  |72|
	  |74|
	  |76|
	  |78|
	  |80|
	  |82|
	  |84|
	  |86|
	  |88|
	  |90|
	  |92|
	  |94|
	  |96|
	  |98|
  	|100|
	  

 
	Examples:
	  | ActiveLightDevice |
	  | RGBBulb03UK_1 |

	@SC-AL-01-02 @ActiveLight2
  Scenario Outline: SC-AL-01-02_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The Active Lights are paired with the Hive Hub
	When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied 5 min and validated for the below brightness values infinitely via Hub
	  | BrightnessValue |
	  | 0               |
	  | 55              |
	  | 60              |
	  | 65              |
	  | 70              |
	  | 75              |
	  | 80              |
	  | 85              |
	  | 90              |
	  | 95              |
	  | 100             |

	Examples:
	  | ActiveLightDevice |
	  | RGBBulb03UK_1      |
  
  @SC-AL-04-01 @ActiveLight
  Scenario Outline: SC-AL-04-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The Active Lights are paired with the Hive Hub
	When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied and validated for <TimePeriod> for the below brightness values infinitely via Hub
	  | BrightnessValue |
	  | 40              |
	  | 60              |
	  | 80              |
	  | 100             |
	
	Examples:
	  | ActiveLightDevice | TimePeriod |
	  | FWBulb01_1        | 120        |
  
  @SC-AL-02 @ActiveLight
  Scenario: SC-AL-02_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values infinitely via telegesis
	  | BrightnessValue | TimeLapse |
	  | 00              | 1         |
	  | 25              | 1         |
	  | 00              | 1         |
	  | 50              | 1         |
	  | 00              | 1         |
	  | 75              | 1         |
	  | 00              | 1         |
	  | 99              | 1         |
	  | 00              | 1         |
  
  @SC-AL-04 @ActiveLight
  Scenario: SC-AL-04_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON and OFF state and brightness of the light is varied to 50 and validated infinitely with timelapse of 1 second via telegesis
  
  @SC-AL-SH01-01 @ActiveLight @ScheduleTestAPI @6_Event @Verify @APITest
  Scenario Outline: SC-AL-SH01-01_Set the given default 'six' event schedule for the given day and verify the same for Active Light
	Given The Active Light are paired with the Hive Hub
	When The below <Device> schedule is set for <Day> via Hub
	  | Start Time | SmartPlug State | Brightness |
	  | 06:30      | ON              | 70         |
	  | 08:30      | OFF             | 100        |
	  | 12:00      | ON              | 50         |
	  | 14:00      | OFF             | 90         |
	  | 16:00      | ON              | 100        |
	  | 21:30      | OFF             | 0          |
	Then Verify if the Schedule is set
	
	Examples:
	  | Device       | Day   |
	  | FWBulb01US_1 | Today |
  
  @SC-AL-SH01-02 @ActiveLight @ScheduleTestAPI @6_Event @Verify @APITest @Tunable
  Scenario Outline: SC-AL-SH01-02_Set the given default 'six' event schedule for the given day and verify the same for Active Light
	Given The Active Light are paired with the Hive Hub
	When The below <Device> schedule is set for <Day> via Hub
	  | Start Time | SmartPlug State | Brightness |
	  | 06:30      | ON              | 70         |
	  | 08:30      | OFF             | 100        |
	  | 12:00      | ON              | 50         |
	  | 14:00      | OFF             | 90         |
	  | 16:00      | ON              | 100        |
	  | 21:30      | OFF             | 0          |
	Then Verify if the Schedule is set
	And Validate if the Schedule is set for the whole week on the <Device>
	
	Examples:
	  | Device       | Day   |
	  | TWBulb01US_1 | Today |
  
  @SC-AL-SHW01-01 @ActiveLight @ScheduleTest @Week @Validate @APITest
  Scenario Outline: SC-CH-SH01-01_Set the given custom schedule for the whole week and verify the same for Active Light
	Given The Active Light are paired with the Hive Hub
	When The below schedule is set for the whole week on the <Device> via Hub API
	  | Day | Event1       | Event2       | Event3       | Event4       | Event5       | Event6      |
	  | Mon | 06:30,ON,100 | 08:30,OFF,20 | 10:30,ON,100 | 13:00,OFF,10 | 15:30,ON,70  | 22:30,OFF,0 |
	  | Tue | 06:30,ON,16  | 08:30,OFF,29 | 10:30,ON,10  | 13:00,OFF,90 | 15:30,ON,100 | 22:30,OFF,0 |
	  | Wed | 00:30,ON,17  | 04:30,OFF,30 | 10:45,ON,1   | 13:00,OFF,0  |              |             |
	  | Thu | 15:30,ON,18  | 18:30,OFF,31 | 20:30,ON,1   | 23:00,OFF,8  | 23:30,ON,40  | 23:45,OFF,0 |
	  | Fri | 06:30,ON,19  | 08:30,OFF,32 |              |              |              |             |
	  | Sat | 06:30,ON,20  | 08:30,OFF,28 | 10:30,ON,1   | 13:00,OFF,07 | 15:30,ON,30  | 22:30,OFF,0 |
	  | Sun | 12:30,ON,14  | 15:30,OFF,0  | 19:15,OFF,0  | 20:00,ON,6   | 22:30,ON,31  | 23:30,OFF,0 |
	Then Verify if the Schedule is set
	Then Validate if the Schedule is set for the whole week on the <Device>
	
	Examples:
	  | Device     |
	  | FWBulb01_1 |
  
  @SC-AL-SHW01-02 @ActiveLight @ScheduleTest @Week @Validate @APITest
  Scenario Outline: SC-CH-SH01-02_Set the given custom schedule for the whole week and verify the same for Active Light
	Given The Active Light are paired with the Hive Hub
	When The below schedule is set for the whole week on the <Device> via Hub API
	  | Day | Event1       | Event2       | Event3       | Event4       | Event5       | Event6      |
	  | Mon | 06:30,ON,100 | 08:30,OFF,20 | 10:30,ON,100 | 13:00,OFF,10 | 15:30,ON,70  | 22:30,OFF,0 |
	  | Tue | 06:30,ON,16  | 08:30,OFF,29 | 10:30,ON,10  | 13:00,OFF,90 | 15:30,ON,100 | 22:30,OFF,0 |
	  | Wed | 00:30,ON,17  | 04:30,OFF,30 | 10:45,ON,1   | 13:00,OFF,0  |              |             |
	  | Thu | 15:30,ON,18  | 18:30,OFF,31 | 20:30,ON,1   | 23:00,OFF,8  | 23:30,ON,40  | 23:45,OFF,0 |
	  | Fri | 06:30,ON,19  | 08:30,OFF,32 |              |              |              |             |
	  | Sat | 06:30,ON,20  | 08:30,OFF,28 | 10:30,ON,1   | 13:00,OFF,07 | 15:30,ON,30  | 22:30,OFF,0 |
	  | Sun | 22:15,ON,100 | 22:30,OFF,0  | 22:45,ON,100 | 23:00,OFF,6  | 23:15,ON,31  | 23:30,ON,70 |
	Then Validate if the Schedule is set for the whole week on the <Device>
	
	Examples:
	  | Device     |
	  | FWBulb01_1 |
  
  @SC-AL-CL-01 @RGB @ActiveLight
  Scenario: SC-AL-CL-01_Switch between colors in a RGB Bulb by changing the Hue
	Given The telegesis is paired with given devices
	When The hue value of the bulb is changed and validated for the given hue value infinitely via telegesis
	  | HueValue | TimeLapse |
	  | 00       | 1         |
	  | 01       | 1         |
	  | 21       | 1         |
	  | 31       | 1         |
	  | 41       | 1         |
	  | 51       | 1         |
	  | 61       | 1         |
	  | 71       | 1         |
	  | 81       | 1         |
	  | 91       | 1         |
	  | A1       | 1         |
  
  @SC-AL-CL-02 @RGB @ActiveLight
  Scenario: SC-AL-CL-02_Change color level in a RGB Bulb by changing the saturation
	Given The telegesis is paired with given devices
	When The hue value of the bulb is changed and validated for the given saturation value infinitely via telegesis
	  | SatValue | TimeLapse |
	  | 00       | 1         |
	  | 2F       | 1         |
	  | 3F       | 1         |
	  | 4F       | 1         |
	  | 5F       | 1         |
	  | 6F       | 1         |
	  | 7F       | 1         |
	  | 8F       | 1         |
	  | 9F       | 1         |
	  | AF       | 1         |
	  | BF       | 1         |
	  | CF       | 1         |
	  | DF       | 1         |
	  | EF       | 1         |
	  | FE       | 1         |
  
  @SC-AL-CL-03 @RGB @ActiveLight
  Scenario: SC-AL-CL-03_Change Hue and Saturation in a RGB Bulb by changing the Hue and saturation respectively
	Given The telegesis is paired with given devices
	When The hue value of the rgb bulb is changed and validated for the given saturation value infinitely via telegesis
	  | HueValue | SatValue | TimeLapse |
	  | 00       | 00       | 1         |
	  | 01       | 2F       | 1         |
	  | 21       | 3F       | 1         |
	  | 31       | 4F       | 1         |
	  | 41       | 5F       | 1         |
	  | 51       | 6F       | 1         |
	  | 61       | 7F       | 1         |
	  | 71       | 8F       | 1         |
	  | 81       | 9F       | 1         |
	  | 91       | BF       | 1         |
	  | A1       | FE       | 1         |
  
  @SC-AL-CL-04 @RGB @ActiveLight
  Scenario Outline: SC-AL-CL-04_Change Hue with Saturation and brightness in a RGB Bulb by changing the Hue with saturation and brightness respectively
	Given The telegesis is paired with given devices
	When The hue value of the <DeviceType> is changed and validated for the given saturation and brightness value infinitely via telegesis
	  | HueValue | SatValue | Brightness | TimeLapse |
	  | 00       | 00       | 00         | 1         |
	  | 01       | 2F       | 10         | 1         |
	  | 21       | 3F       | 20         | 1         |
	  | 31       | 4F       | 30         | 1         |
	  | 41       | 5F       | 40         | 1         |
	  | 51       | 6F       | 50         | 1         |
	  | 61       | 7F       | 60         | 1         |
	  | 71       | 8F       | 70         | 1         |
	  | 81       | 9F       | 80         | 1         |
	  | 91       | BF       | 90         | 1         |
	  | A1       | FE       | 100        | 1         |
	  | 01       | 2F       | 10         | 1         |
	
	Examples:
	  | DeviceType  |
	  | RGBBulb01UK |
  
  @SC-AL-CL-05 @TW @ActiveLight
  Scenario: SC-AL-CL-05_Change Warm to Cook and Brightness in a RGB Bulb by changing the Tune and temperature respectively
	Given The telegesis is paired with given devices
	When The Tune value of the TW bulb is changed and validated for the given Brightness value infinitely via telegesis
	  | Tune | BrightnessValue | TimeLapse |
	  | 0000 | ON              | 1         |
	  | 4E20 | 00              | 1         |
	  | 61A8 | 20              | 1         |
	  | 7530 | 00              | 1         |
	  | 88B8 | 40              | 1         |
	  | 9470 | 00              | 1         |
	  | A028 | 60              | 1         |
	  | B3B0 | 00              | 1         |
	  | C350 | 80              | 1         |
	  | D6D8 | 00              | 1         |
	  | EA60 | 99              | 1         |
	  | FFFF | OFF             | 1         |
  
  
  @SC-AL-SP-01 @FlickeringTest
  Scenario: SC-AL-SP-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 10 brightness for 60 mins via telegesis
  
  @SC-AL-SP-02 @FlickeringTest
  Scenario: SC-AL-SP-02_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 20 brightness for 60 mins via telegesis
  
  @SC-AL-SP-03 @FlickeringTest
  Scenario: SC-AL-SP-03_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 30 brightness for 60 mins via telegesis
  
  @SC-AL-SP-04 @FlickeringTest
  Scenario: SC-AL-SP-04_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 40 brightness for 60 mins via telegesis
  
  @SC-AL-SP-05 @FlickeringTest
  Scenario: SC-AL-SP-05_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 50 brightness for 60 mins via telegesis
  
  @SC-AL-SP-06 @FlickeringTest
  Scenario: SC-AL-SP-06_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 60 brightness for 60 mins via telegesis
  
  @SC-AL-SP-07 @FlickeringTest
  Scenario: SC-AL-SP-07_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 70 brightness for 60 mins via telegesis
  
  @SC-AL-SP-08 @FlickeringTest
  Scenario: SC-AL-SP-08_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 80 brightness for 60 mins via telegesis
  
  @SC-AL-SP-09 @FlickeringTest
  Scenario: SC-AL-SP-09_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 90 brightness for 60 mins via telegesis
  
  @SC-AL-SP-10 @FlickeringTest
  Scenario: SC-AL-SP-10_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the 100 brightness for 60 mins via telegesis
  
  @SC-AL-SP-11
  Scenario Outline: SC-AL-SP-11_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the <Brightness> brightness for 60 mins via telegesis
	
	Examples:
	  | Brightness |
	  | 10         |
	  | 20         |
	  | 30         |
	  | 40         |
	  | 50         |
	  | 60         |
	  | 70         |
	  | 80         |
	  | 90         |
	  | 100        |
  
  @SC-AL-SP-12 @FlickeringTest
  Scenario: SC-AL-SP-12_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state and brightness of the light is validated for the brightness range between 100 to 0 for 1 mins via telegesis
  
  @SC-AL-SP-13 @FlickeringTest
  Scenario: SC-AL-SP-13_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state with given temperature and brightness of the light is validated for the brightness range between 100 to 0 for 1 mins via telegesis
  
  @SC-AL-SP-14 @FlickeringTest
  Scenario: SC-AL-SP-14_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state with given temperature and brightness of the light is validated for the brightness range between 100 to 0 for 5 mins via telegesis
  
  @SC-AL-SP-15 @FlickeringTest
  Scenario: SC-AL-SP-15_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state with given colour and brightness of the light is validated for the brightness range between 100 to 0 for 1 mins via telegesis
	  | HueValue | SatValue | TimeLapse |
	  | 00       | FE       | 1         |
	  | 01       | FE       | 1         |
	  | 21       | FE       | 1         |
	  | 31       | FE       | 1         |
	  | 41       | FE       | 1         |
	  | 51       | FE       | 1         |
	  | 61       | FE       | 1         |
	  | 71       | FE       | 1         |
	  | 81       | FE       | 1         |
	  | 91       | FE       | 1         |
	  | A1       | FE       | 1         |
	  | 01       | FE       | 1         |
  
  @SC-AL-SP-16 @FlickeringTest
  Scenario: SC-AL-SP-16_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON state with given temperature and brightness of the light is validated with varied gain for the brightness range between 100 to 0 for 1 mins for via telegesis
  
  @SC-AL-03 @ActiveLight @Telegesis
  Scenario Outline: SC-AL-03_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The ActiveLight is switched ON and OFF state and brightness of the light is varied and validated for the below brightness values for <TIme Duration  in minutes> via telegesis
	  | BrightnessValue | TimeLapse |
	  | ON              | 1         |
	  | 20              | 1         |
	  | 00              | 1         |
	  | 40              | 1         |
	  | 00              | 1         |
	  | 60              | 1         |
	  | 00              | 1         |
	  | 80              | 1         |
	  | 00              | 1         |
	  | 100             | 1         |
	  | OFF             | 1         |
	
	Examples:
	  | TIme Duration  in minutes |
	  | 1                         |
    
  






