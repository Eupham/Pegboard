#!/bin/bash
set -euo pipefail

####
# file: helloworldapk.sh
# drafted by: Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/30/2023
# revised: 3/30/2023
# reminder: chmod +x helloworldapk.sh
# warning: This script hasn't been tested yet
# This script sets up mobile dev dependencies

# Create a new React Native project
react-native init HelloWorld

# Change into the project directory
cd HelloWorld

# Build and run the project on an Android emulator or connected device
react-native run-android

# Open the project in Visual Studio Code
code .

# Replace the contents of App.js with "Hello, world!" code
echo -e "import React from 'react';\nimport { StyleSheet, Text, View } from 'react-native';\n\nexport default function App() {\n  return (\n    <View style={styles.container}>\n      <Text style={styles.text}>Hello, world!</Text>\n    </View>\n  );\n}\n\nconst styles = StyleSheet.create({\n  container: {\n    flex: 1,\n    backgroundColor: '#fff',\n    alignItems: 'center',\n    justifyContent: 'center',\n  },\n  text: {\n    fontSize: 24,\n    fontWeight: 'bold',\n  },\n});\n" > src/App.js

# Build an unsigned APK file
cd android && ./gradlew assembleDebug