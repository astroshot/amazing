# coding=utf-8

from src.web.handler import AllowCrossDomainHandler


class UploadImagesHandler(AllowCrossDomainHandler):
    def post(self):
        file_infos = []
        names = []
        for key in self.request.files.keys():
            img_file = self.request.files[key][0]
            file_infos.append(img_file)
            names.append(img_file['filename'])

        # filename = file_info['filename'].upper()
        # file_extension = get_file_extension(filename)
        # file_content = file_info['body']
        self.render_json({
            'status': 'success',
            'msg': u'上传成功',
            'names': names,
        })
