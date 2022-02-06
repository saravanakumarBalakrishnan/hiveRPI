"""
Created on 22 May 2015

@author: ranganathan.veluswamy
"""
from behave import *


@given(u'User is logged into Honeycomb via {strNodeType}')
def systemLogin(context, strNodeType):
    print("Getting started with Beekeeper")
    if strNodeType.upper().find('BEEKEEPER') >= 0:
        context.oThermostatEP = context.oThermostatClass.beekeeperEP
    else:
        print("Feature File is not right - please check")
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Logging into API and Beekeeper')
    context.oThermostatEP.beeUpdate(context)


@when('{strRequest} request is made via Beekeeper')
def requestBeekeeperAndAPI(context, strRequest, strServerName="isopProd"):
    context.rFM.setBeeRequest(context, strRequest, strServerName)


@when('{strRequest} request is made for {strContact} via Beekeeper')
def requestBeekeeperAndAPIForPutRequest(context, strRequest, strContact, strServerName="isopProd"):
    if strContact.upper().find('ONE') >= 0:
        strContact = True
    elif strContact.upper().find('MULTIPLE') >= 0:
        strContact = False
    elif strContact.upper().find('ALL') >= 0:
        strContact = None
    elif strContact.upper().find('MAXIMUM') >= 0:
        strContact = None
    context.rFM.setBeeRequest(context, strRequest, strServerName, strContact)


@when('User tries an {strLoginType} via Beekeeper')
def requestBeekeeperAndAPIforLogin(context, strLoginType):
    if strLoginType.upper().find('ADMIN LOGIN') >= 0: strLoginType = 'ADMIN'
    context.rFM.setAdminLoginRequest(context, strLoginType)


@when('{strRequest} request is made to set {oAttribute} as {oTargetValue} for {oType} Product via Beekeeper')
def requestBeekeeperforUpdate(context, strRequest, oAttribute, oTargetValue, oType, strServerName="isopProd"):
    if oTargetValue.upper().find('MINUTES') >= 0:
        oTargetValue = int(oTargetValue[:-8]) - 1
    elif oTargetValue.upper().find('HOUR') >= 0:
        oTargetValue = [int(oTargetValue[:-5]) * 60] - 1
    elif oTargetValue.upper().find('DEGREE') >= 0:
        oTargetValue = int(oTargetValue[:-8])

    # if oAttribute

    context.rFM.setBeeRequest(context, strRequest, strServerName, oAttribute, oTargetValue, oType)


@then('Validate {strRequest} response from Beekeeper against the relevant response of API')
def validateBeekeeperResponse(context, strRequest, strServerName="isopProd"):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating Beekeeper Response data against API')
    context.rFM.ValidateBeeResponse(context, strRequest, strServerName)


@then('Validate the {strRequest} returned from Beekeeper')
def ValidateUserdetailsAndLogin(context, strRequest, strServerName="isopProd"):
    context.reporter.HTML_TC_BusFlowKeyword_Initialize('Validating Beekeeper login and User details against API')
    if strRequest.upper().find('SESSION AND USER') >= 0: strRequest = 'ValidateUserDetails'
    context.rFM.ValidateBeeResponse(context, strRequest, strServerName)
