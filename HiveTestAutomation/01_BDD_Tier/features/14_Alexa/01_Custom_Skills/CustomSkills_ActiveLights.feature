# Created by sri.gunasekaran at 08/04/2017
Feature: Custom Skill - Active Light features
  Contains the scenarios for controlling Hive active light via Alexa custom skills

  @Alexa_CS_L01
  Scenario Outline: Alexa_CS_L01_To verify the turn Off utterance of lights
    Given Alexa user is setup with Hive hub and <Active Light> for Custom skill validation
    And <Active Light> is renamed to <Device Name>
    And <Device Name> is in ON state
    When I say Alexa tell <Invocation Name> to turn OFF the <Device Name>
    Then I get a confirmation response from Alexa
    And my <Device Name> changes to OFF state

    Examples:
    | Active Light     | Device Name | Invocation Name |
    | Warm White Light | Bedroom     | Hive            |