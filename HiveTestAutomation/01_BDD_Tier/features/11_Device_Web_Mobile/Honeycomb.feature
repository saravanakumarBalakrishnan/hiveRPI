# Created by anuj.kumar at 18/01/2017

#@authors:
#iOS        - Shubanker
#Android    - Anuj Kumar
#Web        - TBD
Feature: Validate Honeycomb

  @SC-HC-DS_03 @Honeycomb
  Scenario: SC-HC-DS_03_Verify the title header of the HoneyComb dashboard screen

  Given The Hive products are paired with hub
  When User is on Dashboard screen
  Then Validate the title header of the HoneyComb dashboard screen

  @SC-HC-DS_02 @Honeycomb
  Scenario: SC-HC-DS_02_Validate dashboard screen for the configured devices

  Given The Hive products are paired with hub
  When User is on Dashboard screen
  Then Validate status of devices in dashboard

  @SC-HC-DS_04 @Honeycomb
  Scenario: SC-HC-DS_04_Verify the Hierarchy of devices in HoneyComb dashboard screen

  Given The Hive products are paired with hub
  When User is on Dashboard screen
  Then Validate the Hierarchy of the HoneyComb dashboard screen

  @SC-HC-DS_05 @Honeycomb @Devicelist
  Scenario: SC-HC-DS_05_Verify the status of the devices are displayed as expected in Device List screen

  Given The Hive products are paired with hub
  When User is on Device list screen
  Then Validate the Status of devices in Device List screen

  @SC-HC-DS_06 @Honeycomb @Devicelist
  Scenario: SC-HC-DS_06_Verify the title header of the Device List screen

  Given The Hive products are paired with hub
  When User is on Device list screen
  Then Validate the title header of Device List screen

  @SC-HC-DS_07 @Honeycomb @Devicelist
  Scenario: SC-HC-DS_07_Verify the Hierarchy of devices in Device List screen

  Given The Hive products are paired with hub
  When User is on Device list screen
  Then Validate the Hierarchy of Device List screen

  @SC-HC-DS_08 @Honeycomb
  Scenario Outline: SC-HC-DS_08_Verify if the HoneyComb icon is displayed on top right of all screens and the user is able to reach the last visited dashboard

  Given The Hive products are paired with hub
  When User navigates to <ScreenName> screen and Validates the presence and click on the honeycomb icon
  Then User is on Dashboard screen

  Examples:
		|ScreenName        |
		|Heating           |
        |Manage devices    |
        |Install devices   | 
        |All Recipes       |
         |Geolocation       | 
        |Holiday mode      |
