package com.codesummarizer.ui

import com.intellij.openapi.project.Project
import com.codesummarizer.model.CleaningConfig
import com.intellij.openapi.ui.DialogWrapper
import javax.swing.BoxLayout
import javax.swing.JComponent
import javax.swing.JPanel
import javax.swing.JCheckBox

class SummarizerConfigDialog(project: Project) : DialogWrapper(project) {
    private val removeEmptyMethods = JCheckBox("Remove empty methods")
    private val removeGettersSetters = JCheckBox("Remove getters/setters")
    private val removeLogging = JCheckBox("Remove logging statements")
    private val removeEmptyCatches = JCheckBox("Remove empty catch blocks")
    private val removeUnusedVariables = JCheckBox("Remove unused variables")
    private val summarizeAnnotations = JCheckBox("Summarize annotations")
    private val keepMethodSignatures = JCheckBox("Keep method signatures")

    init {
        title = "Code Summarizer Configuration"
        init()
    }

    override fun createCenterPanel(): JComponent {
        return JPanel().apply {
            layout = BoxLayout(this, BoxLayout.Y_AXIS)
            add(removeEmptyMethods)
            add(removeGettersSetters)
            add(removeLogging)
            add(removeEmptyCatches)
            add(removeUnusedVariables)
            add(summarizeAnnotations)
            add(keepMethodSignatures)
        }
    }

    fun getConfig(): CleaningConfig = CleaningConfig(
        removeEmptyMethods.isSelected,
        removeGettersSetters.isSelected,
        removeLogging.isSelected,
        removeEmptyCatches.isSelected,
        removeUnusedVariables.isSelected,
        summarizeAnnotations.isSelected,
        keepMethodSignatures.isSelected
    )
}