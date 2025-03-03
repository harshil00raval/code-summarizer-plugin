package com.codesummarizer.service

import com.intellij.openapi.components.Service
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.psi.PsiManager
import com.codesummarizer.model.*
import com.codesummarizer.summarizer.AdvancedCodeSummarizer
import com.codesummarizer.model.Language
import com.intellij.openapi.command.WriteCommandAction
import com.intellij.psi.PsiDocumentManager
import com.intellij.psi.PsiFile

@Service
class SummarizerService(private val project: Project) {
    private val codeSummarizer = AdvancedCodeSummarizer()

    fun summarizeFiles(files: List<VirtualFile>, config: CleaningConfig): SummarizedResult {
        val results = mutableMapOf<String, FileResult>()
        var totalTokens = 0

        files.forEach { file ->
            val psiFile = PsiManager.getInstance(project).findFile(file)
            val language = determineLanguage(file.extension)

            psiFile?.let {
                val result = codeSummarizer.process_file(it.text, language, config)
                results[file.path] = result
                totalTokens += result.tokenEstimate

                updateFileContent(psiFile, result.cleanedContent)
            }
        }

        return SummarizedResult(results, totalTokens)
    }

    private fun determineLanguage(extension: String?): Language = when(extension) {
        "java" -> Language.JAVA
        "py" -> Language.PYTHON
        "groovy" -> Language.GROOVY
        else -> throw UnsupportedLanguageException(extension)
    }

    private fun updateFileContent(psiFile: PsiFile, newText: String) {
        val documentManager = PsiDocumentManager.getInstance(project)
        val document = documentManager.getDocument(psiFile)

        document?.let {
            WriteCommandAction.runWriteCommandAction(project) {
                it.setText(newText) // Replaces the entire file content
                documentManager.commitDocument(it) // Ensure changes are reflected
            }
        }
    }
}