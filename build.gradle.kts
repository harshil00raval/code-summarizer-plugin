plugins {
    id("org.jetbrains.intellij") version "1.17.4"
    id("org.jetbrains.kotlin.jvm") version "1.9.22"
}

group = "com.codesummarizer"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

intellij {
    version.set("2024.3.3")
    type.set("IU")
    plugins.set(listOf("com.intellij.java","PythonCore:243.23654.189"))
//    plugins.set(listOf("com.intellij.java","Pythonid:243.23654.189"))
//    plugins.set(listOf("com.intellij.java","org.jetbrains.kotlin"))

}

tasks {
    buildSearchableOptions {
        enabled = false
    }
    patchPluginXml {
        sinceBuild.set("243")
        untilBuild.set("243.*")
    }
}

kotlin {
    jvmToolchain(17) // or use 11 if needed
}

dependencies {
    implementation("org.python:jython-standalone:2.7.3")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

}