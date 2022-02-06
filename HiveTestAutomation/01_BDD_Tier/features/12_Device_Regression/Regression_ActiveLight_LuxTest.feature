Feature: Contains all the Regression scenarios for Smart Plugs testing

  @SC-LDS-01-01 @ActiveLight
  Scenario Outline: SC-LDS-01-01_Switch ActiveLight to ON and OFF state and change the brightness of the light and validate the same
	Given The telegesis is paired with given devices
	When The <ActiveLightDevice> is switched ON and OFF state and brightness of the light is varied <0>min and validated for the below brightness values Default via TGStick
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
	  | RB 245_1 |
