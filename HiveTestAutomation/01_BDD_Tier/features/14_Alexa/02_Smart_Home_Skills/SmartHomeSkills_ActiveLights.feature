# Created by rajeshwari.srinivasan at 19/07/2017
Feature: Smart Home Skill - Active Light features
  Contains the scenarios for controlling Hive active light via Alexa Smart home skills

  @Alexa_SHS_L01
  Scenario Outline: Alexa_SHS_L01_To verify the turn Off utterance of lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa turn OFF <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to ON state at the client

    Examples:
    | Active Light
    | Tuneable


  @Alexa_SHS_L02
  Scenario Outline: Alexa_SHS_L02_To verify the turn On utterance of lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is OFF state
    When For Lights I say Alexa turn ON <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to OFF state at the client

    Examples:
    | Active Light
    | Tuneable

  @Alexa_SHS_L03
  Scenario Outline: Alexa_SHS_L03_To verify the turn Off utterance of lights
    Given Alexa user is setup with Hive devices and <Active Colour Light > for SmartHome skill validation
    And Rename <Active Colour Light> to DeviceName
    And Check <Active Colour Light> state is ON state
    When For Lights I say Alexa turn OFF <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to ON state at the client

    Examples:
    | Active Light
    | Colour


  @Alexa_SHS_L04
  Scenario Outline: Alexa_SHS_L04_To verify the turn On utterance of lights
    Given Alexa user is setup with Hive devices and <Active Colour Light > for SmartHome skill validation
    And Rename <Active Colour Light> to DeviceName
    And Check <Active Colour Light> state is OFF state
    When For Lights I say Alexa turn ON <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to OFF state at the client

    Examples:
    | Active Light
    | Colour


  @Alexa_SHS_L05
  Scenario Outline: Alexa_SHS_L05_To verify the turn Off utterance of lights
    Given Alexa user is setup with Hive devices and <Active Warm White Light > for SmartHome skill validation
    And Rename <Active Warm White Light> to DeviceName
    And Check <Active Warm White Light> state is ON state
    When For Lights I say Alexa turn OFF <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to ON state at the client

    Examples:
    | Active Light
    | White


  @Alexa_SHS_L06
  Scenario Outline: Alexa_SHS_L06_To verify the turn On utterance of lights
    Given Alexa user is setup with Hive devices and <Active Warm White Light > for SmartHome skill validation
    And Rename <Active Warm White Light> to DeviceName
    And Check <Active Warm White Light> state is OFF state
    When For Lights I say Alexa turn ON <Active Light>
    Then I get a confirmation response from Alexa on lights
    And My light changes to OFF state at the client

    Examples:
    | Active Light
    | White


  @Alexa_SHS_L07
  Scenario Outline: Alexa_SHS_L06_To verify the increase brightness of White lights
    Given Alexa user is setup with Hive devices and <Active Warm White Light > for SmartHome skill validation
    And Rename <Active Warm White Light> to DeviceName
    And Check <Active Warm White Light> state is ON state
    When For Lights I say Alexa set the <Active Light> brightness to 100 percent
    Then I get a confirmation response from Alexa on lights
    And My light changes to 100 brightness at the client

    Examples:
    | Active Light
    | White

  @Alexa_SHS_L08
  Scenario Outline: Alexa_SHS_L06_To verify the decrease brightness of White lights
    Given Alexa user is setup with Hive devices and <Active Warm White Light > for SmartHome skill validation
    And Rename <Active Warm White Light> to DeviceName
    And Check <Active Warm White Light> state is ON state
    When For Lights I say Alexa set the <Active Light> brightness to 20 percent
    Then I get a confirmation response from Alexa on lights
    And My light changes to 20 brightness at the client

    Examples:
    | Active Light
    | White

  @Alexa_SHS_L09
  Scenario Outline: Alexa_SHS_L09_To verify the setting the color temperature of lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa set the <Active Light> to cool white
    Then I get a confirmation response from Alexa on lights
    And My light changes to cool white colour temperature at the client

    Examples:
    | Active Light
    | Tuneable

  @Alexa_SHS_L10
  Scenario Outline: Alexa_SHS_L10_To verify the setting the color temperature of lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa set the <Active Light> to warm white
    Then I get a confirmation response from Alexa on lights
    And My light changes to warm white colour temperature at the client

    Examples:
    | Active Light
    | Tuneable


  @Alexa_SHS_L11
  Scenario Outline: Alexa_SHS_L11_To verify the setting the color temperature of lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa set the <Active Light> to mid white
    Then I get a confirmation response from Alexa on lights
    And My light changes to mid white colour temperature at the client

    Examples:
    | Active Light
    | Tuneable

  @Alexa_SHS_L12
  Scenario Outline: Alexa_SHS_L12_To verify the decrease the brightness of Tuneable lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa set the <Active Light> brightness to 20 percent
    Then I get a confirmation response from Alexa on lights
    And My light changes to 20 brightness at the client

    Examples:
    | Active Light
    | Tuneable

  @Alexa_SHS_L13
  Scenario Outline: Alexa_SHS_L13_To verify the increase the brightness of Tuneable lights
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    And Rename <Active Tuneable Light> to DeviceName
    And Check <Active Tuneable Light> state is ON state
    When For Lights I say Alexa set the <Active Light> brightness to 100 percent
    Then I get a confirmation response from Alexa on lights
    And My light changes to 100 brightness at the client

    Examples:
    | Active Light
    | Tuneable

  @Alexa_SHS_L14
  Scenario Outline: Alexa_SHS_L14_To verify the colour change of Colour lights
    Given Alexa user is setup with Hive devices and <Active Colour Light > for SmartHome skill validation
    And Rename <Active Colour Light> to DeviceName
    And Check <Active Colour Light> state is ON state
    When For Lights I say Alexa set the <Active Light>  to blue
    Then I get a confirmation response from Alexa on lights
    And My light changes to blue color at the client

    Examples:
    | Active Light
    | Colour

  @Alexa_SHS_L15
  Scenario Outline: Alexa_SHS_L15_To verify the colour change of Colour lights
    Given Alexa user is setup with Hive devices and <Active Colour Light > for SmartHome skill validation
    And Rename <Active Colour Light> to DeviceName
    And Check <Active Colour Light> state is ON state
    When For Lights I say Alexa set the <Active Light>  to red
    Then I get a confirmation response from Alexa on lights
    And My light changes to red color at the client

    Examples:
    | Active Light
    | Colour

  @Alexa_SHS_L16
  Scenario Outline: Alexa_SHS_L16_To turn on light with different utterance
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn ON <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L17
  Scenario Outline: Alexa_SHS_L17_To turn off light with different utterance
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn OFF <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L18
  Scenario Outline: Alexa_SHS_L18_To turn on all light with different utterance
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn ON ALL <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L19
  Scenario Outline: Alexa_SHS_L19_To turn off all light with different utterance
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn OFF ALL <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L20
  Scenario Outline: Alexa_SHS_L20_To turn on my light
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn ON MY <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L21
  Scenario Outline: Alexa_SHS_L21_To turn off my light
    Given Alexa user is setup with Hive devices and <Active Tuneable Light > for SmartHome skill validation
    When For Lights I say Alexa turn OFF MY <The Active Light>
    Then I get a confirmation response from Alexa on lights

    Examples:
    | The Active Light
    | light

  @Alexa_SHS_L22
  Scenario Outline: Alexa_SHS_L22_To dim the warm white light brightness
    Given Alexa user is setup with Hive devices and <Active Warm white Light> for SmartHome skill validation
    When The mode and brightness is automatically changed to MANUAL and 5%
    And For Lights brightness I say Alexa dim <Active Light>
    Then I get a confirmation response from Alexa on lights
    Then My light changes to OFF state at the client

    Examples:
    | Active Light
    | light

  @Alexa_SHS_L23
  Scenario Outline: Alexa_SHS_L23_To brighten the warm white light brightness
    Given Alexa user is setup with Hive devices and <Active Warm white Light> for SmartHome skill validation
    When The mode and brightness is automatically changed to MANUAL and 5%
    When For Lights brightness I say Alexa brighten <Active Light>
    Then I get a confirmation response from Alexa on lights
    Then automatically validate the mode and brightness as MANUAL and 30%

    Examples:
    | Active Light
    | light