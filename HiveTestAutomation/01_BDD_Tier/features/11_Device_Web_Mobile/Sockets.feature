# Created by kingston.samselwyn at 06/12/2016

Feature: Contains the scenario to test the Active Light
  
  @SC-SK-SC01-01 @Sockets
  Scenario Outline: SC-SK-SC01-01_Set the given default 'six' event schedule for the given day and verify the same for Active Light
	Given The telegesis is paired with given devices
	When The below <Device> state is changed to <Device State> and validated infinitely
	  | Device State |
	  | ON           |
	  | OFF          |
	
	Examples:
	  | Device  |
	  | HAS01UK |