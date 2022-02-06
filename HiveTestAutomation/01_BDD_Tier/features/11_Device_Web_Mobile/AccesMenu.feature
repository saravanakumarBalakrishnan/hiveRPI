Feature: To validate the main menu options in Hive app.

  @SC_ES_VA_01 @EmptySlots
      Scenario: SC_ES_001_Verify if the empty slots are coming if there are less than 7 devices in the screen.
      Given Hive products should be paired to the Hub.
       When User is in Dashboard screen.
        Then calculate the number of devices and check the empty slots if number of devices is less than 7.

    @SC_MM_VA_01 @MainMenuOptions
    Scenario: SC_MM_VA_01_Validate the menu options after clicking the main menu icon in app.
      Given Hive products should be paired to the Hub.
      When User clicks the Main Menu icon.
      Then User is able to see the below options.
      | My Hive Home   |
      | Manage Devices |
      | Install Devices|
      | Settings       |
      | Help & Support |
      | Logout         |
      When User clicks the Manage Device icon from the menu list.
      Then User should be navigated to the Manage Devices Screen.
      When User clicks on the install devices icon.
      Then User should be navigated to the Install Devices screen
      Then User is able to see the below install options.
      | Add heating zone |
      | Upgrade to Hive 2 |
      | Add another device |
      When User clicks on the All Recipes icon.
      Then User should be navigated to All Recipes Screen.
      When User clicks the Settings icon from main menu page.
      Then User is able to see the below sub settings icons.
       |Geolocation|
       |holiday mode|
       |heating notifications|
       |Account details      |
       |Pin Lock             |
       |Change Password      |
      When User clicks the Help & Support icon from main menu options.
      Then User is able to see the below sub help options.
       |FAQs|
       |Help improve Hive|
       |Service Status   |
       |Text Control     |
      When User clicks on the logout icon.
      Then User should be logged out and navigated to Login Screen.






