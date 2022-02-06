# Created by Rajeshwari.Srinivasan at 06/07/2017
Feature: SmartHome Skills - Active Plugs
  Contains the scenarios that controls active plugs using voice - Alexa


  @Alexa_SHS_P01
  Scenario Outline: @Alexa_SHS_P01_TurnON_plug
   Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    And Rename <Active Plug> to DeviceName
    And  Whether DeviceName state is OFF state
    When I say Alexa turn ON <Active Plug>
    Then I get a confirmation response from Alexa
    And My device changes to ON state at the client


    Examples:
    | Active Plug
    | Plug


  @Alexa_SHS_P02
  Scenario Outline: @Alexa_SHS_P02_TurnOFF_plug
    Given Alexa user is setup with Hive devices and <Active Plug OFF> for SmartHome skill validation
    And Rename <Active Plug OFF> to DeviceName
    And Whether DeviceName state is ON state
    When I say Alexa turn OFF <Active Plug OFF>
    Then I get a confirmation response from Alexa
    And My device changes to OFF state at the client

    Examples:
    | Active Plug OFF
    | Plug


  @Alexa_SHS_P03
  Scenario Outline: @Alexa_SHS_P03_TurnON_invalidplug
    Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    And Rename <Active Plug> to invalid DeviceName
    When I say Alexa turn ON <Active Plug>
    Then I get a confirmation response from Alexa


    Examples:
    | Active Plug
    | Plug


  @Alexa_SHS_P04
  Scenario Outline: @Alexa_SHS_P04_TurnOFF_invalidplug
    Given Alexa user is setup with Hive devices and <Active Plug OFF> for SmartHome skill validation
    And Rename <Active Plug OFF> to invalid DeviceName
    When I say Alexa turn OFF <Active Plug OFF>
    Then I get a confirmation response from Alexa


    Examples:
    | Active Plug OFF
    | Plug


  @Alexa_SHS_P05
  Scenario Outline: @Alexa_SHS_P05_TurnON_plug_already_plugON
   Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    And Rename <Active Plug> to DeviceName
    When I say Alexa turn ON <Active Plug>
    Then I get a confirmation response from Alexa
    And My device changes to ON state at the client


    Examples:
    | Active Plug
    | Plug


  @Alexa_SHS_P06
  Scenario Outline: @Alexa_SHS_P06_TurnOFF_plug_already_plugOFF
    Given Alexa user is setup with Hive devices and <Active Plug OFF> for SmartHome skill validation
    And Rename <Active Plug OFF> to DeviceName
    When I say Alexa turn OFF <Active Plug OFF>
    Then I get a confirmation response from Alexa
    And My device changes to OFF state at the client

    Examples:
    | Active Plug OFF
    | Plug


  @Alexa_SHS_P07
  Scenario Outline: @Alexa_SHS_P07_TurnON_all_plug
    Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    When I say Alexa turn ON <ALL Active Plug>
    Then I get a confirmation response from Alexa

    Examples:
    | ALL Active Plug | Active Plug
    | all Plug            | Plug


  @Alexa_SHS_P08
  Scenario Outline: @Alexa_SHS_P08_TurnOFF_all_plug
    Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    When I say Alexa turn OFF <ALL Active Plug>
    Then I get a confirmation response from Alexa

    Examples:
    | ALL Active Plug | Active Plug
    | all Plug            | Plug


  @Alexa_SHS_P09
  Scenario Outline: @Alexa_SHS_P09_TurnON_my_plug
    Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    When I say Alexa turn ON <MY Active Plug>
    Then I get a confirmation response from Alexa

    Examples:
    | MY Active Plug | Active Plug
    | my Plug            | Plug


  @Alexa_SHS_P010
  Scenario Outline: @Alexa_SHS_P10_TurnOFF_my_plug
    Given Alexa user is setup with Hive devices and <Active Plug> for SmartHome skill validation
    When I say Alexa turn OFF <MY Active Plug>
    Then I get a confirmation response from Alexa

    Examples:
    | MY Active Plug | Active Plug
    | my Plug            | Plug

  