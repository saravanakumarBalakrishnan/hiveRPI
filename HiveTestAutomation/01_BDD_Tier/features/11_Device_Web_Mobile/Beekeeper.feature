# Created by selvaraj.kuppusamy at 15/01/2017
Feature: Beekeeper Feature file
  # Enter feature description here


    @Beekeeper2 @beekeeperasdfAdminLogin 
  Scenario: Validate Beekeeper AdminLogin() Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When User tries an Admin login via Beekeeper
    #Then Validate the login session and user details returned from Beekeeper

    @Beekeeper2 @beekeeperLogin 
  Scenario: Validating the Beekeeper Login() response
    Given User is logged into Honeycomb via Beekeeper and API 
    Then Validate the login session and user details returned from Beekeeper

    @Beekeeper2 @getDevices 
  Scenario: Validate GetDevices Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When getDevices request is made via Beekeeper 
    Then Validate getDevices response from Beekeeper against the relevant response of API

    @Beekeeper2 @getProducts 
  Scenario: Validating the getProducts() response from Beekeeper 
    Given User is logged into Honeycomb via Beekeeper and API 
    When getProducts request is made via Beekeeper 
    Then Validate getProducts response from Beekeeper against the relevant response of API   

    @Beekeeper2 @getContacts 
  Scenario: Validating the getContacts() response from Beekeeper 
    Given User is logged into Honeycomb via Beekeeper and API 
    When getContacts request is made via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API  

    @Beekeeper2 @addContacts 
  Scenario: Validating the addContacts() response from Beekeeper 
    Given User is logged into Honeycomb via Beekeeper and API 
    When addContacts request is made for any one contact via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API 
    When addContacts request is made for multiple contacts via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API 
    When addContacts request is made for Maximum number of Contacts via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API

  @Beekeeper2 @updateContacts
   Scenario: Validating the updateContacts() response from Beekeeper 
    Given User is logged into Honeycomb via Beekeeper and API 
    When updateContacts request is made for any one contact via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API 
    When updateContacts request is made for multiple contacts via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API 
    When updateContacts request is made for All Contacts via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API

     	@Beekeeper2 @deleteContacts
   Scenario: Validating the deleteContacts() response from Beekeeper 
    Given User is logged into Honeycomb via Beekeeper and API 
    When deleteContacts request is made via Beekeeper 
    Then Validate getContacts response from Beekeeper against the relevant response of API

  @Beekeeper2 @getHolidayMode 
  Scenario: Validate Get Holiday Mode Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When getHolidayMode request is made via Beekeeper 
    Then Validate getHolidayMode response from Beekeeper against the relevant response of API

  @Beekeeper2 @startHolidayMode 
  Scenario: Validate Start Holiday Mode Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When startHolidayMode request is made via Beekeeper 
    Then Validate getHolidayMode response from Beekeeper against the relevant response of API

    @Beekeeper2 @endHolidayMode 
  Scenario: Validate Get Holiday Mode Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When endHolidayMode request is made via Beekeeper 
    Then Validate getHolidayMode response from Beekeeper against the relevant response of API

    @Beekeeper2 @updateNode 
  Scenario: Validate Get Holiday Mode Response
    Given User is logged into Honeycomb via Beekeeper and API 
    When updateNasdfode request is made to set boost as 30 minutes for heating product via Beekeeper
    #Then Validate getHolidayMode response from Beekeeper against the relevant response of API




