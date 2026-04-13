/*
 * Editor class for CodeMirror 6
 */
import {basicSetup} from "codemirror";
import {EditorView, keymap} from "@codemirror/view";
import {EditorState} from "@codemirror/state";
import {indentWithTab} from "@codemirror/commands";
import {css} from "@codemirror/lang-css";
import {html} from "@codemirror/lang-html";
import {javascript} from "@codemirror/lang-javascript";
import {jinja} from "@codemirror/lang-jinja";
import {python} from "@codemirror/lang-python";
import {sass} from "@codemirror/lang-sass";

import { DjangoBaseEditor } from "../modules/base_editor";

/**
 * Very minimal implementation of CodeMirror
 *
 * NOTE:
 * Since CodeMirror does not use a delay to pack updates on changes,  the usage of
 * 'sync' is quite inefficient. You should prefer the usage of 'form' submit.
 */
class DjangoCodeMirror6 extends DjangoBaseEditor {

    /**
     * Getter for wrapper option 'lang_extension'
     */
    get lang_extension() {
        return this.wrapper_options["lang_extension"] ?
                this.wrapper_options["lang_extension"]
                : "python";
    }

    /**
     * Setter for wrapper option 'lang_extension'
     */
    set lang_extension(value) {
        this.wrapper_options["lang_extension"] = value;
    }

    /**
     * Getter for wrapper option 'allowed_extensions'
     */
    get allowed_extensions() {
        return this.wrapper_options["allowed_extensions"] ?
                this.wrapper_options["allowed_extensions"]
                : ["python"];
    }

    /**
     * Setter for wrapper option 'allowed_extensions'
     */
    set allowed_extensions(value) {
        this.wrapper_options["allowed_extensions"] = value;
    }

    /**
     * Check if given extension name is an allowed extension
     *
     * @param {string} name - An extension name to be checked.
     */
    is_allowed_extension(name) {
        return this.allowed_extensions.indexOf(name) === -1 ? false : true;
    }

    /**
     * Save editor content into source value
     */
    synchronizeInput(state) {
        if (this.isFormControl(this.source) === true) {
            this.source.innerHTML = state.state.doc.toString();
        }
    }

    /**
     * Initialize, create and apply editor object.
     *
     * @return {EditorView} - The created editor object.
     */
    provide() {
        this.container = this.prepareContainer();

        // Editor extensions
        let extensions = [
            basicSetup,
            keymap.of([indentWithTab]),
        ];

        if(!this.is_allowed_extension(this.lang_extension)) {
            throw new Error(
                "Given extension name is not available: " + this.lang_extension
            );
        }

        switch (this.lang_extension) {
            case "css":
                extensions.push(css());
                break;
            case "html":
                extensions.push(html());
                break;
            case "javascript":
                extensions.push(javascript());
                break;
            case "jinja":
                extensions.push(jinja());
                break;
            case "python":
                extensions.push(python());
                break;
            case "sass":
                extensions.push(sass());
                break;
            default:
                break;
        }

        // Only push 'update on each change' extension if 'sync' is enabled
        if (this.is_sync) {
            const seekForEditorUpdate = EditorState.transactionExtender.of(state => {
                if (!state.docChanged) return null
                this.synchronizeInput(state);
                return null
            });

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
