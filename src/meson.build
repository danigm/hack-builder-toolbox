pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'hack_builder_toolbox')
gnome = import('gnome')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'hack-builder-toolbox.in',
  output: 'hack-builder-toolbox',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

sources = [
  '__init__.py',
  'main.py'
]

install_data(sources, install_dir: moduledir)
