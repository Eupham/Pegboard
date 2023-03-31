#!/bin/bash


####
# file: helloworldapk.sh
# drafted by:Evan Upham; evan.upham@outlook.com; https://uphamprojects.com; https://github.com/Eupham/Pegboard.git
# created: 3/30/2023
# revised: 3/30/2023
# reminder: chmod +x helloworldapk.sh
# Attempt at creating a mobile app
#!/bin/bash

# Define project directory
PROJECT_NAME="MyKotlinApp"
PROJECT_DIR="${HOME}/projects/${PROJECT_NAME}"

# Create project directory
mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

# Initialize Gradle project
gradle init --type kotlin-library

# Create Kotlin source directory
mkdir -p src/main/kotlin

# Create main Kotlin file
cat << EOF > src/main/kotlin/Main.kt
fun main() {
    println("Hello, Kotlin!")
}
EOF

# Create VS Code workspace file
cat << EOF > ${PROJECT_NAME}.code-workspace
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "kotlin.configuration.language.version": "1.5"
    },
    "extensions": {
        "recommendations": [
            "mathiasfrohlich.Kotlin",
            "vscjava.vscode-java-debug",
            "vscjava.vscode-java-test"
        ]
    }
}
EOF

# Open project in VS Code
code "${PROJECT_DIR}"
