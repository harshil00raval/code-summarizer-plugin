package com.codesummarizer.model

data class CleaningConfig(
    val removeEmptyMethods: Boolean = true,
    val removeGettersSetters: Boolean = false,
    val removeLogging: Boolean = true,
    val removeEmptyCatches: Boolean = true,
    val removeUnusedVariables: Boolean = true,
    val summarizeAnnotations: Boolean = true,
    val keepMethodSignatures: Boolean = true
)