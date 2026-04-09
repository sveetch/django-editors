/*
 * Editor class for CodeMirror 6
 *
 * - Manage initial/filled cases;
 * - Use something else than JS for default language;
 * - We may implement a "language chooser" with a transaction looking on some select input:
 * https://codemirror.net/try/#c=aW1wb3J0IHtFZGl0b3JTdGF0ZSwgQ29tcGFydG1lbnR9IGZyb20gIkBjb2RlbWlycm9yL3N0YXRlIgppbXBvcnQge2h0bWxMYW5ndWFnZSwgaHRtbH0gZnJvbSAiQGNvZGVtaXJyb3IvbGFuZy1odG1sIgppbXBvcnQge2xhbmd1YWdlfSBmcm9tICJAY29kZW1pcnJvci9sYW5ndWFnZSIKaW1wb3J0IHtqYXZhc2NyaXB0fSBmcm9tICJAY29kZW1pcnJvci9sYW5nLWphdmFzY3JpcHQiCgpjb25zdCBsYW5ndWFnZUNvbmYgPSBuZXcgQ29tcGFydG1lbnQKCmNvbnN0IGF1dG9MYW5ndWFnZSA9IEVkaXRvclN0YXRlLnRyYW5zYWN0aW9uRXh0ZW5kZXIub2YodHIgPT4gewogIGlmICghdHIuZG9jQ2hhbmdlZCkgcmV0dXJuIG51bGwKICBsZXQgZG9jSXNIVE1MID0gL15ccyo8Ly50ZXN0KHRyLm5ld0RvYy5zbGljZVN0cmluZygwLCAxMDApKQogIGxldCBzdGF0ZUlzSFRNTCA9IHRyLnN0YXJ0U3RhdGUuZmFjZXQobGFuZ3VhZ2UpID09IGh0bWxMYW5ndWFnZQogIGlmIChkb2NJc0hUTUwgPT0gc3RhdGVJc0hUTUwpIHJldHVybiBudWxsCiAgcmV0dXJuIHsKICAgIGVmZmVjdHM6IGxhbmd1YWdlQ29uZi5yZWNvbmZpZ3VyZShkb2NJc0hUTUwgPyBodG1sKCkgOiBqYXZhc2NyaXB0KCkpCiAgfQp9KQoKaW1wb3J0IHtFZGl0b3JWaWV3LCBiYXNpY1NldHVwfSBmcm9tICJjb2RlbWlycm9yIgoKbmV3IEVkaXRvclZpZXcoewogIGRvYzogJ2NvbnNvbGUubG9nKCJoZWxsbyIpJywKICBleHRlbnNpb25zOiBbCiAgICBiYXNpY1NldHVwLAogICAgbGFuZ3VhZ2VDb25mLm9mKGphdmFzY3JpcHQoKSksCiAgICBhdXRvTGFuZ3VhZ2UKICBdLAogIHBhcmVudDogZG9jdW1lbnQucXVlcnlTZWxlY3RvcigiI2VkaXRvciIpIHx8IGRvY3VtZW50LmJvZHkKfSkK
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

        // only push seekForEditorUpdate extension if this.sync is enabled
        const extensions = [basicSetup, javascript()];
        if (this.sync === true) {
            extensions.push(seekForEditorUpdate);
        }

        let base_options = {
            parent: this.container,
            doc: this.initial,
            extensions: extensions,
        };

        this.editor = new EditorView({...base_options, ...this.options});

        // Listen to editor content update to synchronize it in input value
//         if (this.sync === true) {
//             this.editor.on("update", ({editor}) => {
//                 this.synchronizeInput(editor);
//             });
//         }

        // Listen to form submit to synchronize editor content in input value
        // TODO: This is not working yet
        if (this.form) {
            this.form.addEventListener("submit", (e) => {
                this.synchronizeInput(e);
            });
        }

        return this.editor;
    }
}


// Export to browser
window.DjangoCodeMirror6 = DjangoCodeMirror6;
