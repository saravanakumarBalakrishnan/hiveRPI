from copy import copy
import random
class Troubleshooting(object):
    def __init__(self):
        self.questions = {}
        self.numeberOfQuestion = 0
        self.nextQuestionID = None
        self.nextAction = None
        self.prevQuestionID = None

        self.currentQuestion = None
        self.currentQuestionID = None
        self.currentQuestionText = None
        self.progress = None
        self.answersDict = None
        self.answers = []
        #Total 9 scenarios involving High and Low
        self.ActionsDict = {'CALL PLUMBER':'call-plumber','I CAN FIX':'i-can-fix','IGNORE':'ignore'}
        self.paths = {}
        self.action_path =None

    def loadQuestions(self, endpoint):
        #End point is not ready yet
        lowQuestions = {"id": 1,
                          "text": "Check if any taps, including outside ones, are slowly dripping. Is that the problem?",
                          "progress": 0.1, "next": [{"answer": "Yes", "step": 2}, {"answer": "No", "step": 4}]}, {
                             "id": 2, "text": "Are you able to fix it or would you like to call a plumber?",
                             "progress": 0.8, "next": [{"answer": "I can fix it", "step": 3},
                                                       {"answer": "Call a plumber", "action": "call-plumber"}]}, {
                             "id": 3,
                             "text": "Great, we will notify you again if we notice anything out of the ordinary.",
                             "progress": 1.0, "next": [{"answer": "OK", "action": "i-can-fix"}]}, {"id": 4,
                                                                                                   "text": "Some toilets can slowly drip after flushing. Are any of your toilets dripping?",
                                                                                                   "progress": 0.2,
                                                                                                   "next": [
                                                                                                       {"answer": "Yes",
                                                                                                        "step": 2},
                                                                                                       {"answer": "No",
                                                                                                        "step": 5}]}, {
                             "id": 5, "text": "Can you see any water dripping from exposed pipework?", "progress": 0.3,
                             "next": [{"answer": "Yes", "step": 2}, {"answer": "No", "step": 6}]}, {"id": 6,
                                                                                                    "text": "Check around your appliances. Are you able to see any water dripping?",
                                                                                                    "progress": 0.4,
                                                                                                    "next": [{
                                                                                                                 "answer": "Yes",
                                                                                                                 "step": 2},
                                                                                                             {
                                                                                                                 "answer": "No",
                                                                                                                 "step": 7}]}, {
                             "id": 7, "text": "Do you have a water meter?", "progress": 0.5,
                             "next": [{"answer": "Yes", "step": 8}, {"answer": "No", "step": 9}]}, {"id": 8,
                                                                                                    "text": "If you are not using any water in your home, is the dial indicator turning?",
                                                                                                    "progress": 0.6,
                                                                                                    "next": [{
                                                                                                                 "answer": "Yes",
                                                                                                                 "action": "call-plumber"},
                                                                                                             {
                                                                                                                 "answer": "No",
                                                                                                                 "step": 9}]}, {
                             "id": 9,
                             "text": "Sometimes drips can be intermittent from things like toilet valves and valves to water tanks in lofts. How can we help you now?",
                             "progress": 0.7, "next": [{"answer": "Call a plumber", "action": "call-plumber"},
                                                       {"answer": "Ignore for now", "step": 10}]}, {"id": 10,
                                                                                                    "text": "Ok, we will notify you if we continue to see a small water flow.",
                                                                                                    "progress": 1.0,
                                                                                                    "next": [{
                                                                                                                 "answer": "Thanks",
                                                                                                                 "action": "finish"}]}
        highQuestions = {"id": 1, "text": "Has anyone in your home recently taken a long shower?", "progress": 0.1,
                         "next": [{"answer": "Yes", "step": 2}, {"answer": "No", "step": 3}]}, {"id": 2,
                                                                                                "text": "Great, thanks! We will notify you if we notice anything out of the ordinary.",
                                                                                                "progress": 1.0,
                                                                                                "next": [
                                                                                                    {"answer": "OK",
                                                                                                     "action": "finish"}]}, {
                            "id": 3,
                            "text": "Check if any taps, including outside ones, have been left running. If so, please shut them off.",
                            "progress": 0.2, "next": [{"answer": "That was the problem", "step": 2},
                                                      {"answer": "That's not the problem", "step": 4}]}, {"id": 4,
                                                                                                            "text": "Some toilets can continue to fill after flushing. Can you hear water running from any of your toilets?",
                                                                                                            "progress": 0.4,
                                                                                                            "next": [{
                                                                                                                         "answer": "Yes",
                                                                                                                         "step": 5},
                                                                                                                     {
                                                                                                                         "answer": "No",
                                                                                                                         "step": 6}]}, {
                            "id": 5, "text": "Are you able to fix it or would you like to call a plumber?",
                            "progress": 0.9, "next": [{"answer": "I can fix it", "step": 12},
                                                      {"answer": "Call a plumber", "action": "call-plumber"}]}, {
                            "id": 6, "text": "Can you see any water around any appliances?", "progress": 0.5,
                            "next": [{"answer": "Yes", "step": 5}, {"answer": "No", "step": 7}]}, {"id": 7,
                                                                                                   "text": "Do you have any water tanks in your loft?",
                                                                                                   "progress": 0.6,
                                                                                                   "next": [
                                                                                                       {"answer": "Yes",
                                                                                                        "step": 8},
                                                                                                       {"answer": "No",
                                                                                                        "step": 9}, {
                                                                                                           "answer": "Not sure",
                                                                                                           "step": 9}]}, {
                            "id": 8,
                            "text": "Ball valves can sometimes continuously run into the water tank. Are you able to check?",
                            "progress": 0.7, "next": [{"answer": "Yes", "step": 10}, {"answer": "No", "step": 9}]}, {
                            "id": 9, "text": "Would you like to call a plumber?", "progress": 0.9,
                            "next": [{"answer": "Yes", "action": "call-plumber"}, {"answer": "No", "step": 11}]}, {
                            "id": 10, "text": "Did you find the problem?", "progress": 0.8,
                            "next": [{"answer": "Yes", "step": 5}, {"answer": "No", "step": 9}]}, {"id": 11,
                                                                                                   "text": "Ok, we'll continue to monitor your water supply over the next 24 hours and let you know if we notice anything out of the ordinary.",
                                                                                                   "progress": 1.0,
                                                                                                   "next": [
                                                                                                       {"answer": "OK",
                                                                                                        "action": "finish"}]}, {
                            "id": 12,
                            "text": "Great, thanks! We will notify you if we notice anything out of the ordinary.",
                            "progress": 1.0, "next": [{"answer": "OK", "action": "i-can-fix"}]}

        if 'SMALL' in endpoint.upper() or 'LOW' in endpoint.upper():
            self.questions = lowQuestions
        else: self.questions = highQuestions
    def nextQuestion(self,answer):
        for eachAnswer in self.answersDict:
            self.nextQuestionID = None
            self.nextAction = None
            if eachAnswer['text'] == answer :
                if 'action' in eachAnswer.keys():
                    self.nextAction = eachAnswer['action']
                if 'next' in eachAnswer.keys():
                    self.nextQuestionID = eachAnswer['next']
            self.prevQuestionID = self.currentQuestionID

    def currentQuestionDetails (self):
        for eachQuestion in self.questions:
            if eachQuestion['id'] == self.currentQuestionID:
                self.currentQuestion = eachQuestion
                self.currentQuestionText = eachQuestion['text']
                self.progress = eachQuestion['progress']
                self.answersDict = eachQuestion['answers'][0]
                self.answers = None
                for eachItem in self.answersDict :
                    self.answers.append(eachItem['text'])

    def find_action_path(self, action):
        finalAction = self.ActionsDict[action]
        action_paths = self.find_action_paths(finalAction)
        randomPathIndex = random.sample(range(1, len(action_paths)+1), 1)[0]
        self.action_path = action_paths[randomPathIndex-1][1:]


    def findPaths(self):

        parentIndex= 0
        parentQuestion = self.questions[parentIndex]
        parentId =  parentQuestion['id']

        self.Index = 1
        parentTuple = {self.Index:{'Path':['Root'],'NodeID':parentId}}
        self.paths.update({parentId:['Root']})
        self.exploreGraph([parentTuple])

    def exploreGraph(self,unexplored_stack):
        question = None
        while unexplored_stack != []:
            childs = None
            currentNode = unexplored_stack.pop()
            currentPath = list(currentNode.values())[0]['Path']
            for eachQuestion in self.questions:
                if eachQuestion['id'] == list(currentNode.values())[0]['NodeID']:
                    childs = eachQuestion['next']
                    question = eachQuestion['text']
                    break
            for eachChild in childs:
                answer = eachChild['answer']
                newPath = copy(currentPath)
                newPath.append({'question':question,'answer':answer})
                self.Index+=1
                next = None
                if 'action' in eachChild.keys():
                    next = eachChild['action']
                if 'step' in eachChild.keys():
                    next = eachChild['step']
                    dictItem = {self.Index: {'Path': newPath, 'NodeID': next}}
                    unexplored_stack.append(dictItem)
                self.updatePathDictionary(newPath, next)


    def updatePathDictionary(self,Path, destination):
        if destination in self.paths.keys():
            tempValue = self.paths[destination]
            tempValue.append(Path)
            self.paths.update({destination:tempValue})
        else:
            self.paths.update({destination:[Path]})

    def fetchQuestion (self, questionID):
        for eachQuestion in self.questions:
            if eachQuestion['id'] == questionID:
                return eachQuestion

    def find_action_paths(self,finalAction):
        return self.paths[finalAction]
