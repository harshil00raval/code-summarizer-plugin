package com.codesummarizer.action

import com.codesummarizer.service.SummarizerService
import com.codesummarizer.summarizer.AdvancedCodeSummarizer
import com.intellij.openapi.actionSystem.AnAction
import com.intellij.openapi.actionSystem.AnActionEvent
import com.intellij.openapi.actionSystem.CommonDataKeys
import com.codesummarizer.ui.SummarizerConfigDialog
import com.intellij.openapi.project.Project
import com.intellij.openapi.vfs.VirtualFile
import com.intellij.psi.PsiManager

class SummarizeCodeAction : AnAction() {

    override fun actionPerformed(e: AnActionEvent) {
        val project = e.project ?: return
        val summarizer = SummarizerService(project)
        val selectedFiles = e.getData(CommonDataKeys.VIRTUAL_FILE_ARRAY)?.toList() ?: return

        val dialog = SummarizerConfigDialog(project)
        if (dialog.showAndGet()) {
            val config = dialog.getConfig()
            summarizer.summarizeFiles(selectedFiles, config)
        }
    }

    private fun getSelectedFiles(e: AnActionEvent): List<VirtualFile> {
        val virtualFiles = e.getData(CommonDataKeys.VIRTUAL_FILE_ARRAY) ?: return emptyList()
        return virtualFiles.filter { it.isValid && !it.isDirectory }
    }
}