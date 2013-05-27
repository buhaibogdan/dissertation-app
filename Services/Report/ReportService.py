import json
from Services.Host.HostService import hostService
from collections import Counter
from Services.Utils.TimeConvertService import TimeConvertService
from time import sleep
from fpdf import FPDF


class ReportService(object):
    def createReportForProject(self, pid):
        if pid == 0 or pid is None:
            return ''

        project = hostService.projectService.getProject(pid)
        userProjectEntities = hostService.userProjectService.getUsersForProject(pid)
        usersInvolved = []
        for user in userProjectEntities:
            usersInvolved.append(user.users.username)
        tasks = hostService.taskService.getTasksForProject(pid)
        nrTasksClosed = len(hostService.taskService.getTasksClosedForProject(pid))
        nrTasksInProgress = len(hostService.taskService.getTasksForProject(pid))
        nrTasksToDO = len(hostService.taskService.getTasksToDoForProject(pid))
        projectHistory = hostService.historyService.getProjectHistory(pid)
        timeRemaining = 0
        totalTime = 0
        # compute time
        for task in tasks:
            timeRemaining += TimeConvertService.convertToMinutes(task.minutes_remaining)
            totalTime += TimeConvertService.convertToMinutes(task.minutes_estimated)

        timeLogged = totalTime - timeRemaining
        users = []
        for event in projectHistory:
            users.append(event.user.username)
        # get fist element
        activeUser = Counter(users).most_common(1)[0][0]
        return {
            'pid': pid,
            'title': project.title,
            'users': usersInvolved,
            'nrTasksClosed': nrTasksClosed,
            'nrTasksInProgress': nrTasksInProgress,
            'nrTasksToDO': nrTasksToDO,
            'mostActive': activeUser,
            'timeRemaining': TimeConvertService.convertFromMinutes(timeRemaining),
            'timeLogged': TimeConvertService.convertFromMinutes(timeLogged)
        }

    def createGeneralReport(self):
        print "Generating general report..."
        sleep(3)
        print "finished."

    def createUserReport(self):
        print "Generating user report..."
        sleep(3)
        print 'finished.'

    def createReportForProjectPDF(self, pid):
        data = self.createReportForProject(pid)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(40, 10, data['title'])
        pdf.set_font('Arial', size=12)
        pdf.multi_cell(w=0, h=10, txt='')
        pdf.multi_cell(0, 5, 'Users involved in project: ')
        for user in data['users']:
            pdf.multi_cell(0, 5, txt=" - " + user)
        pdf.multi_cell(0, 5, 'Tasks closed: ' + str(data['nrTasksClosed']))
        pdf.multi_cell(0, 5, 'Tasks in progress: ' + str(data['nrTasksInProgress']))
        pdf.multi_cell(0, 5, 'Tasks to do: ' + str(data['nrTasksToDO']))
        pdf.multi_cell(0, 5, 'Most active user is: ' + str(data['mostActive']))
        pdf.multi_cell(0, 5, 'Total time logged: ' + str(data['timeLogged']))
        pdf.multi_cell(0, 5, 'Time remaining for tasks: ' + str(data['timeRemaining']))
        sleep(2)
        pdf.output('generated_reports/project_' + pid + '_report.pdf', 'F')
