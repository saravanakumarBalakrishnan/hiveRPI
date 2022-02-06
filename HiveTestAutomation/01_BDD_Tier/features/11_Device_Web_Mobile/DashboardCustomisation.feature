#Created on 24 Feb 2017

#@authors:
#iOS        - Meenakshi
#Android    - Sivakumar
#Web        - TBD

################### Variable Definitions #######################################################
# DeviceName	   - The name of the primary device in the User account used for customisation
# SwapDeviceName   - The name of the secondary device in the User account used for swapping operations
# Heating          - Name given for the Heating in the User Account
# Motion Sensor    - Name given for the Motion Sensor in the User Account
################################################################################################

Feature: Validate various features of Dashboard Customisation

    @SC-DC_01 @DashboardCustomisation @C194509
    Scenario Outline: SC-DC_01_Validate When a user is Adding a device on dashboard cell
    Given The <DeviceName> is paired with the user account
    When User navigates to the dashboard screen and long presses on the device cell
    Then Edit mode should be initiated with cell displaying X on it
    When User taps on Add button
    Then User should be able to add the device from list view and save it

      Examples:
		|DeviceName    |
		|Heating       |

    @SC-DC_02 @DashboardCustomisation @C194511
    Scenario Outline: SC-DC_02_Validate When a user is Cancelling the changes in dashboard
    Given The <DeviceName> is paired with the user account
    When User navigates to the dashboard screen and long presses on the device cell
    Then Edit mode should be initiated with cell displaying X on it
    When User taps on X of device cell on dashboard screen
    Then Device should disappear from the dashboard
    When User taps on Cancel button
    Then Changes should be reverted and edit mode should be exited

      Examples:
		|DeviceName   |
		|Heating      |

    @SC-DC_03 @DashboardCustomisation @C194513 @C215053
    Scenario Outline: SC-DC_03_Validate When a user is Removing an item from the dashboard
    Given The <DeviceName> is paired with the user account
    When User navigates to the dashboard screen and long presses on the device cell
    Then Edit mode should be initiated with cell displaying X on it
    When User taps on X of device cell on dashboard screen
    Then Device should disappear from the dashboard
    When User taps on Save button
    Then Changes should be saved and edit mode should be exited

      Examples:
		|DeviceName   |
		|Heating      |

    @SC-DC_04 @DashboardCustomisation @C194512
    Scenario Outline: SC-DC_04_Validate When a user is Repositioning device cell on dashboard
    Given The <DeviceName> is paired with the user account
    When User navigates to the dashboard screen and long presses on the device cell
    Then Edit mode should be initiated with cell displaying X on it
    When User selects and drags a device to another device <SwapDeviceName> cell
    And User taps on Save button
    Then Devices should be swapped and edit mode should be exited

        Examples:
		|DeviceName |SwapDeviceName  |
		|Plug 1     |Motion sensor   |

# ---------Android only----------------#
    #When User taps on X of device cell on dashboard screen will be 'Remove' at the leftmost botton corner where user can drop the cell for deletion
 # ---------Android only----------------#