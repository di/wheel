from wheel.metadata import pkginfo_to_metadata


def test_pkginfo_to_metadata(tmpdir):
    expected_metadata = [
        ('Metadata-Version', '2.1'),
        ('Name', 'spam'),
        ('Version', '0.1'),
        ('Requires-Dist', "pip @ https://github.com/pypa/pip/archive/1.3.1.zip"),
        ('Provides-Extra', ''),
        ('Requires-Dist', 'foobar; extra == \'\''),
        ('Requires-Dist', 'pywin32; (sys_platform=="win32") and extra == \'\''),
        ('Provides-Extra', 'signatures'),
        ('Requires-Dist', 'pyxdg; (sys_platform!="win32") and extra == \'signatures\''),
        ('Provides-Extra', 'empty_extra'),
        ('Provides-Extra', 'faster-signatures'),
        ('Requires-Dist', "ed25519ll; extra == 'faster-signatures'"),
        ('Provides-Extra', 'rest'),
        ('Requires-Dist', "docutils (>=0.8); extra == 'rest'"),
        ('Requires-Dist', "keyring; extra == 'signatures'"),
        ('Requires-Dist', "keyrings.alt; extra == 'signatures'"),
        ('Provides-Extra', 'test'),
        ('Requires-Dist', "pytest (>=3.0.0); extra == 'test'"),
        ('Requires-Dist', "pytest-cov; extra == 'test'"),
    ]

    pkg_info = tmpdir.join('PKG-INFO')
    pkg_info.write("""\
Metadata-Version: 0.0
Name: spam
Version: 0.1
Provides-Extra: empty+extra
Provides-Extra: test
Provides-Extra: reST
Provides-Extra: signatures
Provides-Extra: Signatures
Provides-Extra: faster-signatures""")

    egg_info_dir = tmpdir.ensure_dir('test.egg-info')
    egg_info_dir.join('requires.txt').write("""\
pip@https://github.com/pypa/pip/archive/1.3.1.zip

[empty+extra]

[]
foobar

[:sys_platform=="win32"]
pywin32

[faster-signatures]
ed25519ll

[reST]
docutils>=0.8

[signatures]
keyring
keyrings.alt

[Signatures:sys_platform!="win32"]
pyxdg

[test]
pytest>=3.0.0
pytest-cov""")

    message = pkginfo_to_metadata(egg_info_path=str(egg_info_dir), pkginfo_path=str(pkg_info))
    assert message.items() == expected_metadata
