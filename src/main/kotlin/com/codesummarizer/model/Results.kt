package com.codesummarizer.model

data class FileResult(
    val imports: List<String>,
    val cleanedContent: String,
    val methodSignatures: List<String>,
    val tokenEstimate: Int
)

data class SummarizedResult(
    val files: Map<String, FileResult>,
    val totalTokens: Int
)

class UnsupportedLanguageException(extension: String?) :
    Exception("Unsupported file extension: $extension")