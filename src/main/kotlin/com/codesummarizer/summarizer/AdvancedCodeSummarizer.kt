package com.codesummarizer.summarizer

import com.codesummarizer.model.*
import com.codesummarizer.model.Language

class AdvancedCodeSummarizer {
    private val pythonSummarizer = PythonCodeSummarizer()

    fun process_file(content: String, language: Language, config: CleaningConfig): FileResult {
        // Delegate to Python implementation
        val result = pythonSummarizer.process_file(content, language.name.lowercase(), config)

        return FileResult(
            imports = result["imports"] as List<String>,
            cleanedContent = result["cleaned_content"] as String,
            methodSignatures = result["method_signatures"] as List<String>,
            tokenEstimate = result["token_estimate"] as Int
        )
    }
}