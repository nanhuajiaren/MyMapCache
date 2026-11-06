import PyInstaller.__main__
print('-' * 30)
PyInstaller.__main__.run([
    'i_dont_know_but_this_works.spec', '--clean'
])
print('-' * 30)
PyInstaller.__main__.run([
    'MyMapCache.spec', '--clean'
])
print('-' * 30)
PyInstaller.__main__.run([
    'MyMapCache-private.spec', '--clean'
])