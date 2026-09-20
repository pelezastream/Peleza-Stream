#!/usr/bin/env python3
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
required = [
    'settings.gradle', 'build.gradle', 'gradle.properties', 'app/build.gradle',
    'app/src/main/AndroidManifest.xml',
    'app/src/main/java/com/pelezastream/app/MainActivity.java',
    'app/src/main/assets/offline.html',
    '.github/workflows/android-ci.yml',
    '.github/workflows/google-play-release.yml',
]
errors = []
for rel in required:
    if not (ROOT / rel).is_file():
        errors.append(f'missing required file: {rel}')

for rel in ['app/src/main/AndroidManifest.xml', 'app/src/main/res/layout/activity_main.xml',
            'app/src/main/res/values/colors.xml', 'app/src/main/res/values/strings.xml',
            'app/src/main/res/values/themes.xml', 'app/src/main/res/xml/network_security_config.xml']:
    try:
        ET.parse(ROOT / rel)
    except Exception as exc:
        errors.append(f'invalid XML {rel}: {exc}')

build = (ROOT / 'app/build.gradle').read_text(encoding='utf-8')
main = (ROOT / 'app/src/main/java/com/pelezastream/app/MainActivity.java').read_text(encoding='utf-8')
all_text = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in ROOT.rglob('*') if p.is_file() and p.resolve() != Path(__file__).resolve() and p.suffix.lower() in {'.java','.gradle','.xml','.yml','.yaml','.md','.html','.txt','.properties'})

checks = {
    "applicationId 'com.pelezastream.app'": build,
    "namespace 'com.pelezastream.app'": build,
    "compileSdk 36": build,
    "targetSdk 36": build,
    "versionName '1.1.0'": build,
    'https://www.pelezastream.com/': all_text,
    'package com.pelezastream.app;': main,
}
for needle, haystack in checks.items():
    if needle not in haystack:
        errors.append(f'missing expected project setting: {needle}')

if 'pelezastream.top' in all_text.lower():
    errors.append('legacy pelezastream.top URL is still present')

if errors:
    print('Peleza Stream project verification FAILED:')
    for err in errors:
        print(f' - {err}')
    sys.exit(1)

print('Peleza Stream project verification passed.')
print('applicationId: com.pelezastream.app')
print('version: 1.1.0 (110)')
print('home: https://www.pelezastream.com/')
