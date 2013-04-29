import tornado.web

class ProjectInfoModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/project_info.html', project="awesome")


class UserLinkModule(tornado.web.UIModule):
    def render(self, user):
        if 'uid' in user and 'username' in user:
            return self.render_string('modules/user_link.html', user=user)
        return ''