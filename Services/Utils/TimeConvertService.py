import re


class TimeConvertService(object):
    minutesInWeek = 60 * 24 * 7
    minutesInDay = 60 * 24
    minutesInHour = 60

    @staticmethod
    def convertFromMinutes(minutes):
        result = ''
        if minutes is None or minutes == 0:
            return '0m'
        minutes = int(minutes)
        weeks = minutes / TimeConvertService.minutesInWeek
        if weeks > 0:
            result += str(weeks) + "w"
            minutes %= TimeConvertService.minutesInWeek
        days = minutes / TimeConvertService.minutesInDay
        if days > 0:
            result += ' ' + str(days) + 'd'
            minutes %= TimeConvertService.minutesInDay
        hours = minutes / TimeConvertService.minutesInHour
        if hours > 0:
            result += ' ' + str(hours) + 'h'
            minutes %= TimeConvertService.minutesInHour
        if minutes > 0:
            result += ' ' + str(minutes) + 'm'
        return result.strip()

    @staticmethod
    def convertToMinutes(string):
        minutes = 0
        wPattern = re.compile('([\d]+)[ ]*w')
        dPattern = re.compile('([\d]+)[ ]*d')
        hPattern = re.compile('([\d]+)[ ]*h')
        mPattern = re.compile('([\d]+)[ ]*m')
        try:
            nrWeeks = int(wPattern.findall(string)[0])
            minutes += nrWeeks * TimeConvertService.minutesInWeek
        except IndexError:
            pass

        try:
            nrDays = int(dPattern.findall(string)[0])
            minutes += nrDays * TimeConvertService.minutesInDay
        except IndexError:
            pass

        try:
            nrDays = int(hPattern.findall(string)[0])
            minutes += nrDays * TimeConvertService.minutesInHour
        except IndexError:
            minutes += 0

        try:
            minutes += int(mPattern.findall(string)[0])
        except IndexError:
            pass

        return minutes
