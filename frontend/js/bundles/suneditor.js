/*
 * Editor class for SunEditor V3
 *
 * TODO: - What options ?
 *         - Tab key management option because on default Suneditor use four &nbsp;
 *           when tab key is pressed. This is not expected tab key behavior (on default
 *           indent on newline start or natural browser behavior to switch to another
 *           element;
 *       - How to enable plugins ?
 *       - Search if MiniCssExtractPlugin can produce CSS into '../css/' instead of
 *         the 'js/' directory.
 */

import suneditor from "suneditor";
import "suneditor/css/editor";
import "suneditor/css/contents";

import { DjangoBaseEditor } from "../modules/base_editor.js";

/**
 * Very minimal implementation of SunEditor
 */
class DjangoSunEditor extends DjangoBaseEditor {
    /**
     * Save editor content into source value
     */
    synchronizeInput(e) {
        // Worked in 3.0.0beta34 but not since 3.0.0 release
        // this.editor.run("save");
        // Doing it in the raw way for now
        if (this.isFormControl(this.source) === true) {
            this.source.innerHTML = e.data;
        }
    }

    /**
     * SunEditor does not need any preparation because it accords automatically to
     * any source element
     */
    prepareContainer() {}

    /**
    * Initialize, create and apply editor object.
    *
    * @return {Editor} - The created editor object.
    */
    provide() {
        // No need of preparing source because SunEditor will make all the job to
        // replace input
        this.container = this.source;

        const editor_options = {
            ...{
                events: {
                    onChange: (e) => {
                        if (this.is_sync) {
                            this.synchronizeInput(e);
                        }
                    }
                },
            },
            ...this.editor_options
        };

        this.editor = suneditor.create(
            this.container,
            editor_options
        );

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
window.DjangoSunEditor = DjangoSunEditor;
