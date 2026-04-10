/*
 * Editor class for CodeMirror 6
 *
 * - Manage initial/filled cases;
 * - Use something else than JS for default language;
 * - We may implement a "language chooser" with a transaction looking on some select input (see Todo)
 *
 */
import {EditorView, basicSetup} from "codemirror";
import {EditorState} from "@codemirror/state"
import {javascript} from "@codemirror/lang-javascript"

import { DjangoBaseEditor } from "../modules/base_editor";

/**
 * Very minimal implementation of CodeMirror
 */
class DjangoCodeMirror6 extends DjangoBaseEditor {
    /**
     * Save editor content into source value
     */
    synchronizeInput(state) {
        console.log("source isFormControl:", this.isFormControl(this.source));
        if (this.isFormControl(this.source) === true) {
            console.log("Update input with content:", state.state.doc.toString());
            this.source.innerHTML = state.state.doc.toString();
        }
    }

    /**
     * Initialize, create and apply editor object.
     *
     * @return {Editor} - The created editor object.
     */
    provide() {
        this.container = this.prepareContainer();

        // TODO: This may be inefficient and for this editor we may prefer the
        // usage of submit but it require the form to be passed (opposed to suneditor
        // or tiptap)
        const seekForEditorUpdate = EditorState.transactionExtender.of(state => {
            if (!state.docChanged) return null
            this.synchronizeInput(state);
            return null
        });

        // only push seekForEditorUpdate extension if 'sync' is enabled
        const extensions = [basicSetup, javascript()];
        if (this.is_sync) {
            extensions.push(seekForEditorUpdate);
        }

        let base_options = {
            parent: this.container,
            doc: this.initial,
            extensions: extensions,
        };

        this.editor = new EditorView({...base_options, ...this.editor_options});

        // Listen to form submit to synchronize editor content in input value
        if (this.attached_form) {
            this.attached_form.addEventListener("submit", (e) => {
                this.synchronizeInput(e);
            });
        }

        return this.editor;
    }
}


// Export to browser
window.DjangoCodeMirror6 = DjangoCodeMirror6;
