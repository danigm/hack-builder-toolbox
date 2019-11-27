conf = configuration_data()
conf.set('bindir', join_paths(get_option('prefix'), get_option('bindir')))

appstream_file = configure_file(
  input: 'com.hack_computer.BuilderToolbox.appdata.xml.in',
  output: 'com.hack_computer.BuilderToolbox.appdata.xml',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata'),
  configuration: conf
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

configure_file(
    input: 'com.hack_computer.BuilderToolbox.service.in',
    output: 'com.hack_computer.BuilderToolbox.service',
    install: true,
    install_dir: join_paths(get_option('datadir'), 'dbus-1', 'services'),
    configuration: conf
)
