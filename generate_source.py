import os
import shutil
import subprocess

here = os.path.dirname(os.path.abspath(__file__))
project_dir = here
destination_js = f'{project_dir}/js/lib/generated'
destination_python = f'{project_dir}/ipyvuetify/generated'
widget_gen_schema = f'{project_dir}/js/gen-source/widget_gen_schema.json'

widgetgen = f'{project_dir}/js/node_modules/.bin/widgetgen'

es6_template = f'{project_dir}/js/gen-source/es6-template.njk'
python_template = f'{project_dir}/js/gen-source/python.njk'


def reset_dir(name):
    if os.path.isdir(name):
        shutil.rmtree(name)

    os.mkdir(name)


reset_dir(destination_js)
subprocess.check_call(f'{widgetgen} -p json -o {destination_js} -t {es6_template} {widget_gen_schema} es6', shell=True)

reset_dir(destination_python)
subprocess.check_call(f'{widgetgen} -p json -o {destination_python} -t {python_template} {widget_gen_schema} python', shell=True)

# Fixme: Can't specify default value for any in widget-gen
with open(f'{destination_python}/VuetifyWidget.py', "r+") as f:
    new_content = f.read().replace(
        'v_model = Any(Undefined).tag(sync=True)',
        'v_model = Any("!!disabled!!").tag(sync=True)')

    f.seek(0)
    f.write(new_content)