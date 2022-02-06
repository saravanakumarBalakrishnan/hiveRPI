from FF_testRailAPI import FF_testRailAPI
global caseids

global currentcaseid
global projectid
global suiteid


class testRailConnect:
    global runid
    def __init__(self):

        print('start')
    def addtestrun(self,projectname,suitename,testrailurl,testrailusername,testrailpassword,testrunname):
        print('connecting...')
        client = FF_testRailAPI(testrailurl)
        client.user = testrailusername
        client.password = testrailpassword

        projects =client.send_get('get_projects&is_completed=0')
        for p in projects:
            if p.__getitem__('name') == projectname:
                projectid = p.__getitem__('id')
                self.projectid = projectid
        getsuiteqyr = 'get_suites/' + str(self.projectid)
        suitenames = client.send_get(getsuiteqyr)
        for s in suitenames:
            if s.__getitem__('name') == suitename:
                suiteid = s.__getitem__('id')
                self.suiteid = suiteid
        caseidqry = 'get_cases/' + str(self.projectid) + '&' + 'suite_id=' + str(self.suiteid)
        # lstcaseids = testrailapiconnect.send_get('get_cases/6&suite_id=213')
        lstcaseids = client.send_get(caseidqry)
        self.lstcaseids = lstcaseids
        # context.suiteid=213
        # users = testrailapiconnect.send_get('get_users')
        caseids = []
        automationscenarioids = []
        for c in lstcaseids:
            if c.__getitem__('custom_automated'):
                caseids.append(c.__getitem__('id'))
                automationscenarioids.append(c.__getitem__('custom_automation_scenario_id'))

        testrunadd = client.send_post(
              'add_run/'+str(projectid),
               {'suite_id': suiteid, 'name': testrunname, 'include_all': True, 'case_ids': caseids}
          )

        runid= testrunadd['id']
        #runid =2606
        # context.caseids=caseids--removed

        return runid

    def updatetestrun(self,statusid,runid,currentcaseid,testrailurl,testrailusername,testrailpassword):
        print('connecting...')
        client = FF_testRailAPI(testrailurl)
        client.user = testrailusername
        client.password = testrailpassword
        qry = 'add_result_for_case/' + str(runid) + '/' + str(currentcaseid)
        testupdateresult = client.send_post(qry,
                                                             {'status_id': statusid})