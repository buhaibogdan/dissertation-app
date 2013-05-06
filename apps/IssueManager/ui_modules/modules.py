import tornado.web


class ProjectInfoModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/project_info.html', project="awesome")


class UserLinkModule(tornado.web.UIModule):
    def render(self, user):
        return self.render_string('modules/user_link.html', user=user)


class ProjectSelectModule(tornado.web.UIModule):
    def render(self, projects, js_id):
        return self.render_string('modules/project_select.html', projects=projects, id=js_id)