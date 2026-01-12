/*
 * Editor class for TipTap V3
 */

import { Editor } from "@tiptap/core"
import StarterKit from "@tiptap/starter-kit"

import { DjangoBaseEditor } from "../modules/base_editor";

/**
 * Very minimal implementation of TipTap
 */
class DjangoTipTap extends DjangoBaseEditor {
    /**
     * Save editor content into source value
     */
    synchronizeInput(e) {
        if (this.isFormControl(this.source) === true) {
            this.source.innerHTML = this.editor.getHTML();
        }
    }

    /**
     * Initialize, create and apply editor object.
     *
     * @return {Editor} - The created editor object.
     */
    provide() {
        this.container = this.prepareContainer();

        this.editor = new Editor({
            element: this.container,
            extensions: [StarterKit],
            content: this.initial,
        });

        // Listen to editor content update to synchronize it in input value
        if (this.sync === true) {
            this.editor.on("update", ({editor}) => {
                this.synchronizeInput(editor);
            });
        }

        // Listen to to form submit to synchronize editor content in input value
        if (this.form) {
            this.form.addEventListener("submit", (e) => {
                this.synchronizeInput(e);
            });
        }

        return this.editor;
    }
}


// Export to browser
window.DjangoTipTap = DjangoTipTap;
