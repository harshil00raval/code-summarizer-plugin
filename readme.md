# Read Me First
Problem statement : With Given boilerplate code, import statement, comments, logs and alerts
the code base has so much code which is foundationally necessary but not needed for the business function.
This pure tech, non-business code  contains so many words, symbols and spaces that if we pass such files to AI model,
then so much of context window of the model is wasted on non-functional aspects of the code. Given the limitation
of AI Model's context window sizes, we can not upload all code files to the AI Model. This result in blindsided
AI conversations.

Solution : This is an Intellij plugin for Java Spring boot projects which does following things to reduce boilerplate
and non-business code : Remove unwanted symbols, logs, imports, comments, and alerts

# build
$ ./gradlew clean build

# packaging and distribution
$ ./gradlew buildPlugin

# local run and debug - it will open and intellij bound to the command
$ ./gradlew runIde