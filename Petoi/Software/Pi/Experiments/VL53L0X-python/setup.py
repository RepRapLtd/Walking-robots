from setuptools import setup, Extension

extension = Extension(
    'vl53l0x_python',
    define_macros=[],
    include_dirs=['.', 'Api/core/inc', 'platform/inc'],
    libraries=[],
    library_dirs=[],
    sources=['Api/core/src/vl53l0x_api_calibration.c',
             'Api/core/src/vl53l0x_api_core.c',
             'Api/core/src/vl53l0x_api_ranging.c',
             'Api/core/src/vl53l0x_api_strings.c',
             'Api/core/src/vl53l0x_api.c',
             'platform/src/vl53l0x_platform.c',
             'python_lib/vl53l0x_python.c'])

setup(name='VL53L0X',
      version='1.0.4',
      description='VL53L0X sensor for raspberry PI/JetsonTX2',
      # author='?',
      # author_email='?',
      url='https://github.com/pimoroni/VL53L0X-python',
      long_description='''
VL53L0X sensor for raspberry PI/JetsonTX2.
''',
      ext_modules=[extension],
      package_dir={'': 'python'},
      py_modules=['VL53L0X'],
      requires=['smbus' or 'smbus2'])
