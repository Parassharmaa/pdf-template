import os
import tempfile
from subprocess import PIPE, run

from django.conf import settings
from django.template.loader import render_to_string

class Chrome(object):
    """ rendering html with chrome """

    def _prepare(self, html):
        """ alter html render properly """
        html = html.replace(
            '/static/',
            'file://{}/'.format(settings.STATIC_ROOT))
        html = html.replace(
            '"/media/',
            '"file://{}/'.format(os.path.join(
                settings.BASE_DIR, settings.MEDIA_ROOT)))

        print(html)
        return html

    def render(self, html, landscape=False, margin='0px', file_type='pdf'):

        html = self._prepare(html)

        with tempfile.NamedTemporaryFile(suffix=f'.html', mode='w+t') as tmpsrc:
            with tempfile.NamedTemporaryFile(suffix=f'.{file_type}') as tmpout:
                tmpsrc.write(html)
                tmpsrc.flush()

                # render into filename.pdf. use px and zoom to make high qualy
                # images
                binary = getattr(settings, 'CHROME_BINARY', 'chromedriver')
                size = (landscape and '{}mm*{}mm'.format(297, 210) or
                        '{}mm*{}mm'.format(210, 297))

                args = [binary,
                        "--headless",
                        "--disable-gpu",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        f"--print-to-pdf={tmpout.name}",
                        tmpsrc.name,
                       
                        ]
                print(" ".join(args))
                res = run(args, stdout=PIPE, stderr=PIPE,
                          universal_newlines=True)
                print(res)
                if res.returncode:
                    print(res.returncode, res.stdout, res.stderr)

                tmpout.flush()
                tmpout.seek(0)
                content = tmpout.read()

        return content

    def render_template(self, template_name, context, landscape=False,
                        margin='0px'):
        html = render_to_string(template_name, context)
        return self.render(html, landscape, margin)

    def render_html(self, template_name, context, landscape=False,
                        margin='0px'):
        html = render_to_string(template_name, context)
        return html
