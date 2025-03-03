package com.codesummarizer.summarizer

import com.codesummarizer.model.CleaningConfig
import org.python.core.PyObject
import org.python.core.PyDictionary  // Add this
import org.python.core.PyString      // Add this
import org.python.util.PythonInterpreter
import java.io.File

class PythonCodeSummarizer {
    private val interpreter: PythonInterpreter
    private val summarizer: PyObject

    init {
        // Load Python code
//        val pythonCode = File("src/main/resources/python/code_summarizer.py").readText()
//        val pythonCode = File("python/code_summarizer.py").readText()

        val pythonResource = this.javaClass.classLoader.getResourceAsStream("python/code_summarizer.py")
        val pythonCode = pythonResource?.bufferedReader()?.use { it.readText() }
            ?: throw IllegalStateException("Failed to load python/code_summarizer.py from resources")

        interpreter = PythonInterpreter()
        interpreter.exec(pythonCode)

        // Create instance of Python class
        val summarizerClass = interpreter.get("AdvancedCodeSummarizer")
        summarizer = summarizerClass.__call__()
    }

    fun process_file(content: String, language: String, config: CleaningConfig): Map<String, Any> {
        // Convert parameters to PyObjects
        val pyContent = PyString(content)
        val pyLanguage = PyString(language)

        // Create Python dictionary for config
        val pyConfig = PyDictionary().apply {
            put("remove_empty_methods", config.removeEmptyMethods)
            put("remove_getters_setters", config.removeGettersSetters)
            put("remove_logging", config.removeLogging)
            put("remove_empty_catches", config.removeEmptyCatches)
            put("remove_unused_variables", config.removeUnusedVariables)
            put("summarize_annotations", config.summarizeAnnotations)
            put("keep_method_signatures", config.keepMethodSignatures)
        }

        // Call Python method with proper PyObject arguments
        val result = summarizer.invoke(
            "process_file",
            arrayOf<PyObject>(pyContent, pyLanguage, pyConfig)
        )

        // Convert Python dict to Kotlin Map
        @Suppress("UNCHECKED_CAST")
        return (result as PyDictionary).toMap() as Map<String, Any>
    }
}